#!/bin/env python3

import click
from serial import Serial
from umodbus.server.serial import get_server
from umodbus.server.serial.rtu import RTUServer


def read_register(slave_id, function_code, address):
    return 42


@click.command()
@click.option("-p", "--port", type=str, required=True, help="Serial port to bind to.")
def main(port):
    s = Serial(port)
    s.timeout = 10
    app = get_server(RTUServer, s)
    app.route_map.add_rule(read_register, slave_ids=list(range(1, 243)), function_codes=[4], addresses=[9, 10, 11])
    try:
        app.serve_forever()
    finally:
        app.shutdown()


def run_modbus_server():
    main()


if __name__ == "__main__":
    run_modbus_server()
