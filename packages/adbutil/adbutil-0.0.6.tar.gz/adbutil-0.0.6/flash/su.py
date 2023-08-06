# -*- coding: utf-8 -*-
# @Time   : 2021/1/21 上午11:31
# @Author : wu


"""
获取 root 权限，目的是让 magisk 的 出现 shell 的超级用户权限授权
"""
from multiprocessing import Process

from loguru import logger

from flash.flash_all import Flash
from flash.flash_all import get_devices


def run():
    devices = get_devices()
    logger.info(f"设备个数: {len(devices)}, 设备: {devices}")
    for device in devices:
        obj = Flash(device)
        p = Process(target=obj.su)
        p.start()


if __name__ == "__main__":
    run()
