# -*- coding: utf-8 -*-
# @Time   : 2021/10/28 14:01
# @Author : wu
import configparser

config = configparser.ConfigParser()

# config.read("config.ini")
# print(config["DEFAULT"]["ServerAliveInterval"])
# print(config.sections())

from flash.flash_all import AdbClient

flash = AdbClient().devices

pp_flash = print(flash)


# print(pp_flash)

def jujube():
    print('吃枣')
