# 1. Import necessary components
from abc import abstractmethod

# --- FROM EX 5: THE METACLASS LOGIC ---
service_registry = {}

class ServiceMeta(type):
    def __new__(mcls, name, bases, namespace):
        if name != 'BaseServiceWithMeta':
            # Validation requirements
            if 'service_name' not in namespace:
                raise TypeError(f"Class '{name}' must define 'service_name'")
            if 'execute' not in namespace or not callable(namespace.get('execute')):
                raise TypeError(f"Class '{name}' must define 'execute' method")

        cls = super().__new__(mcls, name, bases, namespace)

        if name != 'BaseServiceWithMeta':
            # Using the service_name attribute as the key
            key = namespace.get('service_name')
            service_registry[key] = cls
            print(f"[METACLASS] Registered: {key}")
        return cls

class BaseServiceWithMeta(metaclass=ServiceMeta):
    @abstractmethod
    def execute(self, data):
        pass

# --- 2. DEFINING SERVICES (Bridges Ex 1 and Ex 5) ---

class PaymentService(BaseServiceWithMeta):
    service_name = "payment"  # Key for the registry
    
    def execute(self, data):
        print(f"  [EXECUTION] Processing {data} DH through Payment System.")

class NotificationService(BaseServiceWithMeta):
    service_name = "notification"
    
    def execute(self, data):
        print(f"  [EXECUTION] Sending notification: {data}")

class DeliveryService(BaseServiceWithMeta):
    service_name = "delivery"
    
    def execute(self, data):
        print(f"  [EXECUTION] Scheduling delivery for: {data}")

# --- 3. THE FACTORY ---

class ServiceFactory:
    @staticmethod
    def create_service(service_type: str):
        # We look up the service in the global registry populated by the metaclass
        service_class = service_registry.get(service_type.lower())
        
        if not service_class:
            return None
        return service_class()

# --- 4. INTERACTIVE TEST ---

def run_factory_test():
    print("--- 🏭 Dynamic Service Factory ---")
    
    while True:
        print(f"\nRegistered in Metaclass: {list(service_registry.keys())}")
        choice = input("Enter service type to create (or 'q' to quit): ").lower()

        if choice == 'q':
            break

        # The Factory handles the creation logic
        instance = ServiceFactory.create_service(choice)

        if instance:
            print(f"  [SUCCESS] Factory created object of type: {type(instance).__name__}")
            test_data = input("  Enter data to process: ")
            instance.execute(test_data)
        else:
            print(f"  [ERROR] No service found for '{choice}'")

if __name__ == "__main__":
    run_factory_test()