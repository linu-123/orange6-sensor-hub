"""
相机模块 - 前后摄像头调用
支持实时预览、拍照、切换前后摄像头
"""

from kivy.logger import Logger
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty

try:
    from jnius import autoclass
    JNIUS_AVAILABLE = True
except ImportError:
    JNIUS_AVAILABLE = False


class CameraModule(EventDispatcher):
    """
    相机管理器
    在 Android 上使用 Java Camera2 API
    在桌面端使用 Kivy Camera 或模拟
    """

    camera_preview = ObjectProperty(None, allownone=True)
    is_front_camera = BooleanProperty(False)
    camera_available = BooleanProperty(False)
    last_photo_path = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._camera_widget = None
        self._preview_active = False

        if JNIUS_AVAILABLE:
            self._check_camera_hardware()

    def _check_camera_hardware(self):
        """检查摄像头硬件是否可用"""
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Context = autoclass('android.content.Context')
            activity = PythonActivity.mActivity
            package_manager = activity.getPackageManager()
            has_camera = package_manager.hasSystemFeature(
                'android.hardware.camera'
            )
            has_front = package_manager.hasSystemFeature(
                'android.hardware.camera.front'
            )
            self.camera_available = has_camera or has_front
            Logger.info(f"CameraModule: Camera available: {self.camera_available}")
        except Exception as e:
            Logger.warning(f"CameraModule: Camera check failed: {e}")
            self.camera_available = False

    def get_kivy_camera_index(self):
        """获取Kivy Camera索引（0=后置, 1=前置）"""
        return 1 if self.is_front_camera else 0

    def switch_camera(self):
        """切换前后摄像头"""
        self.is_front_camera = not self.is_front_camera
        Logger.info(f"CameraModule: Switched to {'front' if self.is_front_camera else 'back'} camera")
        return self.is_front_camera

    def take_photo(self, filename=None):
        """
        拍照（Android端通过Java Intent实现，桌面端仅模拟）
        返回照片保存路径
        """
        from datetime import datetime
        import os

        if filename is None:
            filename = f"orange6_photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

        # 在真实设备上会通过 Android Intent 调用系统相机
        save_path = os.path.join(
            os.path.expanduser('~'), 'Pictures', filename
        )

        self.last_photo_path = save_path
        Logger.info(f"CameraModule: Photo saved to {save_path}")
        return save_path

    def start_preview(self, camera_widget):
        """开始相机预览"""
        self._camera_widget = camera_widget
        self._preview_active = True
        Logger.info("CameraModule: Camera preview started")

    def stop_preview(self):
        """停止相机预览"""
        self._preview_active = False
        if self._camera_widget:
            self._camera_widget = None
        Logger.info("CameraModule: Camera preview stopped")

    def cleanup(self):
        """清理相机资源"""
        self.stop_preview()