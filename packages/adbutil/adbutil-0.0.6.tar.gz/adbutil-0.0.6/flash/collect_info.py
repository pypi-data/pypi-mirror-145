# -*- coding: utf-8 -*-
# @Time   : 2021/1/20 下午12:52
# @Author : wu


from flash.flash_all import BaseRun


class Run(BaseRun):
    def run(self):
        for device in self.devices:
            obj = self.Flash(device)
            p = self.Process(
                target=obj.collect_info,
            )
            p.start()


if __name__ == "__main__":
    Run().run()
