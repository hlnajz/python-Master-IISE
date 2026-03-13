import abc
from abc import ABC, abstractmethod

# --- 1. SINGLETON LOGGER ---
class Logger:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.logs = []
        return cls._instance

    def log(self, message):
        self.logs.append(message)
        print(f"  [LOG] {message}")

# --- 2. STRATEGY PATTERN ---
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount): pass

class CreditCardStrategy(PaymentStrategy):
    def pay(self, amount): return f"Paid {amount:.2f} DH via Credit Card."

class CryptoStrategy(PaymentStrategy):
    def pay(self, amount): return f"Paid {amount:.2f} DH via Crypto Wallet."

# --- 3. METACLASS REGISTRY ---
service_registry = {}

class ServiceMeta(abc.ABCMeta):
    def __new__(mcls, name, bases, namespace):
        cls = super().__new__(mcls, name, bases, namespace)
        if name not in ["BaseService"]:
            s_type = namespace.get("service_type", name.lower().replace("service", ""))
            service_registry[s_type] = cls
        return cls

# --- 4. DECORATOR ---
def enrich_service(cls):
    cls.author = "Hamza Labbaalli"
    cls.version = "4.0.0"
    return cls

# --- 5. ABSTRACT INTERFACE ---
class BaseService(ABC, metaclass=ServiceMeta):
    @abstractmethod
    def validate(self, data): pass
    @abstractmethod
    def calculate_result(self, data): pass
    @abstractmethod
    def execute(self, data): pass
    @abstractmethod
    def get_description(self): pass

# --- 6. SERVICE CLASSES ---
@enrich_service
class PaymentService(BaseService):
    service_type = "payment"
    def __init__(self): self.strategy = CreditCardStrategy()
    def validate(self, data):
        try: return float(data) > 0
        except: return False
    def calculate_result(self, data): return float(data) * 1.05
    def execute(self, data): return self.strategy.pay(data)
    def get_description(self): return "Financial Service (DH)"

@enrich_service
class NotificationService(BaseService):
    service_type = "notification"
    def validate(self, data): return len(str(data)) > 0
    def calculate_result(self, data): return len(str(data))
    def execute(self, data): return f"Notification sent: {data} chars."
    def get_description(self): return "Alerting Service"

# --- 7. SMART PLATFORM MANAGER ---
class SmartPlatformManager:
    def __init__(self):
        self.logger = Logger()
        self.factory = service_registry 

    def log_event(self, message):
        self.logger.log(message)

    def show_available_services(self):
        print("\n--- Available Services ---")
        for i, s in enumerate(self.factory.keys(), 1):
            print(f"{i}. {s.capitalize()}")

    def select_strategy(self, strategy_name):
        if strategy_name == "2":
            return CryptoStrategy()
        return CreditCardStrategy()

    def register_request(self, service_type, **kwargs):
        self.log_event(f"Registering request for {service_type}...")
        return {"type": service_type, "data": kwargs.get("data"), "strat": kwargs.get("strat")}

    def run_service(self, service_type, **kwargs):
        req = self.register_request(service_type, **kwargs)
        service_cls = self.factory.get(req["type"])
        
        if not service_cls:
            self.log_event("Error: Service not found.")
            return

        instance = service_cls()
        
        if req["type"] == "payment" and req["strat"]:
            instance.strategy = self.select_strategy(req["strat"])
            self.log_event(f"Strategy linked to instance.")

        if instance.validate(req["data"]):
            self.log_event("Validation successful.")
            processed = instance.calculate_result(req["data"])
            output = instance.execute(processed)
            print(f"\n>>> RESULT: {output}")
            self.log_event(f"Execution Output: {output}")
            self.log_event(f"Service {service_type} stopped.")
        else:
            self.log_event("Validation failed. Check your input.")

# --- 8. INTERACTIVE TEST SYSTEM ---
def main():
    platform = SmartPlatformManager()
    print(f"Platform by: {PaymentService.author} | Version: {PaymentService.version}")

    while True:
        platform.show_available_services()
        choice = input("\nSelect a service to test (or 'q' to quit): ").lower()

        if choice == 'q':
            print("Exiting Platform. Goodbye!")
            break

        service_list = list(service_registry.keys())
        try:
            # Convert numeric choice to service key
            idx = int(choice) - 1
            service_key = service_list[idx]
        except (ValueError, IndexError):
            print("Invalid selection.")
            continue

        user_data = input(f"Enter data for {service_key.capitalize()}: ")
        
        strat_choice = None
        if service_key == "payment":
            print("1. Credit Card")
            print("2. Crypto")
            strat_choice = input("Select Strategy (1/2): ")

        # Run the full pipeline
        print("\n--- Executing Platform Pipeline ---")
        platform.run_service(service_key, data=user_data, strat=strat_choice)
        print("-----------------------------------\n")

if __name__ == "__main__":
    main()