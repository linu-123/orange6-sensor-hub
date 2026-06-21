"""
GPS定位模块
通过 plyer.gps 或 pyjnius 调用 Android LocationManager
获取经纬度、海拔、精度、地址信息
"""

from kivy.logger import Logger
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import DictProperty, NumericProperty, BooleanProperty

try:
    from plyer import gps as plyer_gps
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False
    Logger.warning("GPSModule: plyer not available")


class GPSModule(EventDispatcher):
    """
    GPS定位管理器
    支持 GPS + 网络定位
    自动解析地址信息
    """

    location = DictProperty({
        'latitude': 0.0,
        'longitude': 0.0,
        'altitude': 0.0,
        'accuracy': 0.0,
        'speed': 0.0,
        'bearing': 0.0,
        'address': '正在定位...',
    })
    gps_active = BooleanProperty(False)
    gps_available = BooleanProperty(False)
    satellites = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._update_event = None
        self._mock_mode = False

        if PLYER_AVAILABLE:
            try:
                plyer_gps.configure(
                    on_location=self._on_location,
                    on_status=self._on_status
                )
                self.gps_available = True
                Logger.info("GPSModule: plyer.gps configured")
            except Exception as e:
                Logger.warning(f"GPSModule: plyer.gps init failed: {e}")
                self._enable_mock_mode()
        else:
            self._enable_mock_mode()

    def _enable_mock_mode(self):
        """启用模拟模式（桌面测试用）"""
        self._mock_mode = True
        self.gps_available = True
        Logger.info("GPSModule: Using mock GPS data for desktop testing")

    def start(self):
        """启动GPS定位"""
        if not self.gps_available:
            Logger.warning("GPSModule: GPS not available")
            return

        if self._mock_mode:
            self.gps_active = True
            self._update_event = Clock.schedule_interval(self._mock_update, 1.0)
            Logger.info("GPSModule: Mock GPS started")
            return

        try:
            plyer_gps.start(minTime=1000, minDistance=1)
            self.gps_active = True
            Logger.info("GPSModule: GPS started")
        except Exception as e:
            Logger.error(f"GPSModule: Failed to start GPS: {e}")

    def stop(self):
        """停止GPS定位"""
        if self._update_event:
            self._update_event.cancel()
            self._update_event = None

        if self._mock_mode:
            self.gps_active = False
            Logger.info("GPSModule: Mock GPS stopped")
            return

        try:
            plyer_gps.stop()
            self.gps_active = False
            Logger.info("GPSModule: GPS stopped")
        except Exception as e:
            Logger.error(f"GPSModule: Failed to stop GPS: {e}")

    def _on_location(self, **kwargs):
        """plyer.gps 位置回调"""
        self.location = {
            'latitude': kwargs.get('lat', 0.0),
            'longitude': kwargs.get('lon', 0.0),
            'altitude': kwargs.get('altitude', 0.0),
            'accuracy': kwargs.get('accuracy', 0.0),
            'speed': kwargs.get('speed', 0.0),
            'bearing': kwargs.get('bearing', 0.0),
            'address': self._reverse_geocode(
                kwargs.get('lat', 0.0),
                kwargs.get('lon', 0.0)
            ),
        }

    def _on_status(self, status_type, status_message):
        """plyer.gps 状态回调"""
        Logger.info(f"GPSModule: Status {status_type}: {status_message}")

    def _mock_update(self, dt):
        """模拟GPS位置更新"""
        import random
        lat = 39.9042 + random.uniform(-0.005, 0.005)
        lon = 116.4074 + random.uniform(-0.005, 0.005)
        self.location = {
            'latitude': lat,
            'longitude': lon,
            'altitude': random.uniform(10, 100),
            'accuracy': random.uniform(5, 25),
            'speed': random.uniform(0, 10),
            'bearing': random.uniform(0, 360),
            'address': self._reverse_geocode(lat, lon),
        }
        self.satellites = random.randint(4, 12)

    def _reverse_geocode(self, lat, lon):
        """
        反向地理编码
        正式版应接入高德/百度地图API
        模拟版返回示例地址
        """
        # 简单模拟：根据经纬度粗略判断城市
        if 39.8 < lat < 40.2 and 116.2 < lon < 116.6:
            return "北京市朝阳区"
        elif 31.1 < lat < 31.4 and 121.3 < lon < 121.6:
            return "上海市浦东新区"
        elif 22.4 < lat < 22.7 and 113.9 < lon < 114.3:
            return "深圳市南山区"
        else:
            return f"经度 {lon:.4f}, 纬度 {lat:.4f}"

    def get_location_text(self):
        """获取格式化位置文本"""
        loc = self.location
        return (
            f"纬度: {loc['latitude']:.6f}\n"
            f"经度: {loc['longitude']:.6f}\n"
            f"海拔: {loc['altitude']:.1f} m\n"
            f"精度: {loc['accuracy']:.1f} m\n"
            f"速度: {loc['speed']:.1f} m/s\n"
            f"方向: {loc['bearing']:.1f}°\n"
            f"地址: {loc['address']}"
        )

    def cleanup(self):
        """清理GPS资源"""
        self.stop()