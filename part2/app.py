import streamlit as st
import abc
from abc import ABC, abstractmethod
import datetime

# --- 0. STREAMLIT PAGE CONFIG ---
# Must be the very first Streamlit command
st.set_page_config(page_title="Smart Platform Manager", layout="wide")

# Ensure logs persist across Streamlit interactions
if "logs" not in st.session_state:
    st.session_state.logs = []

# --- 1. SINGLETON LOGGER (Requirement 2) ---
class Logger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        # Save to Streamlit's session state to prevent it from clearing
        st.session_state.logs.append(f"[{timestamp}] {message}")

# --- 2. STRATEGY PATTERN (Requirement 4) ---
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount): pass

class CreditCardStrategy(PaymentStrategy):
    def pay(self, amount): return f"Paid {amount:.2f} DH via Credit Card."

class CryptoStrategy(PaymentStrategy):
    def pay(self, amount): return f"Paid {amount:.2f} DH via Crypto Wallet."

# --- 3. METACLASS REGISTRY (Requirement 6) ---
service_registry = {}

class ServiceMeta(abc.ABCMeta):
    def __new__(mcls, name, bases, namespace):
        cls = super().__new__(mcls, name, bases, namespace)
        if name not in ["BaseService"]:
            s_type = namespace.get("service_type", name.lower().replace("service", ""))
            service_registry[s_type] = cls
        return cls

# --- 4. DECORATOR (Requirement 3) ---
def enrich_service(cls):
    cls.author = "Hamza Labbaalli"
    cls.version = "4.0.0"
    return cls

# --- 5. ABSTRACT INTERFACE (Requirement 5) ---
class BaseService(ABC, metaclass=ServiceMeta):
    @abstractmethod
    def validate(self, data): pass
    @abstractmethod
    def calculate_result(self, data): pass
    @abstractmethod
    def execute(self, data): pass
    @abstractmethod
    def get_description(self): pass

# --- 6. SERVICE CLASSES (The Concrete Implementations) ---

@enrich_service
class PaymentService(BaseService):
    service_type = "payment"
    def __init__(self): self.strategy = CreditCardStrategy()
    def validate(self, data):
        try: return float(data) > 0
        except: return False
    def calculate_result(self, data): return float(data) * 1.05
    def execute(self, data): return self.strategy.pay(data)
    def get_description(self): return "Financial Transaction Service"

@enrich_service
class NotificationService(BaseService):
    service_type = "notification"
    def validate(self, data): return len(str(data)) > 0
    def calculate_result(self, data): return len(str(data))
    def execute(self, data): return f"Notification sent: {data} characters."
    def get_description(self): return "System Alerting Service"

@enrich_service
class DeliveryService(BaseService):
    service_type = "delivery"
    def validate(self, data):
        try: return float(data) >= 0
        except: return False
    def calculate_result(self, data): return float(data) * 5.0
    def execute(self, data): return f"Delivery scheduled. Total Cost: {data:.2f} DH."
    def get_description(self): return "Logistics & Shipping Service"

@enrich_service
class ScholarshipService(BaseService):
    service_type = "scholarship"
    def validate(self, data):
        try: return 0 <= float(data) <= 20
        except: return False
    def calculate_result(self, data):
        score = float(data)
        return 2000 if score >= 16 else 1000
    def execute(self, data): return f"Scholarship Approved: {data} DH."
    def get_description(self): return "Academic Merit Service"

# --- 7. SMART PLATFORM MANAGER (The Integration Layer) ---
class SmartPlatformManager:
    def __init__(self):
        self.logger = Logger()
        self.factory = service_registry 

    def log_event(self, message):
        self.logger.log(message)

    def show_available_services(self):
        return list(self.factory.keys())

    def select_strategy(self, strategy_name):
        if strategy_name == "Crypto":
            return CryptoStrategy()
        return CreditCardStrategy()

    def run_service(self, service_type, **kwargs):
        self.log_event(f"Request started for: {service_type}")
        
        service_cls = self.factory.get(service_type)
        if not service_cls:
            return "Error: Service not found in Registry."

        instance = service_cls()
        
        # Handle Strategy for Payment
        if service_type == "payment" and kwargs.get("strat"):
            instance.strategy = self.select_strategy(kwargs.get("strat"))
            self.log_event(f"Strategy {kwargs.get('strat')} linked to PaymentService.")

        # Full Scenario Pipeline
        if instance.validate(kwargs.get("data")):
            self.log_event(f"Validation successful for {service_type}.")
            processed_data = instance.calculate_result(kwargs.get("data"))
            output = instance.execute(processed_data)
            self.log_event(f"Result: {output}")
            self.log_event(f"Service {service_type} execution completed.")
            return output
        else:
            self.log_event(f"Validation failed for input: {kwargs.get('data')}")
            return "Execution Error: Invalid Data Input."

# --- 8. UI RENDERER ---
st.title("🏗️ Smart Platform Manager")
st.markdown(f"**Architect:** {PaymentService.author} | **Version:** {PaymentService.version}")
st.divider()

platform = SmartPlatformManager()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🛠️ Operations Panel")
    selected_service = st.selectbox("Choose a Registered Service", platform.show_available_services())
    
    # Context-aware inputs
    if selected_service == "payment":
        prompt = "Enter Transaction Amount (DH):"
    elif selected_service == "notification":
        prompt = "Enter Message Content:"
    elif selected_service == "delivery":
        prompt = "Enter Distance (KM):"
    elif selected_service == "scholarship":
        prompt = "Enter Student Score (0-20):"
    else:
        prompt = "Enter Input Data:"
        
    user_data = st.text_input(prompt)
    
    strat_choice = None
    if selected_service == "payment":
        strat_choice = st.radio("Choose Payment Strategy", ["Credit Card", "Crypto"])

    if st.button("🚀 Run Platform Pipeline"):
        if not user_data:
            st.warning("Please provide input data.")
        else:
            with st.spinner('Processing...'):
                result = platform.run_service(selected_service, data=user_data, strat=strat_choice)
                st.info(result)

with col2:
    st.subheader("📜 Singleton System Logs")
    if st.button("🗑️ Clear Logs"):
        st.session_state.logs = []
        st.rerun()
        
    # Render logs from shared session state
    if not st.session_state.logs:
        st.write("No active logs.")
    else:
        for entry in reversed(st.session_state.logs):
            st.caption(entry)