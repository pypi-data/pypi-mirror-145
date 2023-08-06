# -*- coding: utf-8 -*-
# @Time   : 2021/1/20 下午12:52
# @Author : wu

"""
安装 app
"""

from flash.flash_all import BaseRun, AdbClient


def get_apps():
    apps = [
        "proxy-setter-debug-0.2.1.apk"
        # "proxydroid-3.2.0.apk",  # 代理机器人，这样设置代理更方便，而且可以保存多个代理配置
        # "ks_8.3.apk",
        # "taobaolive__com.taobao.live__1.7.1__41.apk",
        # "xhs_676.apk",
        # "huoshanv900.apk",
        # "com.tencent.weishi.apk",
        # "douyin_v1250.apk",
    ]
    apps1 = [
        "qzone__com.qzone__8.4.3.288__125.apk",
        "qq__com.tencent.mobileqq__8.1.0__1232.apk",
        "wechat__com.tencent.mm__7.0.22__1820.apk",
    ]
    # apps.extend(apps1)
    return apps


class Run(BaseRun):
    def run(self):
        adb = AdbClient()
        for device in adb.devices:
            # print(device.serial)
            obj = self.Flash(device)
            p = self.Process(target=obj.install_app, args=(get_apps(),))
            p.start()


if __name__ == "__main__":
    Run().run()
