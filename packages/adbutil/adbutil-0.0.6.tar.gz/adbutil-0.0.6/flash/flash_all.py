# -*- coding: utf-8 -*-
# @Time   : 2021/1/20 下午1:53
# @Author : wu

"""
批量刷机，这些工作应该在一开始就完善好

pixel 1代刷机，包括（前4个步骤应该是按顺序来，之所以要先给 shell 授权超级用户，是因为有些操作需要有 su 权限）

1. 刷入系统，下载地址: https://developers.google.com/android/images#crosshatch（需要手动设置一些开机选项）
2. 刷入 twrp，下载地址: https://twrp.me/Devices/
3. 刷入 magisk 和 magisk 相关模块
4. 授权 magisk 的 shell 超级用户权限（执行 su.sh，然后 magisk 会弹出是否允许授权，手动允许即可
5. 批量安装 app
6. 批量把证书推到系统/用户证书目录下
7. 设备相关设置，包括设置日期（有时候代理不生效就是日期的问题）、授权 ag02 的 adb、设备禁止自动旋转屏幕、显示电量百分比

待完善....

pip install loguru
"""
from datetime import datetime
import json
import multiprocessing
from multiprocessing import Pool
from multiprocessing import Process
import os
import platform
import re
import subprocess
import time
import uuid

from loguru import logger

BASE_PATH = "/Users/wu/Work/android-auto"

MAGISK_BASH_PATH = f"{BASE_PATH}/Magisk"

IMG_BASH_PATH = f"{BASE_PATH}/pixel"
OnePlus_IMG_BASH_PATH = f"{BASE_PATH}/OnePlus5"

APK_BASH_PATH = f"{BASE_PATH}/my_apks"

PEM_BASH_PATH = f"{BASE_PATH}/pems"

BUSUYBOX_BASH_PATH = "/Users/wu/Work/android-auto"

ADB = "/usr/local/bin/adb"
FASTBOOT = "/usr/local/bin/fastboot"


def remount(self, func):
    def wrapper(*args, **kw):
        self.adb_shell(f"shell su -c 'mount -o remount,rw / ; '")
        call = func(*args, **kw)
        self.adb_shell(f"shell su -c 'mount -o ro,remount /'")
        return call

    return wrapper


class ShellMixin(object):
    platform = platform.system()

    @staticmethod
    def shell(cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        result, err = p.communicate()
        return result.decode("utf-8") if result.decode("utf-8") != "null" else None

    def sed_execute(self, cmd):
        if self.platform == "Linux":
            cmd = f"sed -i {cmd}"
        elif self.platform == "Darwin":
            cmd = f"sed -i '' {cmd}"
        else:
            raise OSError("Windows 平台请自己补充 sed 用法")

        return self.shell(cmd)

    @staticmethod
    def call(cmd, **kwargs) -> bool:
        """非阻塞调用subprocess.call()，执行且只返回命令结果，成功为True失败为False
        :param cmd:
        :param kwargs: subprocess.check_call kwargs, may be timeout=seconds
        :return:
        """

        # 不设置timeout，非阻塞
        try:
            flag = subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, **kwargs)
        except subprocess.CalledProcessError as e:
            flag = e.returncode
        except subprocess.TimeoutExpired as e:
            flag = 1

        return True if flag == 0 else False


class AdbClient:
    @property
    def devices(self):
        fastboot_devices = os.popen(f"{FASTBOOT} devices | grep -v offline | grep -v emulator").read().split("\r")[1:]
        adb_devices = os.popen(f"{ADB} devices | grep -v offline | grep -v emulator").read().split("\n")[1:]
        _devices = [d.split("\t")[0] for d in fastboot_devices + adb_devices if d]
        _devices = [AdbDevice(serial) for serial in _devices]

        return _devices


class AdbDevice(ShellMixin):
    def __init__(self, serial: str):
        # self._client = client
        self._serial = serial
        self._properties = {}  # store properties data

    def adb_shell(self, cmd):
        if not cmd.startswith("adb -s") and not cmd.startswith("fastboot"):
            cmd = f"{ADB} -s {self.serial} {cmd}"
        return self.shell(cmd)

    @property
    def serial(self):
        return self._serial

    @property
    def model(self):
        return self.adb_shell("shell getprop ro.product.model").strip()

    def __repr__(self):
        return f"AdbDevice(serial={self.serial})"


class Flash:
    def __init__(self, device):
        self.device = device
        self.device_name = device.serial
        self.model = self.adb_shell("shell getprop ro.product.model").strip()

    def __getitem__(self, key):
        return self.__dict__.get(key)

    @staticmethod
    def shell(cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        result, err = p.communicate()
        return result.decode("utf-8") if result.decode("utf-8") != "null" else None

    def adb_shell(self, cmd):
        if not cmd.startswith("adb -s") and not cmd.startswith("fastboot"):
            cmd = f"{ADB} -s {self.device_name} {cmd}"
        return self.shell(cmd)

    def sed_execute(self, cmd):
        if self.device.platform == "Linux":
            cmd = f"sed -i {cmd}"
        elif self.device.platform == "Darwin":
            cmd = f"sed -i '' {cmd}"
        else:
            raise OSError("Windows 平台请自己补充 sed 用法")

        return self.shell(cmd)

    @staticmethod
    def call(cmd, **kwargs) -> bool:
        """非阻塞调用subprocess.call()，执行且只返回命令结果，成功为True失败为False
        :param cmd:
        :param kwargs: subprocess.check_call kwargs, may be timeout=seconds
        :return:
        """

        # 不设置timeout，非阻塞
        try:
            flag = subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, **kwargs)
        except subprocess.CalledProcessError as e:
            flag = e.returncode
        except subprocess.TimeoutExpired as e:
            flag = 1

        return True if flag == 0 else False

    def wait_device(self, message=None):
        """
        等待设备
        Args:
            message: 需要打印的信息
        Returns:

        """
        if message:
            logger.info(f"设备 {self.device_name} {message}")
        while True:
            try:
                res = os.popen(f"{ADB} devices| grep {self.device_name}").read()
                if self.device_name in res:
                    break
            except Exception as e:
                logger.error(e)
            time.sleep(1)

    def side_load_mod(self):
        """
        进入 side load 模式
        刷 zip 包之前需要进入该模式
        """
        self.adb_shell(f"shell twrp sideload")
        self.wait_device()

    def flash_twrp(self):
        """
        刷入第三方 twrp
        Returns:

        """
        if self.model == "ONEPLUS A5000":
            self.shell(
                f"{FASTBOOT} -s {self.device_name} flash recovery {OnePlus_IMG_BASH_PATH}/twrp-3.2.3-0-cheeseburger.img"
            )
            self.shell(f"{FASTBOOT} -s {self.device_name} reboot")
            self.wait_device("重启中，准备进入 recovery 模式")
            self.in_recovery_mod()
            return
        img_file = {
            "Pixel": "pixel-twrp-3.3.0-0-sailfish.img",
            "Pixel 3": "twrp-pixel3-3.3.0-0-blueline.img",
        }
        zip_file = {
            "Pixel": "pixel-twrp-sailfish-3.3.0-0.zip",
            "Pixel 3": "twrp-pixel3-installer-blueline-3.3.0-0.zip",
        }
        flash_twrp_img = f"{FASTBOOT} -s {self.device_name} boot {IMG_BASH_PATH}/{img_file[self.model]}"
        self.shell(flash_twrp_img)
        self.wait_device("刷入 twrp img 临时镜像")
        # 会重启，自动进入 recovery 模式
        # 进入 sideload 模式
        self.side_load_mod()
        flash_twrp_zip = f"sideload {IMG_BASH_PATH}/{zip_file[self.model]}"
        self.adb_shell(flash_twrp_zip)
        self.wait_device("刷入 twrp zip 永久镜像")

    def flash_magisk(self, magisk="Magisk-v21.1.zip"):
        """
        刷入 magisk zip 包，即 magisk app
        Args:
            magisk: magisk 模块名字
        Returns:

        """
        self.wait_device()
        self.side_load_mod()
        self.adb_shell(f"sideload {MAGISK_BASH_PATH}/{magisk}")
        self.wait_device("刷入 Magisk")

    def flash_magisk_module(self, modules: list = None, only_flash_this: bool = True):
        """
        刷入 magisk 下的模块，在 recovery 模式下与 magisk.zip 包的方式是一样的
        当然我们也可以通过先把模块推到手机的 /sdcard，然后在 magisk app 手动刷入
        Args:
            modules: magisk 模块
            only_flash_this: 表示此次是否单独刷入该此模块内容，是的话，需要先进入 reovery 模式；而如果是全部刷的话，
                             可能本身已经处于 recovery 模式了。一般我们也是只会重刷 magisk 模块，像 magisk app 在刷 twrp 会一并刷好了。
                             如果仅仅是想升级 magisk app，也是可以通过刷模块的方式来升级的
        Returns:

        """
        if only_flash_this:
            self.in_recovery_mod()
        self.wait_device("进入 recovery 模式中，准备刷入 magisk modules")

        if not modules:
            modules = [
                "Magisk-v21.1.zip",
                "Move-Certificates-v1.9.zip",  # 证书
                "adbd.zip",  # 华为云的 adbd，自动开启 tcpid
                "frida-12.11-dev.zip",  # 目前用的是 12 版本，14版本在淘宝直播貌似有点问题
                "frida-12.11.zip",  # 目前用的是 12 版本，14版本在淘宝直播貌似有点问题
                "busybox-ndkr.zip",  # 提供的一些 linux 相关命令
                "frpc.zip",  # 提供的一些 linux 相关命令
                # "autofix.zip",  # 自动修复一些异常，注意，这里写了个逻辑，如果连不上网，则会自动重启
                # "HidePropsConf.zip",
                # "Riru-v25.4.4.zip",
                # "Riru-EdXpose-0.5.2.2.zip",
            ]
        for module in modules:
            while True:
                _file = f"{MAGISK_BASH_PATH}/{module}"
                if not os.path.exists(_file):
                    logger.warning(f"{_file} is not exist !!!")
                    break
                self.side_load_mod()
                res = self.adb_shell(f"sideload {_file}")
                self.wait_device()
                if "Total xfer" in res:
                    self.wait_device(f"成功刷入 Magisk 模块: {module}")
                    break
        if only_flash_this:
            self.reboot()

    def in_recovery_mod(self, recovery_mod=True):
        """进入 recovery"""
        if recovery_mod:
            self.adb_shell(f"reboot recovery")

    def in_bootloader_mod(self, bootloader_mod=True):
        """进入 bootloader"""
        if bootloader_mod:
            self.adb_shell(f"reboot bootloader")

    def flash(self):
        """
        刷机，包括 twrp、magisk、magisk module，这些都是在 recovery 模式下去刷的
        Returns:

        """
        try:
            self.in_bootloader_mod()
            time.sleep(1)
            # 刷入 twrp
            self.flash_twrp()
            # 刷入 magisk
            # self.flash_magisk()
            # 刷入 magisk 模块
            self.flash_magisk_module(only_flash_this=False)
        except Exception as e:
            logger.error(e)
        finally:
            self.reboot()

    def flash_system(self):
        """
        刷系统
        Returns:

        """
        try:
            file_path = {
                "Pixel": "sailfish-8.1",
                # 'Pixel': 'sailfish-9.0',
                "Pixel 3": "blueline-9",
                # 'Pixel 3': 'blueline-11',
            }
            self.adb_shell("reboot bootloader")
            time.sleep(1)
            path = f"{IMG_BASH_PATH}/{file_path[self.model]}"
            flash_system_cmd = f"cd {path} && sh flash-all-mul-devices.sh {self.device_name}"
            logger.info(f"设备: {self.device_name} 刷入系统")
            self.shell(flash_system_cmd)
        except Exception as e:
            logger.error(e)

        finally:
            time.sleep(1)
            self.reboot()

    def push_pem_to_system(self, pems: list, is_reboot=True, is_power_off=False):
        """
        推入证书到系统证书目录下
        Args:
            pems: 证书
            is_reboot: 是否重启
            is_power_off: 是否关机

        Returns:

        """
        self.wait_device()
        self.system_mount_rw()
        for pem in pems:
            # 先推入至 sd 卡
            self.adb_shell(f"push {PEM_BASH_PATH}/{pem} /sdcard")
            # 然后将证书放入系统证书目录
            self.adb_shell(f"shell su -c 'mv /sdcard/{pem} /system/etc/security/cacerts'")
            # 修改证书文件的权限
            self.adb_shell(f"shell su -c 'chmod 644 /system/etc/security/cacerts/{pem}'")
            logger.info(f"{self.device_name} 推入证书到系统信任目录下 : {pem}")
        self.system_mount_ro()
        if is_reboot:
            self.reboot()
        if not is_reboot and is_power_off:
            self.power_off()

    def system_mount_rw(self):
        """改为可写"""
        self.adb_shell(f"disable-verity")
        # self.adb_shell(f"shell su -c 'mount -o remount,rw /'")
        # self.adb_shell(f"shell su -c 'mount -o remount,rw /system'")
        self.adb_shell(f"shell su -c 'mount -o rw,remount -t auto /system'")

    def system_mount_ro(self):
        """改为只读"""
        self.adb_shell(f"shell su -c 'mount -o ro,remount /'")

    def push_pem_to_user(self, pems, is_reboot=True):
        """把证书安装到用户目录下，配合 Magisk 的 Move Certificates 模块使用"""
        self.wait_device()
        # 是否要先创建目录
        self.adb_shell(f"shell su -c 'mkdir -p /data/misc/user/0/cacerts-added'")
        for pem in pems:
            # 先推入至 sd 卡
            self.adb_shell(f"push {PEM_BASH_PATH}/{pem} /sdcard")
            # 然后将证书放入系统证书目录
            self.adb_shell(f"shell su -c 'mv /sdcard/{pem} /data/misc/user/0/cacerts-added'")
            # 修改证书文件的权限
            self.adb_shell(f"shell su -c 'chmod 644 /data/misc/user/0/cacerts-added/{pem}'")
            logger.info(f"{self.device_name} 推入证书到用户信任目录下 : {pem}")
        if is_reboot:
            self.reboot()

    def build_busybox(self, busybox):
        """
        BusyBox 是标准 Linux 工具的一个单个可执行实现。BusyBox 包含了一些简单的工具，例如 cat 和 echo，
        还包含了一些更大、更复杂的工具，例如 grep、find、mount 以及 telnet。
        有些人将 BusyBox 称为 Linux 工具里的瑞士军刀.简单的说BusyBox就好像是个大工具箱，它集成压缩了 Linux 的许多工具和命令。
        Args:
            busybox:

        Returns:

        """
        self.wait_device()
        # 先推入至 sd 卡
        self.adb_shell(f"push {BUSUYBOX_BASH_PATH}/{busybox} /sdcard")
        # self.adb_shell("shell su -c 'mount -o remount,rw / '")

        # 然后将证书放入系统证书目录
        # self.adb_shell(f"shell su -c 'mv /sdcard/{busybox} system/bin/'")
        self.adb_shell(f"shell su -c 'mv /sdcard/{busybox} /data/local'")
        # self.adb_shell(f"shell su -c 'mv /sdcard/{busybox} /system/bin/'")
        # 修改证书文件的权限

        # self.adb_shell(f"shell su -c 'chmod 777 /system/bin/{busybox}'")
        self.adb_shell(f"shell su -c 'chmod 777 /data/local/{busybox}'")

        # self.adb_shell("shell 'cd system/bin'")
        self.adb_shell(f"shell su -c '/data/local/{busybox} --install /system/bin/'")
        # self.adb_shell("shell su -c 'mount -o ro,remount /'")

        logger.info(f"{self.device_name} 安装成功 busybox")

    def tcpip(self, start=True, stop=False):
        """tcpip 处理"""
        self.system_mount_rw()
        self.adb_shell("shell su -c 'cp /system/build.prop /sdcard'")
        if start:
            self.adb_shell("shell 'echo service.adb.tcp.port=5555 >>/sdcard/build.prop'")
            self.adb_shell("shell 'echo persist.service.adb.enable=1 >> /sdcard/build.prop'")
        elif stop:
            self.sed_execute("'/service.adb.tcp.port/d' /sdcard/build.prop")
            self.sed_execute("'/persist.service.adb.enable/d' /sdcard/build.prop")
        self.adb_shell("shell su -c 'mv /sdcard/build.prop /system/build.prop'")
        self.system_mount_ro()
        self.reboot()

    def tcpip_start(self):
        """永久开启 tcpip"""
        self.tcpip(start=True)

    def tcpip_stop(self):
        """
        永久关闭 tcpip
        """
        self.tcpip(stop=True)

    def wifi_set(self, host="172.16.88.37", port=8888, wifi="youmi", passwd="www.youmi.net"):
        """
        设置 wifi 和代理，但是代理设置似乎是不起作用的
        """
        logger.info(f"{self.device_name} 设置 wifi: {wifi}")
        self.adb_shell(
            f"shell am start -n tk.elevenk.proxysetter/.MainActivity -e host {host} -e port {port} -e ssid {wifi} -e key {passwd}"
        )

    def remove_password(self):
        self.in_recovery_mod()
        self.wait_device("准备删除密码")
        self.adb_shell("rm /data/system/locksettings.db")
        self.adb_shell("rm /data/system/locksettings.db-shm")
        self.adb_shell("rm /data/system/locksettings.db-wal")
        self.adb_shell("rm /data/system/gatekeeper.password.key")
        self.adb_shell("rm /data/system/gatekeeper.pattern.key")
        self.reboot()

    def screen_rotation(self):
        """
        禁止自动旋转屏幕
        Returns:

        """
        logger.info(f"{self.device_name} 设备禁止自动旋转屏幕")
        self.adb_shell(
            "shell content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0"
        )

    def battery_percent(self):
        """显示电量百分比"""
        logger.info(f"{self.device_name} 显示电量百分比")
        self.adb_shell(
            "shell content insert --uri content://settings/system --bind name:s:status_bar_show_battery_percent --bind value:i:1"
        )

    def reboot(self):
        """重启"""
        logger.info(f"{self.device_name} 设备重启中...")
        self.adb_shell("reboot")

    def power_off(self):
        """关机"""
        logger.info(f"{self.device_name} 设备关机中...")
        self.adb_shell("shell reboot -p")

    def device_setting(self):
        """
        手机设置，包括屏幕旋转，wifi 设置等
        """
        self.reset_date()
        self.screen_rotation()
        self.battery_percent()
        self.authorize_usb_keys()
        self.turn_off_blue_tooth()
        # self.wifi_set()

    def reset_date(self, timezone="Asia/Shanghai"):
        """
        命令格式：date MMddHHmmyyyy.ss set
        （月日时分年.秒）
        例如：date 052514192019.22 set
        Returns:

        """
        import time

        date = time.strftime("%m%d%H%M%Y.%S")
        self.adb_shell(f"shell su -c 'setprop persist.sys.timezone {timezone}'")
        self.adb_shell(f"shell su -c 'settings put global time_zone  {timezone}'")
        self.adb_shell(f"shell su -c 'date {date} set'")
        logger.info(f"{self.device_name} 修正日期")

    def turn_off_blue_tooth(self):
        """
        需要重启手机才能生效
        Returns:

        """
        logger.info(f"{self.device_name} 关闭蓝牙")
        # 打开的话，只需要把 0 改成 1 即可
        self.adb_shell("shell settings put global bluetooth_on 0")

    def su(self):
        """
        这里为的是让 magisk 出现是否允许 shell 命令使用超级用户的提示，这个是需要手动去做点的
        但我们可以批量去让设备出现这个提示
        Returns:

        """
        logger.info(f"{self.device_name} 启动 su 权限。。。")
        # 先亮屏
        self.light_screen()
        self.adb_shell(f"shell su")

    def light_screen(self):
        """亮屏，并往上滑动屏幕"""
        if self.adb_shell("shell dumpsys activity | grep 'mSleeping=true'"):
            self.adb_shell("shell input keyevent 26")
            self.adb_shell("shell input swipe 500 1000 500 100")

    def install_app(self, apps: list):
        """安装 app"""
        self.wait_device()
        for app in apps:
            logger.info(f"{self.device_name} 安装 app : {app}")
            # -r：重新安装现有应用，并保留其数据; -d：允许版本代码降级。
            self.adb_shell(f"install -r -d {APK_BASH_PATH}/{app}")

    def collect_ks_did(self, ks_package="ks_8.3.apk"):
        is_installed = self.adb_shell("shell pm list packages com.smile.gifmaker")
        if not is_installed:
            logger.info(f"正在安装 apk: {ks_package}")
            self.adb_shell(f"install {APK_BASH_PATH}/{ks_package}")
        if not self.adb_shell("shell ps | grep com.smile.gifmaker"):
            # 获取主 activity: aapt list -a ks_8.3.apk | grep -B 15 LAUNCHER  | grep com 或者使用 androguard
            self.adb_shell(f"shell am start com.smile.gifmaker/com.yxcorp.gifshow.HomeActivity")
            if not is_installed:
                time.sleep(8)
        res = self.adb_shell(
            "shell su -c 'cat /data/data/com.smile.gifmaker/shared_prefs/kspocfp.xml | grep kwddk_pro'"
        )

        did = re.findall(">(.*)<", res)[0]
        logger.info(f"android_id: {self.android_id}, did: {did}")
        return did

    @property
    def android_id(self):
        android_id = self.adb_shell("shell settings get secure android_id").strip()
        return android_id

    def authorize_usb_keys(self):
        """
        adb 授权 PC 端的调试，原理是将本地的 adb_keys（本地的key 可通过 cat  ~/.android/adbkey.pub 查看)，加入到 android 端的 /data/misc/adb/adb_keys 文件下
        通过拉取远程的 adb_keys 到本地，然后再加入需要授权的再推到远程去
        这里不直接改动远程的 /data/misc/adb/adb_keys，原因是无论使用 echo 还是 tee 追加，都会报错： can't create /data/misc/user/0/keys: Permission denied
        """
        file_name = "adb_keys"
        # 随机命名，避免冲突，最后会删除该文件
        remote_file_name = f"{self.device_name}:{uuid.uuid4().hex}"
        remote_path = "/data/misc/adb/adb_keys"
        self.wait_device("授权 adb_key")
        self.adb_shell(f"pull {remote_path} {remote_file_name} ")
        with open(file_name, "r") as f, open(remote_file_name, "r+") as w:
            # r+ 模式是把文件指针将会放在文件的开头，如果直接写，会覆盖原来的文件。而使用了w.readlines()后，相当于把指针移到了末尾，这时候再写入就等同于追加了
            remote_adb_keys = [adb_key for adb_key in w.readlines()]
            for i in f.readlines():
                if not i.endswith("\n"):
                    i = i + "\n"
                # 判断如果要追加的 adb_key 没有在 adb_keys 文件中，则写入
                if i not in remote_adb_keys:
                    w.write(i)
        self.adb_shell(f"push {remote_file_name} /sdcard/remote_adb_keys ")
        self.adb_shell(f"shell su -c 'mv /sdcard/remote_adb_keys {remote_path}'")
        self.adb_shell(f"shell su -c 'chown system:shell {remote_path}'")
        self.adb_shell(f"shell su -c 'chmod 640 {remote_path}'")
        os.remove(remote_file_name)

    def collect_info(self, collect_ks_did=False):
        """
        重刷机后，android_id 会变，imei 和 mac 不会变
        Args:
            collect_ks_did:

        Returns:

        """
        cmd_list = {
            # adb shell pm list packages
            "os_version": "shell getprop ro.build.version.release",  # 系统版本
            "sdk": "shell getprop ro.build.version.sdk",  # android版本对应sdk版本
            "brand": "shell getprop ro.product.brand",  # 设备品牌
            "model": "shell getprop ro.product.model",  # 设备型号
            "manufacturer": "shell getprop ro.product.manufacturer",  # 设备厂商
            "imei": "shell service call iphonesubinfo 1",  # imei
            "android_id": "shell settings get secure android_id",  # android_id
            "imsi": "shell getprop persist.radio.last.subscriber",  # imsi
            "sw": "shell wm size",  # 屏幕分辨率-宽
            "sh": "shell wm size",  # 屏幕分辨率-高
            "den": "shell getprop ro.sf.lcd_density",  # 屏幕密度  # 也可 adb shell wm density
            "serialno": "shell getprop ro.serialno",  # 设备序列号
            # 'product_device': 'adb -s %s shell getprop ro.product.device',  # 设备名
            "product": "shell getprop ro.build.product",  # 设备名
            "fingerprint": "shell getprop ro.build.fingerprint",  # 指纹
            "display_id": "shell getprop ro.build.display.id",  # 版本号
            "sys_compiling_time": "shell getprop ro.build.date",  # 系统编译时间
            "sys_compiling_time_utc": "shell getprop ro.bootimage.build.date.utc",  # 系统编译时间对应时间戳
            "mac": "shell su -c 'cat /sys/class/net/wlan0/address'",  # WIFI MAC地址
            # "mac": "shell getprop persist.sys.wifi.mac",  # WIFI MAC地址
            "board": "shell getprop ro.product.board",  # 主板名 / 处理器型号
            "timezone": "shell getprop persist.sys.timezone",  #
            "bluetooth_mac": "shell getprop ro.bluetooth.macaddr",  # 蓝牙mac地址
            "hardware": "shell getprop ro.boot.hardware",  # 硬件信息
            "code_name": "shell getprop ro.product.codename",
            "country": "shell getprop gsm.sim.operator.iso-country",  # 国家
            "ip": "shell getprop net.rmnet_data0.gw",  # IP
        }
        device_info = {}
        for key, value in cmd_list.items():
            result = self.adb_shell(value)
            device_info[key] = result.replace("\n", "").replace("\r", "") if result else ""
        if device_info.get("sh"):
            device_info["sh"] = device_info["sh"].split("x")[-1]
        if device_info["sw"]:
            device_info["sw"] = device_info["sw"].split(" ")[-1].split("x")[0]
        if device_info.get("country"):
            device_info["country"] = device_info["country"].split(",")[-1]
        if device_info["imei"]:
            imei1 = device_info["imei"].split("'")
            device_info["imei"] = (imei1[1] + imei1[3] + imei1[5]).replace(".", "").strip(" ")
        if device_info.get("imsi"):
            device_info["imsi"] = device_info["imsi"].split(",")[-1]
        logger.info(json.dumps(device_info))
        # if collect_ks_did:
        #     device_info["ks_did"] = self.collect_ks_did()
        return device_info

    def push_something(self, files, remote_path="/sdcard"):
        files = files if isinstance(files, list) else [files]
        for file in files:
            self.adb_shell(f"push {file} {remote_path}")
            logger.info(f"push {file} to {remote_path}")

    def write_frpc_conf(self, adb_port_begin=5000, frida_port_begin=22000, alias=1, num=None):
        server_addr = "1.117.31.3"
        server_port = "17000"
        lines = [
            "[common]",
            f"server_addr = {server_addr}",
            f"server_port = {server_port}",
            "token = kingsmanv2",
            "\n",
            f"[adb_tcpip_{num or alias}]",  # 注意命名，所有连入同一个 frps 服务端的，必须是唯一名称
            "type = tcp",
            "local_port = 5555",
            f"remote_port = {adb_port_begin + alias}",
            # f"[frida_tcpip_{alias}]",
            # "type = tcp",
            # "local_port = 22222",
            # f"remote_port = {frida_port_begin + alias}",
        ]
        if frida_port_begin:
            lines.extend(
                [
                    "\n",
                    f"[frida_tcpip_{num or alias}]",
                    "type = tcp",
                    "local_port = 22222",
                    f"remote_port = {frida_port_begin + alias}",
                ]
            )

        file_name = f"{str(uuid.uuid4())}.ini"
        _path = "tmp"
        if not os.path.exists(_path):
            os.mkdir(_path)

        with open(f"{_path}/{file_name}", "w+") as f:
            f.writelines(map(lambda x: x + "\n", lines))
            f.write("\n")
        self.adb_shell(f"push tmp/{file_name} /sdcard/")
        self.adb_shell(f"shell su -c 'mkdir /data/frpc/'")
        self.adb_shell(f"shell su -c 'mv /sdcard/{file_name} /data/frpc/frpc.ini'")
        os.remove(f"tmp/{file_name}")
        logger.info("写入 frpc.ini 文件到 /data/frpc 目录下")


class BaseRun:
    def __init__(self):
        logger.debug(f'开始时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        self.devices = AdbClient().devices
        logger.info(f"设备个数: {len(self.devices)}, 设备: {self.devices}")
        self.Flash = Flash
        self.Process = Process
        self.pool = Pool(multiprocessing.cpu_count())
        self.logger = logger

    def run(self):
        for device in self.devices:
            obj = self.Flash(device)
            self.pool.apply_async(
                obj.flash,
            )
        self.pool.close()
        self.pool.join()


if __name__ == "__main__":
    devices = AdbClient().devices
    print(devices)
