# -*- coding: utf-8 -*-
# @Time   : 2021/11/8 16:11
# @Author : w
"""
自动化 frpc
"""

from multiprocessing import Process

from loguru import logger

from flash.flash_all import Flash
from flash.flash_all import get_devices


def run():
    devices = get_devices()
    logger.info(f"设备个数: {len(devices)}, 设备: {devices}")
    for device in devices:
        alias = 1
        _start = 300
        obj = Flash(device)
        num = _start + alias
        adb_port_begin = 5000 + _start
        p = Process(target=obj.write_frpc_conf(adb_port_begin=adb_port_begin, frida_port_begin=0, alias=alias, num=num))
        p.start()


if __name__ == "__main__":
    run()
