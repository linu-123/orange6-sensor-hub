#
# Orange 6 Sensor Hub - Buildozer 打包配置
# 目标设备: 橘子6 (Orange 6)
# CPU架构: arm64-v8a (必需! 否则无法在橘子6安装)
# 框架: Kivy + KivyMD + pyjnius
#

[app]

# (str) 应用标题
title = Orange 6 Sensor Hub

# (str) 包名 (需唯一)
package.name = orange6sensorhub

# (str) 应用域名
package.domain = com.orange6.sensor

# (str) 源码入口文件
source.dir = .

# (list) 需要包含的源码源文件
source.include_exts = py,png,jpg,kv,atlas,ttf,otf,txt

# (list) 需要排除的文件/目录
source.exclude_dirs = tests, bin, .git, __pycache__, *.pyc

# (list) 需要包含的特定文件
source.include_patterns = *

# (str) 应用版本号
version = 1.0.0

# (str) 应用描述
description = Orange 6 Sensor Hub

# (str) 应用的 Android 最低 SDK 版本
android.api = 31

# (str) 应用的 Android 目标 SDK 版本
android.minapi = 26

# (int) Android SDK 版本号 (用于编译)
android.sdk = 31

# (str) Android NDK 版本
android.ndk = 25c

# (bool) 是否使用 Android 原生主题
android.native.theme = True

# (str) 支持的屏幕方向
orientation = portrait

# (list) 支持的目标架构 - 关键: 橘子6需要arm64-v8a
android.archs = arm64-v8a

# (list) Android 权限声明
android.permissions = CAMERA, RECORD_AUDIO, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, INTERNET, BODY_SENSORS

# (list) Python 依赖
requirements = python3,kivy,kivymd,pyjnius,plyer,Pillow

# (bool) 是否启用 AndroidX
android.use_androidx = True

# (bool) 是否启用暂停/恢复事件
android.wakelock = True

# (str) 编译输出目录
bin_dir = ./bin/

[buildozer]
log_level = 2