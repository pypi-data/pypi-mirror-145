"""
frps.ini

[common]
bind_port = 17000
authentication_method = token
token = kingsmanv2

执行完该脚本，将 frpc.ini 写入 /data/frp 目录下后，需要把 frpc.zip 模块安装到 magisk 中，然后重启手机即可
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
        alias = 7
        p = Process(target=obj.write_frpc_conf(alias=alias))
        p.start()


if __name__ == "__main__":
    run()
