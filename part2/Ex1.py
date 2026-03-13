from abc import ABC, abstractmethod

class BaseService(ABC):
    @abstractmethod
    def validate(self, data):
        pass

    @abstractmethod
    def calculate_result(self, data):
        pass

    @abstractmethod
    def get_description(self):
        pass

    def execute(self, data):
        if self.validate(data):
            result = self.calculate_result(data)
            print(f"Computed Result: {result}")
            return result
        else:
            print("Validation Failed: Invalid input data.")
            return None

    def start(self, data):
        print(f"\n[INFO] Starting {self.__class__.__name__}...")
        self.execute(data)

    def stop(self):
        print(f"[INFO] {self.__class__.__name__} execution finished.")

    def status(self):
        print(f"[STATUS] {self.__class__.__name__} is active.")

class PaymentService(BaseService):
    def validate(self, data):
        try:
            val = float(data)
            return val > 0
        except ValueError:
            return False

    def calculate_result(self, data):
        return float(data) * 0.02

    def get_description(self):
        return "Calculates a 2% transaction fee on a payment amount."

class NotificationService(BaseService):
    def validate(self, data):
        return len(str(data)) > 0

    def calculate_result(self, data):
        return len(str(data))

    def get_description(self):
        return "Calculates the character count of a message."

class DeliveryService(BaseService):
    def validate(self, data):
        try:
            val = float(data)
            return val >= 0
        except ValueError:
            return False

    def calculate_result(self, data):
        return float(data) * 5

    def get_description(self):
        return "Calculates delivery cost based on distance ($5/km)."

def run_user_test():
    services = {
        "1": PaymentService(),
        "2": NotificationService(),
        "3": DeliveryService()
    }

    while True:
        print("\n--- Service Interface Test ---")
        print("1. Payment Service")
        print("2. Notification Service")
        print("3. Delivery Service")
        print("4. Exit")
        
        choice = input("Select a service to test (1-4): ")

        if choice == "4":
            break
        
        service = services.get(choice)
        if service:
            print(f"\nDescription: {service.get_description()}")
            user_input = input("Enter data to process: ")
            
            # Running the lifecycle methods
            service.start(user_input)
            service.status()
            service.stop()
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    run_user_test()