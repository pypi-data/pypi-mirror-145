
### 完整刷机步骤
```bash
1. 刷入系统，下载地址: https://developers.google.com/android/images#crosshatch（需要手动设置一些开机选项）
2. 刷入 twrp，下载地址: https://twrp.me/Devices/
3. 刷入 magisk 和 magisk 相关模块
4. 授权 magisk 的 shell 超级用户权限（执行 su.sh，然后 magisk 会弹出是否允许授权，手动允许即可
5. 批量安装 app
6. 批量把证书推到系统/用户证书目录下
7. 设备相关设置，包括设置日期（有时候代理不生效就是日期的问题）、授权 ag02 的 adb、设备禁止自动旋转屏幕、显示电量百分比
```

#### 1. 刷入系统
```bash
python -m flash.flash_system 
```

#### 2. 刷入 twrp（一并刷入 magisk 和 magisk 模块）
```bash
python -m flash.flash_trwp
``` 

#### 3. 授权 magisk 的 shell 超级用户权限  
```bash
# 需要手动点击授权
python -m flash.su
``` 

#### 4. 批量安装 app
```bash
# 较慢，需要等待
python -m flash.install_app
``` 

#### 5. 批量把证书推到系统/用户证书目录下
```bash
# 较慢，需要等待
python -m flash.push_pem_to_user
``` 

#### 6. 设备相关设置，包括设置日期
```bash
# 较慢，需要等待
python -m flash.device_setting
``` 


### 真机 frida 依赖里的 Magisk 模块

    Move_Certificates-v1.9.zip  # 证书
    adbd.zip,  # 华为云的 adbd，自动开启 tcpid
    frida-12.11.zip  # 目前用的是 12 版本，14版本在淘宝直播貌似有点问题
    busybox-ndkr.zip  # 提供的一些 linux 相关命令
    autofix.zip  # 自动修复一些异常，注意，这里写了个逻辑，如果连不上网，则会自动重启