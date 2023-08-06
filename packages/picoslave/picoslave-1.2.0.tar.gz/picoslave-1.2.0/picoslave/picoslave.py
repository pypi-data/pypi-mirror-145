from enum import IntEnum
import logging
import struct
from typing import List, Dict, Tuple, Any, Optional, cast

import usb.core  # type: ignore
import usb.util  # type: ignore
import usb.legacy  # type: ignore


log = logging.getLogger('picoslave')


def bytestr(b: bytes) -> str:
    return ' '.join(f'{x:02X}' for x in b)


class DeviceNotFound(Exception):
    """error when a specified device was not found"""


class UsbError(Exception):
    """error when communication with the device was not possible"""


class ProtocolError(Exception):
    """when unexpected respnses are received from the device"""


class UsbPicoSlave:

    ID_VENDOR = 0xC001
    ID_PRODUCT = 0x012C
    OUT_EP_ADDR = 0x04
    IN_EP_ADDR = 0x85

    def __init__(self, device: usb.core.Device) -> None:
        assert device is not None

        cfg = device.get_active_configuration()
        assert cfg is not None, 'no active configuration on device'

        intf = usb.util.find_descriptor(cfg, bInterfaceClass=usb.legacy.CLASS_VENDOR_SPEC)
        assert intf is not None, "couldn't find PicoSlave interface on device"

        outep = usb.util.find_descriptor(intf, bEndpointAddress=self.OUT_EP_ADDR)
        assert outep is not None, f"OUT endpoint (0x{self.OUT_EP_ADDR:02X}) not found on device"

        inep = usb.util.find_descriptor(intf, bEndpointAddress=self.IN_EP_ADDR)
        assert outep is not None, f"IN endpoint (0x{self.IN_EP_ADDR:02X}) not found on device"

        self._device = device
        self._inep = inep
        self._outep = outep

    def close(self) -> None:
        self._device.reset()

    def write(self, data: bytes) -> None:
        """raises: UsbError"""
        try:
            wire_hdr = struct.pack('I', len(data))
            self._outep.write(wire_hdr + data)
        except usb.core.USBTimeoutError as e:
            raise UsbError(f'No response from device ({e})')

    def read(self) -> bytes:
        """raises: UsbError"""
        try:
            packet = self._inep.read(8192)
            len_hdr = struct.unpack('I', packet[:4])[0]
            data = packet[4:]
            log.debug(f'[rx]: len_hdr: {len_hdr}, len(data): {len(data)}')
            if len_hdr != len(data):
                raise ProtocolError('received wrong number of bytes')
            return bytes(list(data))
        except usb.core.USBTimeoutError as e:
            raise UsbError(f'No response from device ({e})')

    @classmethod
    def _scan(cls) -> List[usb.core.Device]:
        devs = usb.core.find(idVendor=cls.ID_VENDOR, idProduct=cls.ID_PRODUCT, find_all=True)
        devices: List[usb.core.Device] = []
        for d in devs:
            try:
                # try to access the serial number.
                # this gives an error when the device is in a weird state
                log.debug(f'found device with serial number: {d.serial_number}')
            except Exception as e:
                log.warning(f"couldn't read from device: {e}")
                continue
            devices.append(d)
        return sorted(devices, key=lambda d: cast(int, d.serial_number))

    @classmethod
    def scan(cls) -> List[usb.core.Device]:
        devices = cls._scan()
        vid_pid = f'{cls.ID_VENDOR:04x}:{cls.ID_PRODUCT:04x}'
        id = 1
        for d in devices:
            usb_path = f'{d.bus}.{".".join(str(p) for p in d.port_numbers)}:{d.address}'
            print(f'{id:>2}  {d.serial_number:<16}  {usb_path:>12}-{vid_pid:<9}'
                  f'  {d.manufacturer} {d.product} ')
            id += 1
        if not devices:
            print(f'no PicoSlave device found with {vid_pid}')
        return devices

    @classmethod
    def find(cls, index: Optional[int] = None, serial: Optional[str] = None) -> 'UsbPicoSlave':
        assert index is None or serial is None, "'index' and 'serial' must not be both set"

        selected_device: usb.core.Device = None
        devices = cls._scan()

        try:
            if index is not None:
                assert index < len(devices), f'No device with index "{index}"'
                selected_device = devices[index]
            elif serial is not None:
                matching = [dev for dev in devices if dev.serial_number == serial]
                assert matching, f'No device found with serial number "{serial}"'
                assert len(matching) == 1, \
                    f'Multiple devices found with serial number "{serial}". '\
                    'Select with "index" filter'
                selected_device = matching[0]
            else:
                assert len(devices) > 0, 'No device found'
                assert len(devices) == 1, \
                    'Multiple devices found. Select with "index" or "serial" filter.'
                selected_device = devices[0]
            assert selected_device is not None, 'FATAL: No device found (unknown reason)'
        except AssertionError as e:
            raise DeviceNotFound(e) from e
        return UsbPicoSlave(selected_device)


class PicoSlave:
    class Protocol:

        MAX_RW_SIZE = 32

        class Command(IntEnum):
            CONFIG = 0xA0
            READ = 0xA1
            WRITE = 0xA2
            CLEAR = 0xA3
            STAT = 0xA4
            INFO = 0xB0
            RESET = 0xBF

        class ResponseCode(IntEnum):
            OK = 0
            CRC_ERROR = 1
            INVALID_PACKET = 2
            INVALID_REQUEST = 3
            INVALID_INTERFACE = 4
            INVALID_ADDRESS = 5
            INVALID_SIZE = 6
            INVALID_WIDTH = 7
            MEMORY_ERROR = 8
            OPERATION_FAILED = 9

        @staticmethod
        def crc16(data: bytes, poly: int = 0x8408) -> int:
            """CRC-16-CCITT Algorithm
            source: https://gist.github.com/oysstu/68072c44c02879a2abf94ef350d1c7c6"""
            crc = 0xFFFF
            for b in data:
                cur_byte = 0xFF & b
                for _ in range(0, 8):
                    if (crc & 0x0001) ^ (cur_byte & 0x0001):
                        crc = (crc >> 1) ^ poly
                    else:
                        crc >>= 1
                    cur_byte >>= 1
            crc = (~crc & 0xFFFF)
            crc = (crc << 8) | ((crc >> 8) & 0xFF)
            return crc & 0xFFFF

        @classmethod
        def packet(cls, cmd: Command, iface: int, addr: int, size: int = 0,
                   data: Optional[bytes] = None, mem_width: int = 0) -> bytes:
            assert size is None or size < 2**16
            assert addr < 2**16, 'addr must be in range [0..2**16]'
            if cmd == cls.Command.CONFIG:
                assert data is None, 'CONFIG must not have data'
                assert size > 0, 'CONFIG needs size > 0'
                data = struct.pack('B', mem_width)
            elif cmd == cls.Command.READ or cmd == cls.Command.STAT:
                assert size > 0, 'READ/STAT packet needs size > 0'
                assert data is None, 'READ/STAT must not have data'
            elif cmd == cls.Command.WRITE:
                assert data is not None, 'WRITE packet needs data'
                size = len(data)
            elif cmd == cls.Command.CLEAR:
                assert size == 0, 'CLEAR size must be 0'
                assert data is None, 'CLEAR must not have data'
            elif cmd == cls.Command.RESET:
                assert size == 0, 'RESET size must be 0'
                assert data is None, 'RESET must not have data'
            elif cmd == cls.Command.INFO:
                assert size == 0, 'INFO size must be 0'
                assert data is None, 'INFO must not have data'
            else:
                assert False, f'Unsupported CMD: {cmd}'
            header = bytes([int(cmd), iface]) + struct.pack('H', addr) + struct.pack('H', size)
            packet = header + (data or bytes([]))
            crc = struct.pack('H', cls.crc16(packet))
            return packet + crc

        @classmethod
        def verify(cls, packet: bytes) -> bytes:
            # check that the packet is long enough to make any sense
            assert len(packet) >= 5, f'invalid received packet size: {len(packet)}'

            # check CRC before looking into the packet
            crc_calc = cls.crc16(packet[:-2])
            crc_rx = struct.unpack('H', packet[-2:])[0]
            assert crc_calc == crc_rx, 'CRC mismatch'
            log.debug('rx packet CRC check successful')
            packet_data = packet[:-2]

            # check the result code
            try:
                code = packet_data[0]
                response_code = cls.ResponseCode(code)
                assert response_code == cls.ResponseCode.OK, \
                    f'received error code {code} ({response_code.name})'
                # FIXME: this should be a testable exception
            except ValueError:
                assert False, f'received unknown response code: {code}'

            # check the packet data size (-3 is the header size)
            size = struct.unpack('H', packet_data[1:3])[0]
            assert size == len(packet_data) - 3, \
                f'received packet size mismatch: size={size}, data={len(packet_data) - 3}'
            return packet_data[3:]

    def __init__(self, index: Optional[int] = None, serial: Optional[str] = None) -> None:
        assert index is None or serial is None, "'index' and 'serial' must not be both set"
        self._usb = UsbPicoSlave.find(index=index, serial=serial)

    def close(self) -> None:
        self._usb.close()

    def _txrx(self, packet: bytes) -> bytes:
        """raises: UsbError"""

        log.debug(f'tx-packet: {bytestr(packet)}')
        try:
            self._usb.write(packet)
        except usb.core.USBError as e:
            raise UsbError(e)

        try:
            response = self._usb.read()
        except usb.core.USBError as e:
            raise UsbError(e)
        log.debug(f'rx-packet: {bytestr(response)}')

        try:
            rx_data = self.Protocol.verify(response)
        except AssertionError as e:
            raise ProtocolError(e)
        log.debug(f'rx-data: {bytestr(rx_data)}')
        return rx_data

    def config(self, iface: int, slave_address: int, mem_size: int = 256,
               mem_width: int = 1) -> None:
        """Initialize or re-initialize the slave for a given I2C address.
        Address 0 deactivates the slave. """
        assert mem_size > 0  # FIXME [#12]: can't test currently... and mem_size <= 256
        assert mem_width in [1, 2, 4]
        log.info(f'config: iface={iface}, slave_address={slave_address:02X}h, '
                 f'mem_size={mem_size}, mem_width={mem_width}')
        packet = self.Protocol.packet(self.Protocol.Command.CONFIG,
                                      iface, slave_address, mem_size, mem_width=mem_width)
        rsp = self._txrx(packet)
        if rsp:
            raise ProtocolError(f'CONFIG received an unexpected response: {bytestr(rsp)}')

    def read(self, iface: int, mem_addr: int, size: int) -> bytes:
        log.info(f'read: iface={iface}, mem_addr={mem_addr:02X}h, size={size}')
        packet = self.Protocol.packet(self.Protocol.Command.READ, iface, mem_addr, size)
        rsp = self._txrx(packet)
        assert len(rsp) > 0, 'received no data'
        return rsp

    def write(self, iface: int, mem_addr: int, data: bytes) -> None:
        log.info(f'write: iface={iface}, mem_addr={mem_addr:02X}h, data_size={len(data)}, '
                 f'data="{bytestr(data)}"')
        packet = self.Protocol.packet(self.Protocol.Command.WRITE, iface, mem_addr, len(data), data)
        rsp = self._txrx(packet)
        if rsp:
            raise ProtocolError(f'WRITE received an unexpected response: {bytestr(rsp)}')

    def clear(self, iface: int, reset_value: int = 0) -> None:
        log.info(f'clear: iface={iface}, reset_value={reset_value}')
        packet = self.Protocol.packet(self.Protocol.Command.CLEAR, iface, reset_value)
        rsp = self._txrx(packet)
        if rsp:
            raise ProtocolError(f'CLEAR received an unexpected response: {bytestr(rsp)}')

    def statistics(self, iface: int, mem_addr: int, size: int) -> Dict[int, Tuple[int, int]]:
        log.info(f'stat: iface={iface}, mem_addr={mem_addr:02X}h, size={size}')
        packet = self.Protocol.packet(self.Protocol.Command.STAT, iface, mem_addr, size)
        rsp = self._txrx(packet)
        assert len(rsp) > 0, 'received no data'
        assert len(rsp) % 8 == 0, f'received data size is no multiple of 8 (size={len(rsp)})'

        statistics = {}
        stat_addr = mem_addr
        for i in range(0, len(rsp), 8):
            read_cnt = struct.unpack('I', rsp[i:i + 4])[0]
            write_cnt = struct.unpack('I', rsp[i + 4:i + 8])[0]
            statistics[stat_addr] = (read_cnt, write_cnt)
            stat_addr += 1
        return statistics

    def info(self) -> Dict[str, Any]:
        log.info('reading device info')
        packet = self.Protocol.packet(self.Protocol.Command.INFO, 0, 0)
        rsp = self._txrx(packet)
        assert len(rsp) > 0, 'received no data'
        info = rsp.decode("utf-8")
        infos = info.split(';')
        assert len(infos) == 4, 'received unexpected number of info segments'
        return dict(
            serial=infos[0],
            firmware=infos[1],
            protocol=infos[2],
            interfaces=int(infos[3]),
        )

    def reset(self) -> None:
        log.info('reset device')
        packet = self.Protocol.packet(self.Protocol.Command.RESET, 0, 0)
        rsp = self._txrx(packet)
        if rsp:
            raise ProtocolError(f'RESET received an unexpected response: {bytestr(rsp)}')
