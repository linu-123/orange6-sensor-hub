"""
🍊 Orange 6 Sensor Hub - 橘子6全传感器APP
========================================
目标设备: 橘子6 (Orange 6)
架构: arm64-v8a
框架: Kivy + KivyMD
传感器桥接: pyjnius JNI (SensorManager)

功能:
  - 调用全部内置传感器 (加速度/陀螺仪/地磁/光线/距离/气压/湿度/温度/重力等)
  - 前后摄像头调用
  - GPS定位
  - 电池状态监测
  - Material Design 美化界面
"""

import os
import sys

# 设置 Kivy 环境变量 (必须在导入 kivy 之前)
os.environ['KIVY_ORIENTATION'] = 'Portrait'
os.environ['KIVY_METRICS_DENSITY'] = '1.5'

from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '1080')
Config.set('graphics', 'height', '1920')
Config.set('graphics', 'minimum_width', '360')
Config.set('graphics', 'minimum_height', '640')
Config.set('kivy', 'log_level', 'info')

from kivy.core.window import Window
Window.softinput_mode = 'below_target'

from kivy.logger import Logger
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.utils import platform

# KivyMD 导入
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.toast import toast

# 自定义模块导入
from appui.sensor_bridge import SensorManagerBridge, SENSOR_NAMES_CN, SENSOR_UNITS, SENSOR_ICONS
from appui.camera_module import CameraModule
from appui.gps_module import GPSModule


class Orange6App(MDApp):
    """
    橘子6 全传感器APP 主程序
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 初始化各模块
        self.sensors = SensorManagerBridge()
        self.camera = CameraModule()
        self.gps = GPSModule()

        # 上次传感器刷新时间
        self._last_refresh = 0

    def build(self):
        """构建APP界面"""
        # 设置主题
        self.theme_cls.primary_palette = 'Orange'
        self.theme_cls.accent_palette = 'DeepOrange'
        self.theme_cls.theme_style = 'Light'  # 可切换 'Dark' 深色模式
        self.theme_cls.material_style = 'M3'

        # 加载 KV 布局文件
        kv_path = os.path.join(
            os.path.dirname(__file__), 'ui', 'orange6.kv'
        )
        if os.path.exists(kv_path):
            Builder.load_file(kv_path)
            Logger.info("Orange6App: Loaded KV layout")
        else:
            Logger.error(f"Orange6App: KV file not found at {kv_path}")

        # 定时刷新 UI 数据 (10Hz)
        Clock.schedule_interval(self._update_ui, 0.1)

        Logger.info("Orange6App: Build complete")
        return Builder.load_string('''
MDScreenManager:
    MDScreen:
        name: 'placeholder'
        MDLabel:
            text: '加载中...'
            halign: 'center'
            valign: 'center'
''')

    def on_start(self):
        """APP启动后回调"""
        super().on_start()
        Logger.info("Orange6App: Application started")

        # 切换到仪表盘页面
        if hasattr(self, 'root') and self.root:
            screen_manager = self.root
            if hasattr(screen_manager, 'current'):
                screen_manager.current = 'dashboard'

        # 显示启动提示
        toast('🍊 橘子6 全传感器已启动')

        # 检查传感器状态
        if self.sensors.is_connected:
            Logger.info("Orange6App: Sensors connected successfully")
        else:
            Logger.warning("Orange6App: Sensors not connected - running in desktop mock mode")

    def _update_ui(self, dt):
        """
        定期更新UI显示
        由于Kivy的property绑定，大部分数值会自动更新
        这里主要用于触发UI刷新
        """
        try:
            # 更新GPS标签（如果存在）
            if hasattr(self, 'gps') and self.gps:
                pass  # data-binding handles it

            # 更新顶部栏标题（根据传感器连接状态）
            pass
        except Exception as e:
            Logger.warning(f"Orange6App: UI update warning: {e}")

    def refresh_sensors(self):
        """手动刷新所有传感器数据"""
        toast('🔄 传感器数据已刷新')
        Logger.info("Orange6App: Manually refreshed sensor data")

    def toggle_gps(self, active):
        """切换GPS定位开关"""
        if active:
            self.gps.start()
            toast('📍 GPS 定位已开启')
        else:
            self.gps.stop()
            toast('📍 GPS 定位已关闭')
        Logger.info(f"Orange6App: GPS {'started' if active else 'stopped'}")

    def switch_camera(self):
        """切换前后摄像头"""
        is_front = self.camera.switch_camera()
        toast(f'📷 已切换到{"前置" if is_front else "后置"}摄像头')

    def take_photo(self):
        """拍照"""
        path = self.camera.take_photo()
        toast(f'📸 照片已保存: {os.path.basename(path)}')
        Logger.info(f"Orange6App: Photo taken: {path}")

    def on_pause(self):
        """APP进入后台 - 暂停传感器（省电）"""
        if hasattr(self, 'sensors'):
            # 在真机上应降低采样率或暂停
            pass
        Logger.info("Orange6App: Application paused")
        return True

    def on_resume(self):
        """APP回到前台 - 恢复传感器"""
        Logger.info("Orange6App: Application resumed")
        if hasattr(self, 'sensors'):
            pass  # 恢复传感器监听

    def on_stop(self):
        """APP关闭 - 清理资源"""
        Logger.info("Orange6App: Application stopping...")

        if hasattr(self, 'sensors'):
            self.sensors.cleanup()
            Logger.info("Orange6App: Sensors cleaned up")

        if hasattr(self, 'camera'):
            self.camera.cleanup()
            Logger.info("Orange6App: Camera cleaned up")

        if hasattr(self, 'gps'):
            self.gps.cleanup()
            Logger.info("Orange6App: GPS cleaned up")

        Logger.info("Orange6App: Application stopped")


if __name__ == '__main__':
    Logger.info(f"Orange6App: Platform = {platform}")
    Logger.info(f"Orange6App: Python version = {sys.version}")
    Logger.info(f"Orange6App: Kivy starting...")

    try:
        Orange6App().run()
    except Exception as e:
        Logger.error(f"Orange6App: Fatal error: {e}")
        import traceback
        Logger.error(traceback.format_exc())
        sys.exit(1)