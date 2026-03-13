import types

# 1. & 7. Creating the Metaclass and the Registry
service_registry = {}

class ServiceMeta(type):
    # 2. Implement __new__ to control class creation
    def __new__(mcls, name, bases, namespace):
        # We skip validation for the Base class itself
        if name != 'BaseServiceWithMeta':
            # 3. & 4. Validate presence of service_name and execute method
            if 'service_name' not in namespace:
                raise TypeError(f"Class '{name}' must define a class attribute 'service_name'")
            
            if 'execute' not in namespace or not callable(namespace.get('execute')):
                raise TypeError(f"Class '{name}' must define a method named 'execute'")

        # Create the class
        cls = super().__new__(mcls, name, bases, namespace)

        # 7. Automatically register the class (excluding the base)
        if name != 'BaseServiceWithMeta':
            service_registry[namespace.get('service_name')] = cls
            print(f"  [METACLASS] Successfully created and registered: {name}")

        return cls

# A base class using the metaclass to propagate requirements to subclasses
class BaseServiceWithMeta(metaclass=ServiceMeta):
    pass

# --- INTERACTIVE TESTING ---

def run_metaclass_test():
    print("--- 🧠 Metaclass Validation Lab ---")
    print("Metaclasses enforce rules at 'Definition Time'.")

    # Scenario 1: Pre-defined Valid Class
    print("\n[SCENARIO 1] Defining 'ValidPaymentService' in code...")
    class ValidPaymentService(BaseServiceWithMeta):
        service_name = "Payment_Service"
        def execute(self, data):
            print(f"Processing {data} DH")

    # Scenario 2: User-driven Dynamic Creation
    print("\n[SCENARIO 2] Testing the 'Fail-Fast' mechanism.")
    print("Current Registry:", list(service_registry.keys()))
    
    test_input = input("\nReady to test an invalid class definition? (y/n): ").lower()
    if test_input == 'y':
        print("\nAttempting to define 'BrokenService' without 'execute' method...")
        try:
            # We use type() or a dynamic class block to simulate defining a bad class
            class BrokenService(BaseServiceWithMeta):
                service_name = "Broken_Service"
                # Missing execute() method!
        except TypeError as e:
            print(f"  [CAUGHT ERROR] Definition blocked: {e}")

    # Scenario 3: Final Inspection
    print("\n[SCENARIO 3] Final Registry Check")
    if service_registry:
        for s_name, s_cls in service_registry.items():
            print(f"  - Service: {s_name} | Class: {s_cls.__name__}")

if __name__ == "__main__":
    run_metaclass_test()