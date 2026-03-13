class ServiceConfig:
    # 2. Class variable to track the number of objects
    config_count = 0

    # 3. Implement __new__: The actual creator
    def __new__(cls, *args, **kwargs):
        # 4. Print message for creation
        print(f"\n[STEP 1: __new__] Allocating memory for {cls.__name__} instance...")
        
        # Increment the shared counter
        cls.config_count += 1
        
        # Create the instance using the parent (object) class
        instance = super(ServiceConfig, cls).__new__(cls)
        return instance

    # 3. Implement __init__: The initializer
    def __init__(self, service_name, timeout, retries):
        # 5. Print message for initialization
        print(f"[STEP 2: __init__] Setting values for: {service_name}")
        
        self.service_name = service_name
        self.timeout = timeout
        self.retries = retries

# --- INTERACTIVE USER TESTING ---

def run_interactive_lifecycle():
    print("--- 🧬 Object Lifecycle Explorer ---")
    print("Watch how Python creates and then initializes objects.")

    while True:
        print(f"\nCurrent Object Count: {ServiceConfig.config_count}")
        cmd = input("\nCreate a new config? (y/n): ").lower()

        if cmd != 'y':
            print("\nFinal Report:")
            print(f"Total ServiceConfig objects in memory: {ServiceConfig.config_count}")
            print("Exiting...")
            break

        # User provides parameters for __init__
        name = input("Service Name (e.g., Database): ")
        try:
            to = int(input("Timeout (seconds): "))
            ret = int(input("Retries: "))
            
            # This line triggers both __new__ and __init__
            new_config = ServiceConfig(name, to, ret)
            
            print(f"Successfully built: {new_config.service_name} [TO: {new_config.timeout}s]")
        
        except ValueError:
            print("[Error] Please enter numbers for Timeout and Retries.")

if __name__ == "__main__":
    run_interactive_lifecycle()