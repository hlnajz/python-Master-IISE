from Ex1 import BaseService

# --- 1. & 2. THE SINGLETON LOGGER ---
class Logger:
    _instance = None  # Class variable to store the unique instance

    def __new__(cls, *args, **kwargs):
        # 3. Use __new__ to ensure only one instance exists
        if cls._instance is None:
            print("\n  [SYSTEM] First call: Allocating the Unique Logger Instance...")
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.history = [] # Initialize a shared history list
        return cls._instance

    def log(self, message):
        self.history.append(message)
        print(f"  [LOG]: {message}")

# --- 6. INTEGRATING INTO SERVICES ---
class MonitoredService(BaseService):
    def __init__(self, name):
        self.name = name
        self.logger = Logger() # Every service gets the same instance

    def validate(self, data): return True
    def calculate_result(self, data): return data
    def get_description(self): return f"Service: {self.name}"

    def start(self, data):
        self.logger.log(f"Starting {self.name} with: {data}")
        # Assuming Ex1 has a status/start logic
        print(f"  [STATUS] {self.name} is running.")

# --- INTERACTIVE TESTING ---

def run_singleton_test():
    print("--- 🛡️ Singleton pattern Lab ---")
    
    # Proof of Identity
    print("Creating three logger variables...")
    l1, l2, l3 = Logger(), Logger(), Logger()
    
    print(f"  ID 1: {id(l1)}")
    print(f"  ID 2: {id(l2)}")
    print(f"  ID 3: {id(l3)}")
    print(f"  Are they the same object? {l1 is l2 is l3}")

    # Interactive logging across multiple "Services"
    print("\n--- Testing Global Shared State ---")
    s1 = MonitoredService("PaymentGate")
    s2 = MonitoredService("EmailNotifier")

    while True:
        print("\n1. Log from PaymentGate")
        print("2. Log from EmailNotifier")
        print("3. View Shared History")
        print("q. Quit")
        
        choice = input("\nSelect action (1/2/3/q): ")

        if choice == '1':
            s1.start("Transaction_233")
        elif choice == '2':
            s2.start("Alert_001")
        elif choice == '3':
            print("\nShared Logger History:")
            for i, msg in enumerate(l1.history, 1):
                print(f"  {i}. {msg}")
        elif choice == 'q':
            break

if __name__ == "__main__":
    run_singleton_test()