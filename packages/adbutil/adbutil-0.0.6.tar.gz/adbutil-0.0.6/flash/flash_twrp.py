"""
刷入 twrp，即 recovery
然后刷 magisk 以及 magisk module
"""

from flash.flash_all import BaseRun


class Run(BaseRun):
    def run(self):
        for device in self.devices:
            obj = self.Flash(device)
            p = self.Process(target=obj.flash)
            p.start()


if __name__ == "__main__":
    Run().run()
