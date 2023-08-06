# -*- coding: utf-8 -*-
# @Time   : 2021/1/20 下午2:36
# @Author : wu

"""
如果已经在 magisk 上装了 Move Certificates，就直接跑这个模块，不需要再直接推入到系统
把证书推到用户信任目录
"""

from loguru import logger

from flash.flash_all import BaseRun

from flash.push_certificate_to_system import get_pems


class Run(BaseRun):
    def run(self):
        pems = get_pems(True)
        logger.info(f"证书数量：{len(pems)}")
        for device in self.devices:
            obj = self.Flash(device)
            p = self.Process(target=obj.push_pem_to_user, args=(pems, False))
            p.start()


if __name__ == "__main__":
    Run().run()
