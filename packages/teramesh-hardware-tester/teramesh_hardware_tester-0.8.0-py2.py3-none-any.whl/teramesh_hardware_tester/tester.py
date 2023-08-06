#!/bin/env python3

import asyncio
import click
import csv
import esptool
import glob
import importlib
import logging
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import termios
import tty
from serial.tools import list_ports

from .idrc_esp_tools import serial_asyncio, at
from .idrc_esp_tools.gen_esp32part import PartitionTable


logger = logging.getLogger('tester')
logger.setLevel(logging.INFO)

BASE_DIR = os.path.dirname(__file__)
TMP_DIR = os.path.join(os.environ['HOME'], '.hwtester')

exit_code = 0


def getch():
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    return _getch()


class SerialTestRunner:

    def __init__(self, usb_port, baudrate):
        self.usb_port = usb_port
        self.baudrate = baudrate

    def set_nvs_testing_flag(self):

        os.makedirs(TMP_DIR, exist_ok=True)

        with tempfile.NamedTemporaryFile(dir=TMP_DIR, suffix='.bin') as f:

            # dump partition table from a running node
            esptool.main([
                '-p',
                self.usb_port,
                '--after',
                'no_reset',
                'read_flash',
                '0x8000',
                '0x1000',
                f.name,
            ])
            logger.info('Dumped partition table')

            f.seek(0)
            partition_table = PartitionTable.from_binary(f.read())
            test_partition = partition_table.find_by_name('test')
            assert test_partition, 'Test partition not found!'
            logger.info('Test partition @%s len: %s', test_partition.offset, test_partition.size)

        with tempfile.NamedTemporaryFile(dir=TMP_DIR, suffix='.bin') as f:

            # prepare test partition contents
            f.write(b'test')
            f.write(b'\x00' * (test_partition.size - 4))
            f.flush()

            # flash test partition and reboot the node
            esptool.main([
                '-p',
                self.usb_port,
                'write_flash',
                str(test_partition.offset),
                f.name,
            ])
            logger.info('Flashed test flag partition')

        # TODO: start testing
        logger.info('Ready to test!')

    @staticmethod
    def get_all_tests():
        for filename in glob.glob(os.path.join(BASE_DIR, 'tests/**/test*.py'), recursive=True):
            module = importlib.machinery.SourceFileLoader('test', filename).load_module()
            for func_name in dir(module):
                if func_name.startswith('test') and callable(getattr(module, func_name)):
                    yield {
                        'filename': os.path.basename(filename),
                        'func': func_name,
                    }

    @staticmethod
    def get_all_ports():
        for port in list_ports.comports():
            yield {
               'device': port.device,
               'name': port.name,
               'description': port.description,
               'hwid': port.hwid,
               'vid': port.vid,
               'pid': port.pid,
               'serial_number': port.serial_number,
               'location': port.location,
               'manufacturer': port.manufacturer,
               'product': port.product,
               'interface': port.interface,
            }

    async def run_test_cases(self, include, exclude, tests_list=True, tests_execute=True):
        global exit_code
        tests_passed = True
        include = include or []
        exclude = exclude or []
        if tests_execute:
            self.reader, self.writer = await serial_asyncio.open_serial_connection(
                url=self.usb_port,
                baudrate=self.baudrate,
            )
            self.at = at.AT(
                r=self.reader,
                w=self.writer,
                default_timeout=5,
            )
            try:
                await self.at.TEST.expect_reply(timeout=10)
            except Exception as e:
                logger.error('Hardware did not reply with +TEST acknowledgement')
                logger.error(e)
                exit_code = 1
                return exit_code
        if tests_list:
            logger.info('TESTS LIST:')
        for filename in glob.glob(os.path.join(BASE_DIR, 'tests/**/test*.py'), recursive=True):
            module = importlib.machinery.SourceFileLoader('test', filename).load_module()
            if tests_execute and hasattr(module, 'setup'):
                await module.setup(AT=self.at)
            for func_name in dir(module):
                if func_name.startswith('test') and callable(getattr(module, func_name)):
                    if tests_list:
                        logger.info('%s: %s', os.path.basename(filename), func_name)
                    if not tests_execute:
                        continue
                    skip = False
                    for incl in include:
                        if not re.match(incl, func_name):
                            skip = True
                    for excl in exclude:
                        if re.match(excl, func_name):
                            skip = True
                    if skip:
                        logger.warning('[?] %s skipped', func_name)
                        continue
                    try:
                        await getattr(module, func_name)(AT=self.at)
                    except Exception as e:
                        logger.error('[!] %s error %s', func_name, e)
                        tests_passed = False
                    else:
                        logger.info('[x] %s passed', func_name)
            if tests_execute and hasattr(module, 'teardown'):
                await module.teardown(AT=self.at)
        if not tests_execute:
            exit_code = 0
            return exit_code
        if tests_passed:
            logger.info('All tests passed, good job!')
            exit_code = 0
        else:
            logger.critical('NOTHING WORKS!!!111')
            exit_code = 1
        return exit_code


@click.command()
@click.option('-p', '--port', type=str, help='USB port to open serial to.')
@click.option('-b', '--baudrate', type=int, default=115200, help='Port baudrate.')
@click.option('-i', '--include', multiple=True, help='ONLY execute these test funcs (by func name, regex, multiple).')
@click.option('-x', '--exclude', multiple=True, help='DO NOT execute these test funcs (by func name, regex, multiple).')
@click.option('--tests-list/--no-tests-list', default=True)
@click.option('--tests-execute/--no-tests-execute', default=True)
def main(port, baudrate, include, exclude, tests_list, tests_execute):
    if tests_execute and not port:
        logger.error('--port is required when --tests-execute')
        sys.exit(1)
    runner = SerialTestRunner(usb_port=port, baudrate=baudrate)
    if tests_execute:
        runner.set_nvs_testing_flag()
    asyncio.run(runner.run_test_cases(
        include=include,
        exclude=exclude,
        tests_list=tests_list,
        tests_execute=tests_execute,
    ))

def run_tester():
    global exit_code

    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)-10s %(name)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    test_logs = logging.getLogger('test')
    test_logs.setLevel(logging.DEBUG)
    test_logs.addHandler(handler)

    atlog = logging.getLogger('at')
    atlog.setLevel(logging.DEBUG)
    atlog.addHandler(logging.StreamHandler())

    # monkey-patch Click's sys.exit
    _exit = sys.exit
    sys.exit = lambda x: ...
    try:
        main()
    except Exception as e:
        logger.exception(e)
        exit_code = 1
    sys.exit = _exit

    sys.exit(exit_code)


if __name__ == '__main__':
    run_tester()
