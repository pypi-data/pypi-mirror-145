# -*- coding: utf-8 -*-
# @Time   : 2021/1/20 下午2:36
# @Author : wu

"""
把证书推到系统信任目录

值得注意的是：
1. mitmproxy/fiddler，不同设备导出来的证书转出来的 hash 值都是一样的，至少我试了几个都是c8750f0d。如果我们都是保存为 c8750f0d.0，那应该只有一台电脑是能信任，其他都不行。
因此我们需要分别命名为 c8750f0d.1、c8750f0d.2...

2. 如果是 fidller 导出的证书，没有 pem 格式，一般是 crt 格式需要转换下
openssl x509 -in fiddlerRootCertificate.crt -inform DER -out fiddlerRootCertificate.pem -outform PEM

trans_pem.sh
```bash
# bin/bash

# pem 转为 hash 文件

num=0
if [ -n "$2" ] ;then
    num=$2
fi

echo `openssl x509 -subject_hash_old -in $1` | awk -va=.$num '{print $1a}' | xargs  -I {} cp $1 {}
```
"""
import os
import re

from loguru import logger

from flash.flash_all import PEM_BASH_PATH
from flash.flash_all import BaseRun
from flash.flash_all import Flash


def end_num(string):
    # 以一个数字结尾字符串
    text = re.compile(r".*[0-9]$")
    return text.match(string)


def get_pems_without_mitm(is_gen_pem=False):
    if is_gen_pem:
        Flash.execute(f"cd {PEM_BASH_PATH} &&  for pem in `ls | grep '\.pem' |uniq`;do sh trans_pem.sh $pem; done")
    files = [file for file in os.listdir(PEM_BASH_PATH) if file.endswith(".0")]
    return files


def get_pems(is_gen_pem=False):
    if is_gen_pem:
        mitm_pems = []
        fiddler_mitm_pems = []
        charles_mitm_pems = []
        http_canary_pems = []
        pems = [file for file in os.listdir(PEM_BASH_PATH) if ".pem" in file]
        for pem in pems:
            # mitmproxy 和 fiddler 的证书，不同设备导出证书转出来的 hash 值都是一样的，至少我试了几个都是c8750f0d。
            # 如果我们都是保存为 c8750f0d.0。那应该只有一台电脑是能信任，其他都不行。
            # 因此我们需要分别命名为 c8750f0d.1、c8750f0d.2...
            if "mitm" in pem or "mitmproxy" in pem:
                mitm_pems.append(pem)
            elif "fiddler" in pem:
                fiddler_mitm_pems.append(pem)
            elif "HttpCanary" in pem or "httpCanary" in pem:
                http_canary_pems.append(pem)
            else:
                charles_mitm_pems.append(pem)
        for i, pem in enumerate(charles_mitm_pems):
            Flash.execute(f"cd {PEM_BASH_PATH} && sh trans_pem.sh {pem} ")
        for i, pem in enumerate(mitm_pems):
            Flash.execute(f"cd {PEM_BASH_PATH} && sh trans_pem.sh {pem} {i} ")
        for i, pem in enumerate(fiddler_mitm_pems):
            Flash.execute(f"cd {PEM_BASH_PATH} && sh trans_pem.sh {pem} {i} ")
        for i, pem in enumerate(http_canary_pems):
            Flash.execute(f"cd {PEM_BASH_PATH} && sh trans_pem.sh {pem} {i} ")
    files = [file for file in os.listdir(PEM_BASH_PATH) if end_num(file)]
    return files


class Run(BaseRun):
    def run(self):
        for device in self.devices:
            obj = self.Flash(device)
            pems = get_pems(True)
            logger.info(f"证书数量：{len(pems)}")
            p = self.Process(target=obj.push_pem_to_system, args=(pems, False, False))
            p.start()


if __name__ == "__main__":
    Run().run()
