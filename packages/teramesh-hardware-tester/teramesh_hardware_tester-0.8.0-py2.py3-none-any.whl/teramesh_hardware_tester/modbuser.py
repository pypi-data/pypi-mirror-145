#!/bin/env python3

import asyncio
import click
import logging
import os
import sys

from asciimatics.widgets import (
    Frame,
    ListBox,
    Layout,
    Divider,
    VerticalDivider,
    Text,
    Button,
    TextBox,
    Widget,
    Label,
)
from asciimatics.widgets.utilities import THEMES
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import StopApplication
from collections import defaultdict
from functools import partial

# idrc_esp_tools modules
from .idrc_esp_tools import serial_asyncio, at
from .tester import SerialTestRunner


logger = logging.getLogger("modbuser")
logger.setLevel(logging.INFO)


THEMES["monochrome2"] = defaultdict(
    lambda: (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    {
        "invalid": (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_RED),
        "label": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
        "title": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
        "selected_field": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_BLACK),
        "selected_focus_field": (
            Screen.COLOUR_YELLOW,
            Screen.A_BOLD,
            Screen.COLOUR_BLUE,
        ),
        "focus_button": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_BLUE),
        "selected_focus_control": (
            Screen.COLOUR_YELLOW,
            Screen.A_BOLD,
            Screen.COLOUR_BLUE,
        ),
        "disabled": (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_BLACK),
        "edit_text": (Screen.COLOUR_YELLOW, Screen.A_NORMAL, Screen.COLOUR_BLACK),
        "focus_edit_text": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_BLACK),
    },
)


class ModbusView(Frame):
    """
    Main view.
    """

    def __init__(self, screen, queue):
        super(ModbusView, self).__init__(
            screen,
            screen.height,
            screen.width,
            hover_focus=True,
            can_scroll=False,
            title="Modbus Tester v.0.0.1",
        )
        self.testing_queue = queue

        layout = Layout([10, 1, 81], fill_frame=True)
        self.add_layout(layout)

        self._parity_view = ListBox(
            4,
            [
                ("even", 1),
                ("odd", 2),
                ("none", 3),
            ],
            name="parity",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self._go,
        )
        layout.add_widget(Label("Parity"), 0)
        layout.add_widget(Divider(), 0)
        layout.add_widget(self._parity_view, 0)

        self._function_code_view = ListBox(
            5,
            [
                ("discrete", 1),
                ("coil", 2),
                ("input", 3),
                ("holding", 4),
            ],
            name="function_code",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self._go,
        )
        layout.add_widget(Label("Function"), 0)
        layout.add_widget(Divider(), 0)
        layout.add_widget(self._function_code_view, 0)

        self._word_order_view = ListBox(
            3,
            [
                ("big", 1),
                ("little", 2),
            ],
            name="word_order",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self._go,
        )
        layout.add_widget(Label("Word order"), 0)
        layout.add_widget(Divider(), 0)
        layout.add_widget(self._word_order_view, 0)

        self._byte_order_view = ListBox(
            3,
            [
                ("big", 1),
                ("little", 2),
            ],
            name="byte_order",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self._go,
        )
        layout.add_widget(Label("Byte order"), 0)
        layout.add_widget(Divider(), 0)
        layout.add_widget(self._byte_order_view, 0)

        self._encoding_view = ListBox(
            Widget.FILL_FRAME,
            [
                ("bool", 1),
                ("float", 2),
                ("double", 3),
                ("int8", 4),
                ("int16", 5),
                ("int32", 6),
                ("int64", 7),
                ("uint8", 8),
                ("uint16", 9),
                ("uint32", 10),
                ("uint64", 11),
            ],
            name="encoding",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self._go,
        )
        layout.add_widget(Label("Encoding"), 0)
        layout.add_widget(Divider(), 0)
        layout.add_widget(self._encoding_view, 0)

        layout.add_widget(VerticalDivider(), 1)

        self.data["baudrate"] = "9600"
        self.data["slave"] = "1"
        self.data["register"] = "10000"
        self.data["output"] = ["Output will appear here..."]
        layout.add_widget(Text("Baudrate:", "baudrate"), 2)
        layout.add_widget(Divider(), 2)
        layout.add_widget(Text("Slave ID:", "slave"), 2)
        layout.add_widget(Divider(), 2)
        layout.add_widget(Text("Register:", "register"), 2)
        layout.add_widget(Divider(), 2)
        self.output = TextBox(
            Widget.FILL_FRAME,
            "Output:",
            "output",
            readonly=True,
            line_wrap=True,
        )
        layout.add_widget(self.output, 2)

        divider = Layout([1])
        self.add_layout(divider)
        divider.add_widget(Divider())

        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)

        layout2.add_widget(Button("Test", self._go), 0)
        layout2.add_widget(Button("Quit", self._quit), 3)

        self.set_theme("monochrome2")
        self.fix()

        self._parity_view.value = 3
        self._function_code_view.value = 3
        self._word_order_view.value = 2
        self._byte_order_view.value = 2
        self._encoding_view.value = 10

        self._on_pick()

    def _on_pick(self):
        pass

    def _go(self):
        self.save()
        self.testing_queue.put_nowait(
            (
                # //! slave address: raw value
                int(self.data["slave"]),
                # //! baud rate: raw value (ex: 1200 or 2400 or 4800 or 9600 or 14400 or ...)
                int(self.data["baudrate"]),
                # //! parity: [1 = even][2 = odd][3 = none] (cf. protocol)
                int(self.data["parity"]),
                # //! function code: [1 = discret input][2 = coil][3 = input register][4 =
                # //! holding register] (cf protocol)
                int(self.data["function_code"]),
                # //! register address: raw value
                int(self.data["register"]),
                # //! word/byte order: [1 = big endian][2 = little endian] (cf protocol)
                int(self.data["word_order"]),
                int(self.data["byte_order"]),
                # //! encoding: [1 = bool][2 = float][3 = double][4 = int8][5 = int16][6 =
                # //! int32][7 = int64][8 = uint8][9 = uint16][10 = uint32][11 = uint64] (cf
                # //! protocol)
                int(self.data["encoding"]),
            )
        )

    @staticmethod
    def _quit():
        sys.exit(0)


class ModbuserRunner(SerialTestRunner):
    async def modbusize(self, queue, begin_testing_event, modbus_view):
        self.reader, self.writer = await serial_asyncio.open_serial_connection(
            url=self.usb_port,
            baudrate=self.baudrate,
        )
        self.at = at.AT(
            r=self.reader,
            w=self.writer,
            default_timeout=5,
            log=os.path.join(os.path.abspath(os.getcwd()), "modbus_test.log"),
        )
        try:
            await self.at.TEST.expect_reply(timeout=10)
        except Exception as e:
            logger.error("Hardware did not reply with +TEST acknowledgement")
            logger.error(e)
            sys.exit(1)
        begin_testing_event.set()
        while to_test := await queue.get():
            modbus_view.output.value.append("> AT+TESTMODBUS=" + ",".join(map(str, to_test)))
            modbus_view.output.reset()
            modbus_view.screen.force_update(True)
            modbus_view.screen.draw_next_frame()
            await self.at.TESTMODBUS.set(*to_test)
            try:
                reply = await self.at.TESTMODBUS.expect_reply(timeout=5)
                modbus_view.output.value.append("< " + reply.strip())
            except Exception as e:
                modbus_view.output.value.append("< ERROR: " + str(e))
            modbus_view.output.reset()
            modbus_view.screen.force_update(True)
            modbus_view.screen.draw_next_frame()


def global_shortcuts(event):
    if isinstance(event, KeyboardEvent):
        c = event.key_code
        # Stop on Ctrl+Q
        if c in [Screen.ctrl("Q"), Screen.ctrl("q")]:
            raise StopApplication("User terminated app")


async def screen_loop(screen, port, baudrate):
    testing_queue = asyncio.Queue()
    modbus_view = ModbusView(screen, testing_queue)
    screen.set_scenes(
        [
            Scene([modbus_view], -1, name="Main"),
        ],
        unhandled_input=global_shortcuts,
    )
    runner = ModbuserRunner(usb_port=port, baudrate=baudrate)
    runner.set_nvs_testing_flag()
    begin_testing_event = asyncio.Event()
    asyncio.create_task(runner.modbusize(testing_queue, begin_testing_event, modbus_view))
    await begin_testing_event.wait()
    while True:
        modbus_view.output.reset()
        screen.draw_next_frame()
        await asyncio.sleep(0.02)


def modbusizer_ui(port, baudrate, screen):
    asyncio.run(screen_loop(screen, port, baudrate))


@click.command()
@click.option("-p", "--port", type=str, help="USB port to open serial to.")
@click.option("-b", "--baudrate", type=int, default=115200, help="Port baudrate.")
def main(port, baudrate):
    Screen.wrapper(partial(modbusizer_ui, port, baudrate))


def run_modbuser():
    main()


if __name__ == "__main__":
    run_modbuser()
