# 🍊 Orange 6 Sensor Hub — 橘子6全传感器APP

> **目标设备**: 橘子6 (Orange 6)  
> **架构**: arm64-v8a (64位)  
> **框架**: Kivy 2.1.0 + KivyMD 1.1.1  
> **传感器桥接**: pyjnius JNI (Android SensorManager)  
> **打包工具**: Buildozer

---

## 📁 项目结构

```
orange6_app/
├── main.py                  # APP主入口
├── buildozer.spec           # Buildozer打包配置 (arm64-v8a)
├── requirements.txt         # Python依赖
├── README.md                # 本文件
├── __init__.py
├── appui/                   # 功能模块
│   ├── __init__.py
│   ├── sensor_bridge.py     # 传感器JNI桥接 (核心)
│   ├── camera_module.py     # 前后摄像头
│   └── gps_module.py        # GPS定位
├── ui/                      # UI布局
│   ├── __init__.py
│   └── orange6.kv           # KivyMD界面定义
└── assets/                  # 资源文件 (图标等)
```

---

## 🚀 快速开始

### 1️⃣ 桌面测试 (无传感器, 模拟数据)

```bash
# 安装依赖
pip install kivy kivymd pyjnius plyer

# 运行 (桌面模式, 传感器为模拟数据)
cd orange6_app
python main.py
```

### 2️⃣ 编译APK (Linux / WSL)

#### 环境要求
- Ubuntu 20.04+ / Debian 11+ / WSL2
- Python 3.8+
- JDK 8+
- Android SDK + NDK

#### 一键编译

```bash
# 1. 安装 buildozer
pip install buildozer cython

# 2. 初始化 (若第一次使用)
# cd orange6_app
# buildozer init

# 3. ⚠️ 修改 buildozer.spec 中的关键配置:
#    - android.archs = arm64-v8a      ← 橘子6必须!
#    - android.api = 31
#    - android.minapi = 26
#    - 确认所有权限已声明
# (上述配置已预设好，直接使用即可)

# 4. 编译 APK
buildozer android debug

# 5. 生成的 APK 在 bin/ 目录下
#    orange6sensorhub-1.0.0-arm64-v8a-debug.apk
```

#### 编译参数说明

| 参数 | 值 | 说明 |
|------|-----|------|
| `android.archs` | `arm64-v8a` | 🟢 **必须** - 橘子6是64位处理器 |
| `android.api` | `31` | 目标 Android 12 |
| `android.minapi` | `26` | 最低 Android 8.0 |
| `orientation` | `portrait` | 竖屏锁定 |
| `android.permissions` | 见 spec | 全部传感器/相机/GPS/麦克风权限 |

---

## 📱 功能详解

### 传感器支持

| 传感器 | Android API | 状态指示 | 实时数据 |
|--------|------------|----------|---------|
| 📐 加速度传感器 | TYPE_ACCELEROMETER (1) | 🟢/🔴 | X/Y/Z 三轴 m/s² |
| 🌀 陀螺仪 | TYPE_GYROSCOPE (4) | 🟢/🔴 | X/Y/Z 三轴 rad/s |
| 🧲 地磁传感器 | TYPE_MAGNETIC_FIELD (2) | 🟢/🔴 | X/Y/Z 三轴 μT |
| ☀️ 光线传感器 | TYPE_LIGHT (5) | 🟢/🔴 | lux |
| 📏 距离传感器 | TYPE_PROXIMITY (8) | 🟢/🔴 | cm |
| 🌡 气压传感器 | TYPE_PRESSURE (6) | 🟢/🔴 | hPa |
| 💧 湿度传感器 | TYPE_RELATIVE_HUMIDITY (12) | 🟢/🔴 | % |
| 🌡 温度传感器 | TYPE_AMBIENT_TEMPERATURE (13) | 🟢/🔴 | °C |
| ⬇️ 重力传感器 | TYPE_GRAVITY (9) | 🟢/🔴 | X/Y/Z m/s² |
| 🚀 线性加速度 | TYPE_LINEAR_ACCELERATION (10) | 🟢/🔴 | X/Y/Z m/s² |
| 🔄 旋转向量 | TYPE_ROTATION_VECTOR (11) | 🟢/🔴 | 四元数 |
| 🚶 计步器 | TYPE_STEP_COUNTER (19) | 🟢/🔴 | 步数 |
| ❤️ 心率 | TYPE_HEART_RATE (21) | 🟢/🔴 | bpm |
| 💥 显著运动 | TYPE_SIGNIFICANT_MOTION (17) | 🟢/🔴 | 是/否 |

### 其他功能

- 📷 **前后摄像头** — 实时预览、拍照、切换
- 🛰 **GPS定位** — 经纬度、海拔、速度、方向、地址反编码
- 🔋 **电池状态** — 电量百分比、充电状态
- 📊 **传感器总览** — 全部传感器数值实时显示
- 🎨 **Material Design 3** — 圆角卡片、图标、状态指示灯

---

## 🔐 权限清单

| 权限 | 用途 |
|------|------|
| `CAMERA` | 前后摄像头调用 |
| `RECORD_AUDIO` | 麦克风录音 |
| `ACCESS_FINE_LOCATION` | GPS精确定位 |
| `ACCESS_COARSE_LOCATION` | 网络辅助定位 |
| `WRITE_EXTERNAL_STORAGE` | 存储照片/数据 |
| `READ_EXTERNAL_STORAGE` | 读取存储 |
| `BODY_SENSORS` | 心率传感器 |
| `ACTIVITY_RECOGNITION` | 计步器/运动检测 |
| `HIGH_SAMPLING_RATE_SENSORS` | 高采样率传感器 |

---

## ⚠️ 重要注意事项

### 1. arm64-v8a 架构
橘子6 搭载 64 位处理器，**必须**在 `buildozer.spec` 中设置：
```ini
android.archs = arm64-v8a
```
否则编译出的 APK 无法在橘子6上安装。

### 2. 传感器 JNI 桥接
Python 无法直接读取 Android 复合传感器，本项目通过 `pyjnius` 桥接 Java `SensorManager` API：

```
Python (Kivy) → pyjnius → Java SensorManager → Sensor HAL → 硬件
```

确保 `buildozer.spec` 的 `requirements` 中包含 `pyjnius`：
```ini
requirements = python3,kivy==2.1.0,kivymd==1.1.1,pyjnius==1.5.0,plyer==2.1.0,Pillow
```

### 3. 运行时权限
Android 6.0+ 需要在运行时动态申请权限：
- 相机
- 麦克风  
- GPS定位

APP启动后会自动弹出权限请求。

### 4. 后台保活
传感器监听在 Activity 生命周期管理下运行，切换后台时会自动降低采样率以省电。

### 5. 深色模式适配
可在 `main.py` 中切换：
```python
self.theme_cls.theme_style = 'Dark'  # 或 'Light'
```

---

## 🛠 开发调试

### 查看日志

```bash
# 安装到手机后查看日志
adb logcat | grep -i "orange\|sensor\|python"
```

### 桌面模式
在 Windows/Mac/Linux 桌面运行时，所有传感器数据使用 **模拟数据**，方便 UI 调试：
- 加速度: 随机 ±9.8 m/s²
- 陀螺仪: 随机 ±5 rad/s
- GPS: 北京/上海/深圳 模拟位置
- 电池: 随机 50-100%

---

## 📦 输出产物

编译完成后，APK 文件位于 `bin/` 目录：

```
bin/
└── orange6sensorhub-1.0.0-arm64-v8a-debug.apk
```

将此 APK 直接拷贝到橘子6安装即可。

---

## 📄 许可证

本项目为开源项目，仅供学习交流使用。

---

> **技术栈**: Python + Kivy + KivyMD + pyjnius + Buildozer  
> **适用设备**: 橘子6 (Orange 6) / 其他 arm64-v8a Android 设备  
> **版本**: v1.0.0