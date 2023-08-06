# -*- coding: utf-8 -*-
# @Time   : 2021/3/2 上午11:36
# @Author : wu

"""
设备相关设备，例如禁止屏幕旋转，显示电量百分比
"""

from flash.flash_all import BaseRun


class Run(BaseRun):
    def run(self):
        for device in self.devices:
            obj = self.Flash(device)
            p = self.Process(target=obj.device_setting, args=())
            p.start()


if __name__ == "__main__":
    Run().run()
