import random

# 1. Logger Mixin
class LoggerMixin:
    def log(self, message):
        print(f"[LOG - {self.__class__.__name__}]: {message}")

# 2. Base Class Sensor
class Sensor(LoggerMixin):
    def __init__(self, sensor_id, name):
        self.__id = sensor_id
        self.__name = name
        self.__value = 0.0

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        # Basic validation: ensure value is a number
        if isinstance(new_value, (int, float)):
            self.__value = new_value
        else:
            raise ValueError("Sensor value must be a number.")

    def read_value(self):
        """Method to be overridden by derived classes"""
        pass

# 3. Derived Classes
class TemperatureSensor(Sensor):
    def read_value(self):
        # Simulate reading temperature
        self.value = round(random.uniform(20.0, 30.0), 2)
        self.log(f"Read temperature: {self.value}°C")
        return self.value

class PressureSensor(Sensor):
    def read_value(self):
        # Simulate reading pressure
        self.value = round(random.uniform(1000.0, 1020.0), 2)
        self.log(f"Read pressure: {self.value} hPa")
        return self.value

class MotionSensor(Sensor):
    def read_value(self):
        # Simulate motion detection (True/False, converted to 1/0)
        self.value = float(random.choice([True, False]))
        self.log(f"Motion detected: {bool(self.value)}")
        return self.value

# 4. Sensor System Management
class SensorSystem:
    def __init__(self):
        self.sensors = []

    def add_sensor(self, sensor):
        if isinstance(sensor, Sensor):
            self.sensors.append(sensor)
        else:
            print("Invalid sensor object.")

    def read_all_sensors(self):
        print("\n--- Initiating System-Wide Sensor Read ---")
        readings = {}
        for sensor in self.sensors:
            # Polymorphism: calling read_value() on different types
            readings[sensor.name] = sensor.read_value()
        print("--- Read Complete ---\n")
        return readings

# 5. Testing and Demonstration
if __name__ == "__main__":
    # Create sensors
    temp = TemperatureSensor("T01", "Main Room Temp")
    press = PressureSensor("P01", "Barometer")
    motion = MotionSensor("M01", "Hallway Motion")

    # Initialize system
    system = SensorSystem()
    system.add_sensor(temp)
    system.add_sensor(press)
    system.add_sensor(motion)

    # Demonstrate polymorphic behavior and logging
    system.read_all_sensors()

    # Demonstrate encapsulation via properties
    print(f"Direct access check: {temp.name} is currently reading {temp.value}")