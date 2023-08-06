# -*- coding: utf-8 -*-
# @Time   : 2021/10/28 14:42
# @Author : wu


from multiprocessing import Process

from loguru import logger

from flash.flash_all import Flash
from flash.flash_all import get_devices


def run():
    devices = get_devices()
    logger.info(f"设备个数: {len(devices)}, 设备: {devices}")
    for device in devices:
        obj = Flash(device)
        p = Process(target=obj.push_something("tmp/7fec8a38-2197-4d7b-a4e9-7b17a94c42da.ini"))
        p.start()


if __name__ == "__main__":
    run()
