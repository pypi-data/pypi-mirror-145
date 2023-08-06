#!/bin/env python3

import click
import logging
import os
import tempfile
import struct
import sys
import csv
import binascii
import esptool

from .idrc_esp_tools.gen_esp32part import PartitionTable
from .idrc_esp_tools import analyze_nvs


logger = logging.getLogger('configurer')
logger.setLevel(logging.INFO)

BASE_DIR = os.path.dirname(__file__)
TMP_DIR = os.path.join(os.environ['HOME'], '.hwtester')

NVS_TARGET_NAMESPACE = 'ESP-MDF'
exit_code = 0


class SerialDumper:

    def __init__(self, usb_port, baudrate):
        self.usb_port = usb_port
        self.baudrate = baudrate

    def get_nvs(self, nvs_key):

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
            nvs_partition = partition_table.find_by_name('nvs')
            assert nvs_partition, 'NVS partition not found!'
            logger.info('NVS partition @%s len: %s', nvs_partition.offset, nvs_partition.size)

        with tempfile.NamedTemporaryFile(dir=TMP_DIR, suffix='.bin') as f:

            # dump NVS from a running node
            esptool.main([
                '-p',
                self.usb_port,
                'read_flash',
                str(nvs_partition.offset),
                str(nvs_partition.size),
                f.name,
            ])
            logger.info('Dumped NVS partition')

            # get CSV of NVS values
            f.seek(0)
            nvs_data = f.read()
            analyze_nvs.verify_nvs_size(nvs_data)
            analyze_nvs.parse_nvs_binary(nvs_data)
            for line in analyze_nvs.get_nvs_data(only_namespace=NVS_TARGET_NAMESPACE):
                k, data, entry_type, value = line.split(',')
                if k == nvs_key:
                    return binascii.unhexlify(value)


@click.command()
@click.option('-p', '--port', type=str, required=True, help='USB port to open serial to.')
@click.option('-b', '--baudrate', type=int, default=115200, help='Port baudrate.')
def main(
    port,
    baudrate,
):

    runner = SerialDumper(usb_port=port, baudrate=baudrate)
    data = runner.get_nvs('mconfig_data')

    (
        router_ssid,
        router_password,
        router_bssid,
        mesh_id,
        mesh_password,
        mesh_type,
        channel,
        channel_switch_disable,
        router_switch_disable,
        mqtt_uri,
        _,
    ) = struct.unpack(
        '32s' # char router_ssid[32];
        '64s' # char router_password[64];
        '6s' # uint8_t router_bssid[6];
        '6s' # uint8_t mesh_id[6];
        '64s' # char mesh_password[64];
        'B' # mwifi_node_type_t mesh_type;
        'B' # uint8_t channel;
        'B' # uint8_t channel_switch_disable;
        'B' # uint8_t router_switch_disable;
        '128s' # uint8_t custom[32 + 96];
        'H', # uint16_t whitelist_size;
        data[:306]
    )

    mesh_type = {
        0: 'idle',
        1: 'root',
        2: 'node',
        3: 'leaf',
        4: 'sta',
    }.get(mesh_type)

    print('router_ssid =', router_ssid.rstrip(b'\x00').decode())
    print('router_password =', router_password.rstrip(b'\x00').decode())
    print('router_bssid =', binascii.hexlify(router_bssid).decode())
    print('mesh_id =', binascii.hexlify(mesh_id).decode())
    print('mesh_password =', mesh_password.rstrip(b'\x00').decode())
    print('mesh_type =', mesh_type)
    print('channel =', channel)
    print('channel_switch_disable =', channel_switch_disable)
    print('router_switch_disable =', router_switch_disable)
    print('mqtt_uri =', mqtt_uri.rstrip(b'\x00').decode())


def run_dumper():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)-10s %(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    main()


if __name__ == '__main__':
    run_dumper()
