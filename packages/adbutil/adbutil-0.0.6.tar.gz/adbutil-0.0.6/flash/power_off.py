# -*- coding: utf-8 -*-
# @Time   : 2021/1/20 下午2:36
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
        p = Process(target=obj.power_off)
        p.start()


if __name__ == "__main__":
    run()
