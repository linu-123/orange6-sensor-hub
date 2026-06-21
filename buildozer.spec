"""
============================================================
🍊 Orange 6 Sensor Hub - Buildozer 打包配置
============================================================
目标设备: 橘子6 (Orange 6)
CPU架构: arm64-v8a (必需! 否则无法在橘子6安装)
框架: Kivy + KivyMD + pyjnius
"""

[app]
title=Orange6
package.name=orange6sensor
package.domain=com.orange6
source.dir=.
version=1.0.0
requirements=python3,kivy,kivymd,pyjnius,plyer,Pillow
orientation=portrait
android.api=31
android.minapi=26
android.sdk=31
android.ndk=25c
android.archs=arm64-v8a
android.permissions=CAMERA,RECORD_AUDIO,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,INTERNET
android.use_androidx=True
android.wakelock=True
p4a.branch=develop
bin_dir=./bin/
