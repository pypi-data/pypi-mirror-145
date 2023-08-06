# -*- coding: utf-8 -*-
# @Time   : 2021/1/20 下午3:25
# @Author : wu

from flash.flash_all import BaseRun


def get_magisk_modules():
    # modules = ["Move_Certificates-v1.9.zip", "magisk-frida-12.11.zip", "adbd-v0.4.zip"]
    # modules = ["frida-12.11.zip", "adbd-v0.4.zip", "busybox-ndkr.zip",]
    modules = [
        # "Magisk-v21.1.zip",
        # "Move-Certificates-v1.9.zip",
        # "adbd.zip",
        # "frida-12.11-dev.zip",
        # "busybox-ndkr.zip",
        # "autofix.zip",
        # 'SSH_for_Magisk-v0.10'
    ]
    # modules = ["Magisk-v21.1.zip",]

    return modules


class Run(BaseRun):
    def run(self):
        for device in self.devices:
            obj = self.Flash(device)
            p = self.Process(target=obj.flash_magisk_module, args=(get_magisk_modules(),))
            p.start()


if __name__ == "__main__":
    Run().run()
