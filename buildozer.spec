"""
============================================================
🍊 Orange 6 Sensor Hub - Buildozer 打包配置
============================================================
目标设备: 橘子6 (Orange 6)
CPU架构: arm64-v8a (必需! 否则无法在橘子6安装)
框架: Kivy + KivyMD + pyjnius
"""

[app]

# (str) 应用标题
title = 橘子6 全传感器

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

# (str) 应用版本代码 (Android, 用于版本比较)
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py

# (str) 应用描述
description = 橘子6全传感器APP - 调用手机全部内置传感器、摄像头、GPS、麦克风等硬件的综合传感器工具。

# (str) 应用长描述
description.full = 一款专为橘子6(Orange 6)手机设计的全传感器调用工具。支持加速度传感器、陀螺仪、地磁传感器、光线传感器、距离传感器、气压传感器、湿度传感器、温度传感器、重力传感器、线性加速度、旋转向量、计步器、心率传感器等全部内置传感器的实时数据读取与展示。同时支持前后摄像头拍照、GPS精准定位、麦克风录音等功能。Material Design 3 美化界面，流畅交互体验。

# (str) 应用的 Android 最低 SDK 版本
android.api = 31

# (str) 应用的 Android 目标 SDK 版本
android.minapi = 26

# (int) Android SDK 版本号 (用于编译)
android.sdk = 31

# (str) Android NDK 版本
android.ndk = 25b

# (bool) 是否使用 Android 原生主题
android.native.theme = True

# (str) 应用图标 (需为 512x512 PNG)
# icon.filename = %(source.dir)s/assets/icon.png

# (str) 应用启动画面
# presplash.filename = %(source.dir)s/assets/presplash.png

# (str) 支持的屏幕方向: portrait, landscape, sensor, user
orientation = portrait

# (list) 支持的目标架构
# ⚠️ 关键: 橘子6是64位处理器, 必须指定 arm64-v8a
android.archs = arm64-v8a

# (list) Android 权限声明
# ⚠️ 关键: 橘子6需要全部传感器权限
android.permissions = \
    CAMERA, \
    RECORD_AUDIO, \
    ACCESS_FINE_LOCATION, \
    ACCESS_COARSE_LOCATION, \
    WRITE_EXTERNAL_STORAGE, \
    READ_EXTERNAL_STORAGE, \
    INTERNET, \
    ACCESS_NETWORK_STATE, \
    ACCESS_WIFI_STATE, \
    VIBRATE, \
    BLUETOOTH, \
    WAKE_LOCK, \
    BODY_SENSORS, \
    ACTIVITY_RECOGNITION, \
    HIGH_SAMPLING_RATE_SENSORS

# (list) Android 硬件特性声明
# 声明需要使用哪些传感器硬件
android.features = \
    android.hardware.camera, \
    android.hardware.camera.front, \
    android.hardware.camera.autofocus, \
    android.hardware.sensor.accelerometer, \
    android.hardware.sensor.gyroscope, \
    android.hardware.sensor.compass, \
    android.hardware.sensor.light, \
    android.hardware.sensor.proximity, \
    android.hardware.sensor.barometer, \
    android.hardware.sensor.humidity, \
    android.hardware.sensor.ambient_temperature, \
    android.hardware.sensor.heartrate, \
    android.hardware.sensor.stepcounter, \
    android.hardware.location.gps, \
    android.hardware.microphone

# (bool) 如果传感器硬件不存在, 是否仍允许安装
android.gradle_dependencies = ''

# (str) Gradle 仓库
android.gradle_repositories = []

# (str) 额外的 Android 清单配置
android.manifest_matches = \
    <uses-feature android:name="android.hardware.sensor.light" android:required="false"/> \
    <uses-feature android:name="android.hardware.sensor.proximity" android:required="false"/> \
    <uses-feature android:name="android.hardware.sensor.barometer" android:required="false"/> \
    <uses-feature android:name="android.hardware.sensor.humidity" android:required="false"/> \
    <uses-feature android:name="android.hardware.sensor.ambient_temperature" android:required="false"/> \
    <uses-feature android:name="android.hardware.sensor.heartrate" android:required="false"/> \
    <uses-feature android:name="android.hardware.camera" android:required="true"/> \
    <uses-feature android:name="android.hardware.camera.front" android:required="false"/> \
    <uses-feature android:name="android.hardware.microphone" android:required="true"/> \
    <uses-feature android:name="android.hardware.location.gps" android:required="true"/>

# (str) 附加的 Android 库 (AAR/JAR)
# android.add_aars =

# (str) 附加的 Java 源码目录
# android.add_src =

# (str) 附加的编译参数
android.add_compile_args = -target 1.8

# (str) Java 编译级别
android.java_compile_options = -source 1.8 -target 1.8

# (str) Python-for-Android 分支
p4a.branch = develop

# (str) Python-for-Android 源码目录 (如果使用本地 clone)
# p4a.source_dir =

# (list) 需要包含的 Python 包 (pip requirements)
requirements = python3,kivy==2.1.0,kivymd==1.1.1,pyjnius==1.5.0,plyer==2.1.0,Pillow

# (str) 自定义 Android 活动类(Activity) 名称
# android.custom_activity =

# (str) Android 应用的类别 (launcher, info, etc)
# android.category =

# (bool) 是否启用 AndroidX
android.use_androidx = True

# (bool) 是否启用暂停/恢复事件
android.wakelock = True

# (str) 编译输出目录
# build_dir = ./build/

# (str) Android 原生库输出目录
# dist_dir = ./dist/

# (str) APK 输出目录
# bin_dir = ./bin/

# (str) 签名密钥目录
# android.keystore =

# (str) 签名密钥密码
# android.keystore.alias =

# (str) Android 包签名密码
# android.keystore.password =

# (list) 需要加入 JAR 列表的 Java 库
# android.add_jars =

# (str) Jar 文件搜索目录
# android.jetify_src =

# (bool) 是否使用 Gradle 构建 (推荐)
android.build_tools = 33.0.0

# (str) Gradle 版本
android.gradle_version = 7.4.2

# (list) 附加的 Android Gradle 编译配置
# android.gradle_compile_options =

# (str) 自定义 AndroidManifest.xml 覆盖
# android.manifest = AndroidManifest.xml


[buildozer]

# (int) 日志级别 (0=安静, 1=正常, 2=详细)
log_level = 2

# (bool) 是否在编译前清理构建目录
# clean_before_build = False

# (str) 下载缓存目录
# download_cache_dir =


[www]

# (str) 应用网站 URL 路径
# path = /

# (int) 服务器端口
# port = 8080


[build]
# (str) 编译平台目录
# platform_dir = ./platforms/

# (str) 本地 python-for-android 目录
# p4a_local =

# (str) Buildozer 源码目录
# buildozer_dir =