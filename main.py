#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""PySerial test example"""

from datetime import datetime as dt
import time

import serial

SLEEP_T = 0.1
TEST_NAME = 'csv_test'
FIELDS_NAMES = ['Time', 'tLM35', 'T6675', 'ANALOG']

def open_next_file(f):
    """ Close old file and open new one"""
    if f is not None:
        if not f.closed:
            f.close()
    f = open(f'{TEST_NAME}_{dt.now():%Y%m%d_%H%M%S}.txt', 'w', encoding="utf-8")
    return f

ser = serial.Serial(port = '/dev/tty.usbserial-A5XK3RJT'
    , baudrate = 9600
    # , baudrate = 57600
    , timeout = 0.1
    )
# ser.open()
time.sleep(SLEEP_T)

f_time = dt.now()
probe_start_time = dt.now()
dict2save = {}
f = open_next_file(None)

while ser.is_open and (dt.now()-probe_start_time).seconds < 10800:
    if (dt.now()-f_time).seconds > 600:
        f_time = dt.now()
        f = open_next_file(f)

    while ser.in_waiting == 0:
        time.sleep(SLEEP_T)
    while ser.in_waiting > 0:
        buf_b = ser.read_until()
        try:
            byte2str = buf_b.decode("utf-8")
            f.write(byte2str)
        except UnicodeDecodeError as ex:
            print(f'UnicodeDecodeError except: {ex}\n\t buf: {buf_b}')

    print(f'{byte2str}')
    # time.sleep(5)

if not f.closed:
    f.close()
ser.close()
