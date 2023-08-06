#!/bin/env python3

import click
import logging
import os
import subprocess
import tempfile
import struct
import sys
import hashlib
import esptool

from .idrc_esp_tools.gen_esp32part import PartitionTable


logger = logging.getLogger('configurer')
logger.setLevel(logging.INFO)

BASE_DIR = os.path.dirname(__file__)
TMP_DIR = os.path.join(os.environ['HOME'], '.hwtester')

NVS_TARGET_NAMESPACE = 'ESP-MDF'
exit_code = 0


class SerialConfigurator:

    def __init__(self, usb_port, baudrate):
        self.usb_port = usb_port
        self.baudrate = baudrate

    def generate_nvs(self, nvs_items=None):

        nvs_items = nvs_items or []

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

        with tempfile.NamedTemporaryFile(dir=TMP_DIR, mode='wt', suffix='.csv') as csv_out:

            # generate CSV
            csv_out.write('key,type,encoding,value\n')
            csv_out.write(f'{NVS_TARGET_NAMESPACE},namespace,,\n')
            for item in nvs_items:
                csv_out.write(f'{item["key"]},data,{item["encoding"]},{item["value"]}\n')
            csv_out.flush()

            with tempfile.NamedTemporaryFile(dir=TMP_DIR, suffix='.bin') as nvs_partition_out:

                # generate partition
                p = subprocess.run([
                    'python3',
                    os.path.join(BASE_DIR, 'idrc_esp_tools/nvs_partition_gen.py'),
                    'generate',
                    csv_out.name,
                    nvs_partition_out.name,
                    str(nvs_partition.size),
                ], capture_output=True, text=True)
                if p.stderr:
                    logger.warning(p.stderr)
                p.check_returncode()
                logger.info('Generated new NVS partition')

                # flash NVS partition
                esptool.main([
                    '-p',
                    self.usb_port,
                    'write_flash',
                    str(nvs_partition.offset),
                    nvs_partition_out.name,
                ])
                logger.info('Flashed new NVS partition')

        logger.info('Ready!')


@click.command()
@click.option('-p', '--port', type=str, required=True, help='USB port to open serial to.')
@click.option('-b', '--baudrate', type=int, default=115200, help='Port baudrate.')
@click.option('--router-ssid', type=str, required=True, help='')
@click.option('--router-password', type=str, required=True, help='')
@click.option('--router-bssid', type=str, default='0' * 12, help='')
@click.option('--mesh-id', type=str, required=True, help='')
@click.option('--mesh-password', type=str, required=True, help='')
@click.option('--mesh-type', type=str, default='idle', help='')
@click.option('--channel', type=int, default=0, help='')
@click.option('--channel-switch-disable/--no-channel-switch-disable', default=False)
@click.option('--router-switch-disable/--no-router-switch-disable', default=False)
@click.option('--mqtt-uri', type=str, required=True, help='')
def main(
    port,
    baudrate,
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
):
    if len(router_ssid) > 32:
        raise click.BadParameter('router_ssid must be shorter than 32 characters!')
    if len(router_password) > 64:
        raise click.BadParameter('router_password must be shorter than 64 characters!')
    if len(mesh_password) > 64:
        raise click.BadParameter('mesh_password must be shorter than 64 characters!')
    try:
        _router_bssid = int(router_bssid, 16)
    except Exception:
        raise click.BadParameter('router_bssid is invalid')
    try:
        _mesh_id = int(mesh_id, 16)
    except Exception:
        raise click.BadParameter('mesh_id is invalid')

    if len(mesh_password) == 63:
        encoded_mesh_password = mesh_password
    else:
        ap_sha256 = list(hashlib.sha256(router_password.encode()).digest())
        mesh_sha256 = list(hashlib.sha256(mesh_password.encode()).digest())
        encoded_mesh_password = ['0'] * 64
        for i in range(32):
            mesh_sha256[i] ^= ap_sha256[i]
            tmp = ((mesh_sha256[i] & 0xf0) >> 4) + ord(b'0')
            encoded_mesh_password[2 * i] = chr(tmp + ord(b'A') - ord(b'9') if tmp > ord(b'9') else tmp)
            tmp = (mesh_sha256[i] & 0x0f) + ord(b'0')
            encoded_mesh_password[2 * i + 1] = chr(tmp + ord(b'A') - ord(b'9') if tmp > ord(b'9') else tmp)
        encoded_mesh_password = ''.join(encoded_mesh_password)[:63]

    print(f'''
port = {port}
baudrate = {baudrate}
router_ssid = {router_ssid}
router_password = {router_password}
router_bssid = {router_bssid}
mesh_id = {mesh_id}
mesh_password = {mesh_password}
encoded_mesh_password = {encoded_mesh_password}
mesh_type = {mesh_type}
channel = {channel}
channel_switch_disable = {channel_switch_disable}
router_switch_disable = {router_switch_disable}
mqtt_uri = {mqtt_uri}
    ''')

    '''
    typedef enum {
        MWIFI_MESH_IDLE,
        MWIFI_MESH_ROOT,
        MWIFI_MESH_NODE,
        MWIFI_MESH_LEAF,
        MWIFI_MESH_STA,
    } node_type_t;

    typedef uint8_t mwifi_node_type_t;

    typedef struct {
        char router_ssid[32];
        char router_password[64];
        uint8_t router_bssid[6];
        uint8_t mesh_id[6];
        char mesh_password[64];
        mwifi_node_type_t mesh_type;
        uint8_t channel;
        uint8_t channel_switch_disable;
        uint8_t router_switch_disable;
    } mwifi_config_t;

    typedef struct {
        mwifi_config_t config;
        uint8_t custom[32 + 96];
        uint16_t whitelist_size;
        mconfig_whitelist_t whitelist_data[0];
    } __attribute__((packed)) mconfig_data_t;
    '''

    data = struct.pack(
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
        'H' # uint16_t whitelist_size;
        '', # mconfig_whitelist_t whitelist_data[0]; - NOT SUPPORTED
        router_ssid.encode(), # char router_ssid[32];
        router_password.encode(), # char router_password[64];
        _router_bssid.to_bytes(6, 'big'), # uint8_t router_bssid[6];
        _mesh_id.to_bytes(6, 'big'), # uint8_t mesh_id[6];
        mesh_password.encode(), # char mesh_password[64];
        {
            'idle': 0,
            'root': 1,
            'node': 2,
            'leaf': 3,
            'sta': 4,
        }.get(mesh_type), # mwifi_node_type_t mesh_type;
        channel, # uint8_t channel;
        int(channel_switch_disable), # uint8_t channel_switch_disable;
        int(router_switch_disable), # uint8_t router_switch_disable;
        mqtt_uri.encode(), # uint8_t custom[32 + 96];
        0, # uint16_t whitelist_size;
    )

    runner = SerialConfigurator(usb_port=port, baudrate=baudrate)
    runner.generate_nvs([
        {
            'key': 'mconfig_data',
            'encoding': 'hex2bin',
            'value': data.hex(),
        }
    ])


def _main():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)-10s %(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    main()


def run_configurer():
    os.makedirs(TMP_DIR, exist_ok=True)
    _main()


if __name__ == '__main__':
    run_configurer()
