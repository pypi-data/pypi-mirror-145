""" module:: dlt.serial_port
    :synopsis: A Serial Port as a source for dlt.
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""

from threading import Thread
from typing import Optional
from warnings import warn

from serial import Serial

from dlt.protocol import parse_dlt_record, DLT_MAGIC_SERIAL

import logging

LOGGER = logging.getLogger(__name__)

DLT_STD_BAUDRATES = [115200,
                     500000,
                     921600]


class SerialStreamHandler:
    """
    A handler for a dlt stream on a serial port.
    """

    def __init__(self,
                 port: Optional[str] = None,
                 baudrate: Optional[int] = None,
                 ser: Optional[Serial] = None,
                 ):
        """
        Constructor. Either pass port and baudrate or a serial object to it.
        :param port: The port device, e.g. "/dev/ttyUSB0" on linux or "com10" on windows
        :param baudrate: The baudrate of the serial port.
        :param ser: The serial connection.
        NOTE: It is recommended to set devices by udev rule to distinct names and prevent swapping serial ports.
              Or to use /dev/serial/by-id/... method.
        """

        self.listeners = []
        self.port = port
        if (baudrate is not None) and (baudrate not in DLT_STD_BAUDRATES):
            warn("{0} is not a standard baudrate".format(baudrate))
        self.baudrate = baudrate
        self.ser = ser or Serial(port=self.port,
                                 baudrate=self.baudrate,
                                 timeout=0.1)

        self.rx_handler = Thread(target=self.handle_rx)
        self.rx_handler.setDaemon(True)
        self.rx_handler.start()

    def handle_rx(self) -> None:
        """
        The rx thread. It loops over the serial buffer and self.handle() to handle the received record.
        :return: Nothing.
        """
        buffer = bytearray()
        with self.ser:
            while True:
                data = self.ser.read(1)
                if data:
                    buffer.extend(data)
                    buffer.extend(self.ser.read(self.ser.inWaiting()))
                    if not buffer.startswith(DLT_MAGIC_SERIAL) and DLT_MAGIC_SERIAL in buffer:
                        # sync to the next DLT_MAGIC_SERIAL
                        buffer = bytearray(buffer[buffer.index(DLT_MAGIC_SERIAL):])
                    try:
                        record = parse_dlt_record(buffer[len(DLT_MAGIC_SERIAL):])
                    except (ValueError, NotImplementedError):
                        pass
                    else:
                        # strip the dlt magic from the front and resync on next marker
                        record_length = record.pop("record_length")
                        buffer = bytearray(buffer[len(DLT_MAGIC_SERIAL)+record_length:])
                        self.handle(record=record)

    def handle(self, record):
        """
        Handle a received record.
        :param record: A parsed dlt record.
        :return: Nothing.
        """
        for listener in self.listeners:
            listener(record)

    def register_listener(self, callback: callable) -> None:
        """
        Register a listener function for the received dlt record.
        :param callback: The callback. It must have one argument of type dictionary.
        :return: Nothing.
        """
        self.listeners.append(callback)

    def unregister_listener(self, callback: callable) -> None:
        """
        Unregister a previously listener function.
        :param callback: The callback.
        :return: Nothing
        """
        if callback in self.listeners:
            self.listeners.remove(callback)
