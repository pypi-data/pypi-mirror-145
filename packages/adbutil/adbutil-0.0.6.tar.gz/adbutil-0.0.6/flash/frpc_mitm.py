# -*- coding: utf-8 -*-
# @Time   : 2021/11/4 18:31
# @Author : w

from multiprocessing import Process

from loguru import logger

from flash.flash_all import Flash, AdbClient


def run():
    adb = AdbClient()
    devices = adb.devices
    logger.info(f"设备个数: {len(devices)}, 设备: {devices}")
    for device in devices:
        obj = Flash(device)
        alias = 12
        num = 200 + alias
        p = Process(target=obj.write_frpc_conf(adb_port_begin=5200, frida_port_begin=0, alias=alias, num=num))
        p.start()


if __name__ == "__main__":
    run()
