import streamlit as st
import time
import abc
from abc import ABC, abstractmethod
import datetime
import pandas as pd

# --- 0. STREAMLIT UI CONFIG ---
st.set_page_config(page_title="IISE Embedded Control Platform", layout="wide")

# Persistent State for Embedded System
if "system_logs" not in st.session_state:
    st.session_state.system_logs = []
if "perf_data" not in st.session_state:
    st.session_state.perf_data = []

# --- 1. SINGLETON MONITOR ---
class EmbeddedMonitor:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddedMonitor, cls).__new__(cls)
        return cls._instance

    def log(self, level, module, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        entry = {"Time": timestamp, "Level": level, "Module": module, "Message": message}
        st.session_state.system_logs.append(entry)

# --- 2. PERFORMANCE DECORATOR ---
def track_hw_performance(func):
    def wrapper(*args, **kwargs):
        monitor = EmbeddedMonitor()
        start = time.perf_counter()
        
        result = func(*args, **kwargs)
        
        end = time.perf_counter()
        duration_ms = (end - start) * 1000
        
        # Store for the chart
        st.session_state.perf_data.append({
            "Task": func.__name__, 
            "ms": round(duration_ms, 4),
            "Timestamp": datetime.datetime.now()
        })
        monitor.log("PERF", "Kernel", f"Task {func.__name__} finished in {duration_ms:.3f}ms")
        return result
    return wrapper

# --- 3. METACLASS REGISTRY ---
hw_registry = {}

class HardwareMeta(abc.ABCMeta):
    def __new__(mcls, name, bases, namespace):
        cls = super().__new__(mcls, name, bases, namespace)
        if name not in ["BaseHWService"]:
            h_type = namespace.get("hw_type", name.lower().replace("service", ""))
            hw_registry[h_type] = cls
        return cls

# --- 4. HARDWARE ABSTRACTION LAYER (HAL) ---
class BaseHWService(ABC, metaclass=HardwareMeta):
    @abstractmethod
    def self_test(self): pass

    @abstractmethod
    @track_hw_performance
    def run(self, params=None): pass

# --- 5. REGISTERED HARDWARE MODULES ---

class SensorReadingService(BaseHWService):
    hw_type = "sensor_array"
    def self_test(self): return True
    @track_hw_performance
    def run(self, params=None):
        time.sleep(0.05) # Simulate hardware latency
        return {"Temperature": 22.5, "Humidity": 45, "Status": "OK"}

class ActuatorService(BaseHWService):
    hw_type = "servo_actuator"
    def self_test(self): return True
    @track_hw_performance
    def run(self, params=None):
        time.sleep(0.12) # Simulate mechanical movement
        return f"Servo moved to {params}°"

class CommunicationService(BaseHWService):
    hw_type = "lora_wan"
    def self_test(self): return True
    @track_hw_performance
    def run(self, params=None):
        time.sleep(0.08) # Simulate network handshake
        return "Packet Sent: [ACK 0xFE]"

# --- 6. THE CONTROLLER ---
class SmartController:
    def __init__(self):
        self.monitor = EmbeddedMonitor()

    def execute_hardware_task(self, hw_key, data=None):
        service_cls = hw_registry.get(hw_key)
        if not service_cls:
            self.monitor.log("ERROR", "Factory", f"Module {hw_key} not found")
            return "Error"
        
        instance = service_cls()
        if instance.self_test():
            self.monitor.log("INFO", hw_key, "Hardware check passed.")
            return instance.run(data)
        return "Hardware Fault"

# --- 7. STREAMLIT DASHBOARD ---

st.title("🛰️ Smart Embedded Control Platform")
st.caption(f"Architect: Hamza Labbaalli | Track: IISE - Embedded Systems")

controller = SmartController()
monitor = EmbeddedMonitor()

# Layout
top_col1, top_col2 = st.columns([1, 2])

with top_col1:
    st.subheader("⚙️ Hardware Control")
    target_hw = st.selectbox("Select Hardware Module", list(hw_registry.keys()))
    
    # Contextual Input
    input_data = None
    if target_hw == "servo_actuator":
        input_data = st.slider("Target Angle", 0, 180, 90)
    
    if st.button("▶️ Execute Hardware Task"):
        with st.spinner(f"Interfacing with {target_hw}..."):
            result = controller.execute_hardware_task(target_hw, input_data)
            st.success(f"Output: {result}")

with top_col2:
    st.subheader("📊 Execution Timing (ms)")
    if st.session_state.perf_data:
        df_perf = pd.DataFrame(st.session_state.perf_data)
        st.line_chart(df_perf.set_index("Timestamp")["ms"])
    else:
        st.info("No execution data yet. Trigger a hardware task.")

st.divider()

# Bottom Row: Logs
st.subheader("📜 System Event Logs (Singleton Monitor)")
if st.session_state.system_logs:
    df_logs = pd.DataFrame(st.session_state.system_logs)
    
    # Color coding logs
    def color_logs(val):
        color = 'red' if val == 'ERROR' else 'green' if val == 'PERF' else 'white'
        return f'color: {color}'
    
    st.table(df_logs.iloc[::-1].style.applymap(color_logs, subset=['Level']))
else:
    st.write("Waiting for system events...")

if st.button("🗑️ Clear System Memory"):
    st.session_state.system_logs = []
    st.session_state.perf_data = []
    st.rerun()