import streamlit as st
import random
from datetime import datetime

# ==========================================
# BACKEND LOGIC: OOP Architecture
# ==========================================

# 1. Mixin Class (for Multiple Inheritance)
class LoggerMixin:
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        return f"[{timestamp} LOG] {message}"

# 2. Base Class (Encapsulation & Properties)
class Sensor:
    def __init__(self, sensor_id, name):
        # Private attributes
        self.__sensor_id = sensor_id
        self.__name = name
        self.__current_value = None

    # Properties for controlled access
    @property
    def sensor_id(self):
        return self.__sensor_id

    @property
    def name(self):
        return self.__name

    @property
    def current_value(self):
        return self.__current_value

    @current_value.setter
    def current_value(self, value):
        self.__current_value = value

    def read_value(self):
        raise NotImplementedError("Subclasses must implement read_value()")

# 3. Derived Classes (Inheritance & Multiple Inheritance)
class TemperatureSensor(Sensor, LoggerMixin):
    def read_value(self):
        # Simulate reading a temperature
        self.current_value = round(random.uniform(-10.0, 45.0), 2)
        return self.log(f"{self.name} (Temp): {self.current_value} °C")

class PressureSensor(Sensor, LoggerMixin):
    def read_value(self):
        # Simulate reading pressure
        self.current_value = round(random.uniform(980.0, 1050.0), 2)
        return self.log(f"{self.name} (Pressure): {self.current_value} hPa")

class MotionSensor(Sensor, LoggerMixin):
    def read_value(self):
        # Simulate motion detection
        self.current_value = random.choice([True, False])
        state = "Motion Detected!" if self.current_value else "Clear"
        return self.log(f"{self.name} (Motion): {state}")

# 4. Manager Class (Polymorphism)
class SensorSystem:
    def __init__(self):
        self.sensors = []

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def read_all(self):
        # Polymorphism in action: calling read_value() on different objects
        # without needing to know their specific class.
        return [sensor.read_value() for sensor in self.sensors]


# ==========================================
# FRONTEND UI (Streamlit)
# ==========================================
st.set_page_config(page_title="Embedded Sensor System", layout="centered")

st.title("📡 Embedded Sensor Management System")
st.markdown("**IISE Problematic - Built by Hamza**")
st.divider()

# Initialize the Sensor System in session state so it persists
if 'system' not in st.session_state:
    sys = SensorSystem()
    # Pre-load some sensors
    sys.add_sensor(TemperatureSensor("T-01", "Engine Temp"))
    sys.add_sensor(PressureSensor("P-01", "Hydraulic Pressure"))
    sys.add_sensor(MotionSensor("M-01", "Perimeter Motion"))
    st.session_state['system'] = sys

# --- Dashboard UI ---
st.subheader("Central Control Panel")

# The "Polymorphic" Button
if st.button("🔄 Read All Sensors (Trigger Polymorphism)", use_container_width=True):
    with st.spinner("Fetching data from embedded network..."):
        readings = st.session_state['system'].read_all()
        
        st.success("Data retrieved successfully!")
        
        # Display the logs
        with st.container(border=True):
            for reading in readings:
                st.code(reading, language="log")

st.divider()

# --- Add New Sensor UI ---
st.subheader("Add New Sensor")
col1, col2, col3 = st.columns(3)

with col1:
    s_id = st.text_input("Sensor ID", value=f"S-{random.randint(10, 99)}")
with col2:
    s_name = st.text_input("Sensor Name", value="New Sensor")
with col3:
    s_type = st.selectbox("Sensor Type", ["Temperature", "Pressure", "Motion"])

if st.button("➕ Register Sensor"):
    if s_type == "Temperature":
        new_sensor = TemperatureSensor(s_id, s_name)
    elif s_type == "Pressure":
        new_sensor = PressureSensor(s_id, s_name)
    else:
        new_sensor = MotionSensor(s_id, s_name)
        
    st.session_state['system'].add_sensor(new_sensor)
    st.toast(f"{s_type} sensor '{s_name}' added to the network!")
    st.rerun()

# --- Display Registered Sensors ---
with st.expander("View Registered Sensors Details"):
    for s in st.session_state['system'].sensors:
        st.write(f"- **{s.sensor_id}**: {s.name} *(Class: {s.__class__.__name__})*")