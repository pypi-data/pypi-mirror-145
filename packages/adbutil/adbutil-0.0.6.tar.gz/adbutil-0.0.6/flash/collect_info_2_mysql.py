# -*- coding: utf-8 -*-
# @Time   : 2021/1/26 下午3:42
# @Author : wu
"""
pip install sqlalchemy

收集手机参数并写入 mysql，主要是收集 mac 地址和设备编号的关系，以配置静态 ip
"""
import json

import pymysql
from sqlalchemy.ext.declarative import declarative_base

from flash.flash_all import BaseRun
from flash.sqlalchemy_cli import SqlAlchemy
from models.local_devices import LocalDevice

sqlalchemy_obj = SqlAlchemy()

Base = declarative_base()


class Run(BaseRun):
    def run(self):
        infos = []
        for device in self.devices:
            obj = self.Flash(device)
            res = self.pool.apply_async(obj.collect_info, args=(True,))
            infos.append(res)
        self.pool.close()
        self.pool.join()

        self.save2mysql(infos)

    def run_single(self):
        if not self.devices:
            self.logger.info("no devices")
            return
        device = self.devices[0]
        obj = self.Flash(device)
        res = self.pool.apply_async(obj.collect_info, args=(False,))

        self.pool.close()
        self.pool.join()
        # self.save2mysql([res])

    def save2mysql(self, infos, is_create_table=False):
        if is_create_table:
            sqlalchemy_obj.create_table(Base)
        datas = []
        for info in infos:
            info = info.get()
            keys = [
                "android_id",
                "imei",
                "mac",
                "os_version",
                "sdk",
                "brand",
                "model",
                "manufacturer",
                "sw",
                "sh",
                "serialno",
                "product",
                "fingerprint",
                "sys_compiling_time",
                "sys_compiling_time_utc",
                "timezone",
                "bluetooth_mac",
                "hardware",
                "ks_did",
            ]

            item = {_key: info[_key] for _key in keys if info.get(_key)}
            item["infos"] = json.dumps(info)
            number = "65"  # 根据编号来修改
            item["num"] = int(number)
            item["name"] = f"PX-{number}"
            data = LocalDevice(**item)
            datas.append(data)
            self.write2db(data, item)

    def write2db(self, data, item):
        try:
            # sqlalchemy_obj.insert(LocalDevice, item)  # 允许覆盖插入
            sqlalchemy_obj.add_new(data)  # 不允许覆盖插入
            pass
        except pymysql.err.IntegrityError as e:
            sqlalchemy_obj.del_data(LocalDevice.name.in_(item["name"]))
            sqlalchemy_obj.add_new([data])
        self.logger.success(f'设备: {item["name"]}, mysql 写入成功')


if __name__ == "__main__":
    Run().run_single()
