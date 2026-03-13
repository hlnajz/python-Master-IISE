from Ex1 import BaseService, PaymentService, NotificationService, DeliveryService

# 1. Global dictionary to act as the registry
service_registry = {}

# 2. Class decorator to register the service
def register_service(cls):
    # Using the class name as the key and the class object as the value
    service_registry[cls.__name__] = cls
    return cls

# 3. Applying the decorator
PaymentService = register_service(PaymentService)
NotificationService = register_service(NotificationService)
DeliveryService = register_service(DeliveryService)

def interactive_registry_test():
    print("--- 🛠️ Service Registry Platform ---")
    
    # List registered services
    print(f"Total Services Found: {len(service_registry)}")
    for i, name in enumerate(service_registry.keys(), 1):
        print(f"{i}. {name}")

    while True:
        choice = input("\nEnter the Service Name to execute (or 'q' to quit): ")

        if choice.lower() == 'q':
            print("Exiting Registry Test.")
            break

        # 6. Dynamic instantiation based on user input
        if choice in service_registry:
            # Retrieve the class object from the dictionary
            ServiceClass = service_registry[choice]
            
            print(f"\n[SYSTEM] Instantiating {choice}...")
            instance = ServiceClass()
            
            # Request test data
            test_data = input(f"Enter numeric data for {choice}: ")
            try:
                numeric_data = float(test_data)
                
                # Execute lifecycle (Methods from Ex1)
                instance.start(numeric_data)
                instance.status()
                instance.stop()
            except ValueError:
                print("[ERROR] Please enter a valid number for this test.")
        else:
            print(f"[ERROR] '{choice}' is not in the registry. Remember, names are case-sensitive.")

if __name__ == "__main__":
    interactive_registry_test()