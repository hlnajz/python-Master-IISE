from Ex1 import BaseService

# --- DECORATORS ---

def add_version(cls):
    cls.version = "1.0.0"
    return cls

def add_author(cls):
    cls.author = "Hamza Labbaalli"
    return cls

def add_category(cls):
    cls.category = "Middleware Service"
    return cls

def add_class_name(cls):
    cls.class_name = cls.__name__
    return cls

def add_display_info(cls):
    def display_info(self):
        print(f"\n--- METADATA [Ref: {getattr(self, 'class_name', 'Service')}] ---")
        print(f"  Author:   {getattr(self, 'author', 'N/A')}")
        print(f"  Version:  {getattr(self, 'version', 'N/A')}")
        print(f"  Category: {getattr(self, 'category', 'N/A')}")
        print(f"  Desc:     {self.get_description()}")
        print("-" * 40)
    cls.display_info = display_info
    return cls

# --- CONCRETE CLASSES ---

@add_display_info
@add_class_name
@add_category
@add_author
@add_version
class PaymentService(BaseService):
    def validate(self, data):
        try: return float(data) > 0
        except: return False
    def calculate_result(self, data):
        return float(data) * 0.02
    def get_description(self):
        return "Calculates transaction fees (2% in DH)."

@add_display_info
@add_class_name
@add_category
@add_author
@add_version
class NotificationService(BaseService):
    def validate(self, data):
        return len(str(data)) > 0
    def calculate_result(self, data):
        return len(str(data))
    def get_description(self):
        return "Calculates message character length."

# --- INTERACTIVE TESTING ---

def run_interactive_test():
    services = {
        "1": PaymentService(),
        "2": NotificationService()
    }

    print(f"Decorator Test Platform | Architect: {PaymentService.author}")
    
    while True:
        print("\nAvailable Services:")
        print("1. Payment Service")
        print("2. Notification Service")
        print("q. Quit")
        
        choice = input("\nSelect service to inspect (1/2/q): ").lower()
        
        if choice == 'q':
            break
        
        if choice in services:
            service = services[choice]
            
            # 1. Test the method injected by @add_display_info
            service.display_info()
            
            # 2. Test the core logic
            val = input(f"Enter test data for {service.class_name}: ")
            
            if service.validate(val):
                res = service.calculate_result(val)
                print(f"  [RESULT] Processed value: {res}")
            else:
                print("  [ERROR] Validation failed for input.")
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    run_interactive_test()