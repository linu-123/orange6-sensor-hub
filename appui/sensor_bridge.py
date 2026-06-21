"""
传感器JNI桥接模块
通过 pyjnius 调用 Android Java SensorManager API
实现在 Python/Kivy 中读取全部内置传感器数据
"""

from kivy.logger import Logger
from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import (
    NumericProperty, StringProperty, DictProperty,
    BooleanProperty, ListProperty
)

try:
    from jnius import autoclass, PythonJavaClass, java_method, cast
    JNIUS_AVAILABLE = True
except ImportError:
    JNIUS_AVAILABLE = False
    Logger.warning("SensorBridge: jnius not available, using mock sensors")


# 传感器类型常量 (Android API)
SENSOR_TYPES = {
    'accelerometer': 1,    # TYPE_ACCELEROMETER
    'gyroscope': 4,        # TYPE_GYROSCOPE
    'magnetic_field': 2,   # TYPE_MAGNETIC_FIELD
    'light': 5,            # TYPE_LIGHT
    'proximity': 8,        # TYPE_PROXIMITY
    'pressure': 6,         # TYPE_PRESSURE
    'humidity': 12,        # TYPE_RELATIVE_HUMIDITY
    'temperature': 13,     # TYPE_AMBIENT_TEMPERATURE
    'gravity': 9,          # TYPE_GRAVITY
    'linear_acceleration': 10,  # TYPE_LINEAR_ACCELERATION
    'rotation_vector': 11,      # TYPE_ROTATION_VECTOR
    'step_counter': 19,         # TYPE_STEP_COUNTER
    'heart_rate': 21,           # TYPE_HEART_RATE
    'significant_motion': 17,   # TYPE_SIGNIFICANT_MOTION
}

SENSOR_NAMES_CN = {
    'accelerometer': '加速度传感器',
    'gyroscope': '陀螺仪',
    'magnetic_field': '地磁传感器',
    'light': '光线传感器',
    'proximity': '距离传感器',
    'pressure': '气压传感器',
    'humidity': '湿度传感器',
    'temperature': '温度传感器',
    'gravity': '重力传感器',
    'linear_acceleration': '线性加速度',
    'rotation_vector': '旋转向量',
    'step_counter': '计步器',
    'heart_rate': '心率传感器',
    'significant_motion': '显著运动',
}

SENSOR_UNITS = {
    'accelerometer': 'm/s²',
    'gyroscope': 'rad/s',
    'magnetic_field': 'μT',
    'light': 'lux',
    'proximity': 'cm',
    'pressure': 'hPa',
    'humidity': '%',
    'temperature': '°C',
    'gravity': 'm/s²',
    'linear_acceleration': 'm/s²',
    'rotation_vector': '',
    'step_counter': '步',
    'heart_rate': 'bpm',
    'significant_motion': '',
}

SENSOR_ICONS = {
    'accelerometer': '📐',
    'gyroscope': '🌀',
    'magnetic_field': '🧲',
    'light': '☀️',
    'proximity': '📏',
    'pressure': '🌡',
    'humidity': '💧',
    'temperature': '🌡',
    'gravity': '⬇️',
    'linear_acceleration': '🚀',
    'rotation_vector': '🔄',
    'step_counter': '🚶',
    'heart_rate': '❤️',
    'significant_motion': '💥',
}


class SensorListener(PythonJavaClass):
    """
    Android SensorEventListener 的 Python 实现
    通过 pyjnius 注册到 Java 层接收传感器数据回调
    """
    __javainterfaces__ = ['android/hardware/SensorEventListener']

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    @java_method('(Landroid/hardware/SensorEvent;)V')
    def onSensorChanged(self, event):
        """传感器数据变化回调"""
        if self.callback:
            sensor_type = event.sensor.getType()
            values = list(event.values)
            timestamp = event.timestamp
            self.callback(sensor_type, values, timestamp)

    @java_method('(Landroid/hardware/Sensor;I)V')
    def onAccuracyChanged(self, sensor, accuracy):
        """传感器精度变化回调"""
        pass


class MockSensorData:
    """当无法使用 jnius 时，模拟传感器数据用于桌面测试"""
    def __init__(self):
        import random
        import math
        self.random = random
        self.math = math
        self._values = {}
        self._t = 0

    def get_values(self, sensor_type):
        self._t += 0.05
        t = self._t
        r = self.random
        data = {
            1:  (r.uniform(-9.8, 9.8), r.uniform(-9.8, 9.8), r.uniform(-9.8, 9.8)),
            4:  (r.uniform(-5, 5), r.uniform(-5, 5), r.uniform(-5, 5)),
            2:  (r.uniform(-50, 50), r.uniform(-50, 50), r.uniform(-50, 50)),
            5:  (r.uniform(0, 1000),),
            8:  (r.uniform(0, 10),),
            6:  (r.uniform(950, 1050),),
            12: (r.uniform(30, 80),),
            13: (r.uniform(15, 35),),
            9:  (0, 0, -9.8),
            10: (r.uniform(-2, 2), r.uniform(-2, 2), r.uniform(-2, 2)),
            11: (r.uniform(-1, 1), r.uniform(-1, 1), r.uniform(-1, 1), r.uniform(0, 1)),
            19: (r.randint(0, 3),),
            21: (r.randint(60, 100),),
            17: (r.randint(0, 1),),
        }
        return data.get(sensor_type, (0,))


class SensorManagerBridge(EventDispatcher):
    """
    传感器管理器桥接类
    统一管理所有传感器的注册、监听、数据分发
    """

    # Kivy Properties 用于 UI 绑定
    accelerometer = ListProperty([0, 0, 0])
    gyroscope = ListProperty([0, 0, 0])
    magnetic_field = ListProperty([0, 0, 0])
    light = NumericProperty(0)
    proximity = NumericProperty(0)
    pressure = NumericProperty(0)
    humidity = NumericProperty(0)
    temperature = NumericProperty(0)
    gravity = ListProperty([0, 0, 0])
    linear_acceleration = ListProperty([0, 0, 0])
    rotation_vector = ListProperty([0, 0, 0, 0])
    step_counter = NumericProperty(0)
    heart_rate = NumericProperty(0)
    significant_motion = NumericProperty(0)

    # 状态属性
    sensor_status = DictProperty({})  # {sensor_name: True/False}
    gps_location = DictProperty({
        'latitude': 0.0,
        'longitude': 0.0,
        'altitude': 0.0,
        'accuracy': 0.0,
        'address': '未知位置',
    })
    battery_level = NumericProperty(100)
    battery_charging = BooleanProperty(False)
    is_connected = BooleanProperty(False)

    # 事件
    sensor_updated = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._listeners = {}
        self._java_bridge = None
        self._mock = None

        if JNIUS_AVAILABLE:
            self._init_java_bridge()
        else:
            Logger.info("SensorBridge: Using mock sensor data for desktop testing")
            self._mock = MockSensorData()
            self.is_connected = True
            Clock.schedule_interval(self._mock_update, 0.1)

        # 初始化所有传感器状态
        for name in SENSOR_TYPES:
            self.sensor_status[name] = False

    def _init_java_bridge(self):
        """初始化Java层桥接"""
        try:
            self.PythonActivity = autoclass('org.kivy.android.PythonActivity')
            self.Context = autoclass('android.content.Context')
            self.SensorManager = autoclass('android.hardware.SensorManager')
            self.Sensor = autoclass('android.hardware.Sensor')

            activity = self.PythonActivity.mActivity
            self._sensor_manager = activity.getSystemService(
                self.Context.SENSOR_SERVICE
            )

            # 注册所有可用传感器
            self._register_all_sensors()
            self.is_connected = True
            Logger.info("SensorBridge: Java bridge initialized successfully")

        except Exception as e:
            Logger.error(f"SensorBridge: Failed to init Java bridge: {e}")
            self.is_connected = False

    def _register_all_sensors(self):
        """注册所有可用传感器"""
        from jnius import PythonJavaClass

        # 为每个传感器类型创建监听器
        for name, type_code in SENSOR_TYPES.items():
            try:
                sensor = self._sensor_manager.getDefaultSensor(type_code)
                if sensor is not None:
                    # 创建回调闭包
                    def make_callback(name, type_code):
                        def callback(sensor_type, values, timestamp):
                            if sensor_type == type_code:
                                self._on_sensor_data(name, values)
                        return callback

                    listener = SensorListener(make_callback(name, type_code))
                    self._sensor_manager.registerListener(
                        listener,
                        sensor,
                        self.SensorManager.SENSOR_DELAY_NORMAL
                    )
                    self._listeners[name] = listener
                    self.sensor_status[name] = True
                    Logger.info(f"SensorBridge: Registered {name}")
                else:
                    self.sensor_status[name] = False
                    Logger.info(f"SensorBridge: {name} not available on this device")
            except Exception as e:
                self.sensor_status[name] = False
                Logger.warning(f"SensorBridge: Failed to register {name}: {e}")

    def _on_sensor_data(self, name, values):
        """接收传感器数据并更新Kivy属性"""
        if name == 'accelerometer':
            self.accelerometer = list(values[:3])
        elif name == 'gyroscope':
            self.gyroscope = list(values[:3])
        elif name == 'magnetic_field':
            self.magnetic_field = list(values[:3])
        elif name == 'light':
            self.light = float(values[0]) if values else 0
        elif name == 'proximity':
            self.proximity = float(values[0]) if values else 0
        elif name == 'pressure':
            self.pressure = float(values[0]) if values else 0
        elif name == 'humidity':
            self.humidity = float(values[0]) if values else 0
        elif name == 'temperature':
            self.temperature = float(values[0]) if values else 0
        elif name == 'gravity':
            self.gravity = list(values[:3])
        elif name == 'linear_acceleration':
            self.linear_acceleration = list(values[:3])
        elif name == 'rotation_vector':
            self.rotation_vector = list(values[:4])
        elif name == 'step_counter':
            self.step_counter = int(values[0]) if values else 0
        elif name == 'heart_rate':
            self.heart_rate = float(values[0]) if values else 0
        elif name == 'significant_motion':
            self.significant_motion = int(values[0]) if values else 0

        self.sensor_updated = name

    def _mock_update(self, dt):
        """模拟传感器数据更新（桌面测试用）"""
        if not self._mock:
            return
        for name, type_code in SENSOR_TYPES.items():
            values = self._mock.get_values(type_code)
            self._on_sensor_data(name, values)
            self.sensor_status[name] = True

        # 模拟GPS
        import random
        self.gps_location = {
            'latitude': 39.9042 + random.uniform(-0.01, 0.01),
            'longitude': 116.4074 + random.uniform(-0.01, 0.01),
            'altitude': random.uniform(10, 100),
            'accuracy': random.uniform(5, 20),
            'address': '北京市朝阳区模拟测试位置',
        }

        # 模拟电池
        self.battery_level = random.uniform(50, 100)
        self.battery_charging = random.choice([True, False])

    def get_sensor_display_value(self, name):
        """获取格式化后的传感器显示值"""
        if name == 'accelerometer':
            v = self.accelerometer
            return f"X: {v[0]:+.1f}  Y: {v[1]:+.1f}  Z: {v[2]:+.1f}"
        elif name == 'gyroscope':
            v = self.gyroscope
            return f"X: {v[0]:+.2f}  Y: {v[1]:+.2f}  Z: {v[2]:+.2f}"
        elif name == 'magnetic_field':
            v = self.magnetic_field
            return f"X: {v[0]:+.1f}  Y: {v[1]:+.1f}  Z: {v[2]:+.1f}"
        elif name == 'light':
            return f"{self.light:.0f}"
        elif name == 'proximity':
            return f"{self.proximity:.1f}"
        elif name == 'pressure':
            return f"{self.pressure:.1f}"
        elif name == 'humidity':
            return f"{self.humidity:.0f}"
        elif name == 'temperature':
            return f"{self.temperature:.1f}"
        elif name == 'gravity':
            v = self.gravity
            return f"X: {v[0]:+.1f}  Y: {v[1]:+.1f}  Z: {v[2]:+.1f}"
        elif name == 'linear_acceleration':
            v = self.linear_acceleration
            return f"X: {v[0]:+.2f}  Y: {v[1]:+.2f}  Z: {v[2]:+.2f}"
        elif name == 'rotation_vector':
            v = self.rotation_vector
            if len(v) >= 4:
                return f"({v[0]:.2f}, {v[1]:.2f}, {v[2]:.2f}, {v[3]:.2f})"
            return str(v)
        elif name == 'step_counter':
            return f"{int(self.step_counter)}"
        elif name == 'heart_rate':
            return f"{self.heart_rate:.0f}"
        elif name == 'significant_motion':
            return "是" if self.significant_motion else "否"
        return "—"

    def get_sensor_status_color(self, name):
        """获取传感器状态颜色（绿/红）"""
        status = self.sensor_status.get(name, False)
        return (0.2, 0.8, 0.2, 1) if status else (0.8, 0.2, 0.2, 1)

    def cleanup(self):
        """清理传感器资源"""
        if JNIUS_AVAILABLE and hasattr(self, '_sensor_manager'):
            for listener in self._listeners.values():
                try:
                    self._sensor_manager.unregisterListener(listener)
                except:
                    pass
            self._listeners.clear()
            Logger.info("SensorBridge: Cleaned up all sensor listeners")
        if self._mock:
            Clock.unschedule(self._mock_update)