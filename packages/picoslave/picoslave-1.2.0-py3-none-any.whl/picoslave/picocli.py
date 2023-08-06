#!/usr/bin/env python3

"""
\033[1;33mpicocli\033[0m a CLI tool to control the \033[1;33mPicoSlave\033[0m I2C/USB slave simulator.

PicoSlave USB devices have the vid/pid \033[0;33mC001:012C\033[0m and are automatically detected
by this tool if only one is present. The \033[1;39mscan\033[0m command lists devices showing an
index and the device serial number, by which a specific device can be selected
using \033[1;39m-i\033[0m or \033[1;39m-s\033[0m.

\033[1;33mPicoSlave\033[0m supports 2 I2C slaves to be each configured via the \033[1;39mconfig\033[0m command
command for an I2C slave address to operate on a register space of configurable
size starting at address 0x00. Slave operation can be disabled by configuring a
slave for the I2C address 0x00. Slaves 0 or 1 are selected using the \033[1;39miface\033[0m
argument for all slave specific commands.

The register spaces of the slaves can be written into (\033[1;39mwrite\033[0m) and read from (\033[1;39mread\033[0m).
This can be done when slaves are enabled or disabled. \033[1;39mclear\033[0m resets the entire
configured register space to 0x00 or a given value.
"""  # pylint: disable=line-too-long  # noqa

import argparse
import logging
import sys

import picoslave as ps
from picoslave.picoslave import PicoSlave, UsbPicoSlave
from picoslave.picoslave import bytestr
from picoslave.picoslave import DeviceNotFound, UsbError


def config_cmd(args: argparse.Namespace, picoslave: PicoSlave) -> None:
    if args.slave_addr == 0:
        print(f'deactivating I2C-{args.iface}')
    else:
        print(f'configuring I2C-{args.iface} for address {args.slave_addr:02X}h, '
              f'size {args.size} and word width {args.width}')
    picoslave.config(args.iface, args.slave_addr, args.size, args.width)


def read_cmd(args: argparse.Namespace, picoslave: PicoSlave) -> None:
    print(f'reading from I2C-{args.iface}: {args.size} bytes from address {args.addr:02X}h')
    response_data = picoslave.read(args.iface, args.addr, args.size)
    print('response:')
    print(bytestr(response_data))


def write_cmd(args: argparse.Namespace, picoslave: PicoSlave) -> None:
    print(f'writing to I2C-{args.iface}: {len(args.data)} '
          f'{"bytes" if len(args.data) > 1 else "byte"} to address {args.addr:02X}h:')
    print(bytestr(args.data))
    picoslave.write(args.iface, args.addr, args.data)


def clear_cmd(args: argparse.Namespace, picoslave: PicoSlave) -> None:
    print(f'clearing memory of I2C-{args.iface} with value {args.value:02x}h')
    picoslave.clear(args.iface, args.value)


def stat_cmd(args: argparse.Namespace, picoslave: PicoSlave) -> None:
    print(f'reading statistics from I2C-{args.iface}: {args.size} entries '
          f'from address {args.addr:02X}h')
    statistics = picoslave.statistics(args.iface, args.addr, args.size)
    print('  ADDR  READ  WRITE')
    for addr in statistics:
        if statistics[addr][0] or statistics[addr][1]:
            print(f'   {addr:02X}h  {statistics[addr][0]:4}   {statistics[addr][1]:4}')


def info_cmd(args: argparse.Namespace, picoslave: PicoSlave) -> None:
    info = picoslave.info()
    print(info)


def reset_cmd(args: argparse.Namespace, picoslave: PicoSlave) -> None:
    print('resetting target')
    try:
        picoslave.reset()
    except UsbError:
        pass


def main() -> None:

    loglevels = ['debug', 'info', 'warning', 'error', 'critical']
    ifaces = [0, 1]

    def auto_int(x: str) -> int:
        return int(x, 0)

    def mem_addr8(x: str) -> int:
        addr = auto_int(x)
        if addr >= 2**8:
            raise argparse.ArgumentTypeError(f'address must be in range [0..{2**8-1}]')
        return addr

    def mem_addr16(x: str) -> int:
        addr = auto_int(x)
        if addr >= 2**16:
            raise argparse.ArgumentTypeError(f'address must be in range [0..{2**16-1}]')
        return addr

    def byte_str(x: str) -> bytes:
        try:
            return bytes.fromhex(x)
        except Exception:
            raise argparse.ArgumentTypeError(f'not a valid byte string: "{x}"')

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-l', '--loglevel', metavar='L', type=str, default='Warning',
                        choices=loglevels,
                        help=f'log level: L={loglevels}')
    parser.add_argument('-d', '--debug', action='store_true',
                        help="shortcut for '--loglevel debug'")
    device_group = parser.add_mutually_exclusive_group()
    device_group.add_argument('-i', '--index', type=int, metavar='X',
                              help="Device index to select a specific PicoSlave device\n"
                                   "(see cmd='scan')")
    device_group.add_argument('-s', '--serial', type=str, metavar='S',
                              help='Device serial number to select a specific PicoSlave\n'
                                   "device (see cmd='scan')")
    parser.add_argument('-V', '--version', action='store_true', help='show the program version')

    # subparsers
    sub = parser.add_subparsers(title='command', dest='command',
                                description='commands to execute on PicoSlave')
    iface_parser = argparse.ArgumentParser(add_help=False)
    iface_parser.add_argument('iface', type=int, metavar='iface', choices=ifaces,
                              help=f'I2C interface number ({ifaces})')

    # config
    config_parser = sub.add_parser('config', aliases=['c'], parents=[iface_parser],
                                   help='configure an I2C slave')
    config_parser.add_argument('slave_addr', type=auto_int,
                               help='Memory or 7-bit slave address (use -8 for 8-bit addresses)')
    config_parser.add_argument('-8', dest='eightbit', action='store_true',
                               help='Set to interpret I2C addresses as 8-bit (default is 7-bit)')
    config_parser.add_argument('size', type=int, nargs='?', default=256,
                               help='size of the configured I2C memory, at which it will overflow '
                                    '(max 256). Note that the I2C memory size is given in words '
                                    '(of size [width]), not bytes.')
    config_parser.add_argument('width', type=int, nargs='?', default=1, choices=[1, 2, 4],
                               metavar='width',
                               help='width of data words in I2C memory (1, 2 or 4)')
    config_parser.set_defaults(func=config_cmd)

    # read
    read_parser = sub.add_parser('read', aliases=['r'], parents=[iface_parser],
                                 help='read from the slaves I2C memory')
    read_parser.add_argument('addr', type=mem_addr16, help='address to start reading from')
    read_parser.add_argument('size', type=int, nargs='?', default=1,
                             help='number of words to read from [addr] (max 256 * [width])')
    read_parser.set_defaults(func=read_cmd)

    # write
    write_parser = sub.add_parser('write', aliases=['w'], parents=[iface_parser],
                                  help='write data to the slaves I2C memory')
    write_parser.add_argument('addr', type=mem_addr16, help='address to start writing into')
    write_parser.add_argument('data', type=byte_str,
                              help='data to write to the I2C memory at [addr].\n'
                                   'Data format is a little endian hex string without spaces, '
                                   'e.g.: 03ab7fE0 (4 bytes). Note that data length must be a '
                                   'multiple of the configured word [width]. (see "config -h")')
    write_parser.set_defaults(func=write_cmd)

    # clear
    clear_parser = sub.add_parser('clear', aliases=['C'], parents=[iface_parser],
                                  help='clear the I2C memory to 0 or an initial value')
    clear_parser.add_argument('value', type=auto_int, nargs='?', default=0x00,
                              help='initialize with this value')
    clear_parser.set_defaults(func=clear_cmd)

    # stat
    stat_parser = sub.add_parser('stat', aliases=['s'], parents=[iface_parser],
                                 help='retrieve read/write statistics from I2C memory')
    stat_parser.add_argument('addr', type=mem_addr8, nargs='?', default=0x00,
                             help='start memory address for reading statistics')
    stat_parser.add_argument('size', type=int, nargs='?', default=256,
                             help='number of addresses/words to get r/w statistics for (max 256)')
    stat_parser.set_defaults(func=stat_cmd)

    # scan
    scan_parser = sub.add_parser('scan', aliases=['S'], help='scan for PicoSlave devices on USB')
    scan_parser.set_defaults(func='scan_cmd')

    # info
    info_parser = sub.add_parser('info', aliases=['I'], help='print info for the selected device')
    info_parser.set_defaults(func=info_cmd)

    # reset
    reset_parser = sub.add_parser('reset', aliases=['R'], help='reset the PicoSlave device')
    reset_parser.set_defaults(func=reset_cmd)

    args = parser.parse_args()

    if args.version:
        print(f'PicoSlave {ps.__version__}')
        exit(0)

    if args.debug:
        args.loglevel = 'debug'

    log_format = '%(asctime)s %(name)-10s %(levelname)-8s %(message)s'
    logging.basicConfig(level=logging.getLevelName(args.loglevel.upper()), format=log_format)

    try:
        import coloredlogs  # type: ignore
        coloredlogs.install(level=logging.getLevelName(args.loglevel.upper()), fmt=log_format)
    except ModuleNotFoundError:
        pass

    if 'func' not in args:
        parser.print_help()
        exit(1)

    if args.func == 'scan_cmd':
        devices = UsbPicoSlave.scan()
        sys.exit(1 if not devices else 0)

    # do command specific parsing before we create the PicoSlave
    if args.func == config_cmd:
        if args.eightbit:
            print(f"converting 8-bit address '{args.slave_addr:02X}h' to 7-bit address "
                  f'{args.slave_addr >> 1:02X}h')
            args.slave_addr = args.slave_addr >> 1
        assert args.slave_addr <= 0x7F, 'I2C address out of range [0..7Fh]'

    assert args.index is None or args.index > 0, 'Device index must not be 0'
    args.index = args.index - 1 if args.index is not None else None

    picoslave = PicoSlave(index=args.index, serial=args.serial)

    try:
        args.func(args, picoslave)
    except (AssertionError, DeviceNotFound) as e:
        if str(e):
            print(f'ERROR: {e}')
            sys.exit(1)
        raise


if __name__ == '__main__':
    main()
