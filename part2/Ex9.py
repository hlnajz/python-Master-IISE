from abc import ABC, abstractmethod

# --- 1. ABSTRACTIONS (DIP & ISP) ---
class IService(ABC):
    @abstractmethod
    def validate(self, data): pass
    
    @abstractmethod
    def calculate_result(self, data): pass
    
    @abstractmethod
    def execute(self, data): pass
    
    @abstractmethod
    def get_description(self): pass

# --- 2. REFACTORED CORE (SRP & DIP) ---
class ServiceEngine:
    """
    High-level module. It doesn't know the logic of the services,
    it only knows the interface defined by IService.
    """
    def __init__(self, service: IService):
        self.service = service

    def run(self, data):
        print(f"\n[ENGINE] Initializing: {self.service.get_description()}")
        print(f"[ENGINE] Validating input: {data}")
        
        if self.service.validate(data):
            print("[ENGINE] Validation Successful. Calculating...")
            result = self.service.calculate_result(data)
            self.service.execute(result)
        else:
            print("[ENGINE] Validation Failed. Process Aborted.")

# --- 3. THE NEW SERVICE (OCP) ---
class ScholarshipService(IService):
    def validate(self, data):
        try:
            score = float(data)
            return 0 <= score <= 20
        except:
            return False

    def calculate_result(self, data):
        # Moroccan grading logic: 16/20 is 'Très Bien'
        score = float(data)
        return 2000 if score >= 16 else 1000

    def execute(self, data):
        print(f"  [ACTION] Grant of {data} DH approved for the student.")

    def get_description(self):
        return "National Excellence Scholarship Manager"

# --- INTERACTIVE TESTING ---

def run_interactive_solid():
    # Plug the specific service into the generic engine
    scholarship_app = ScholarshipService()
    engine = ServiceEngine(scholarship_app)

    print("--- 🏛️ SOLID Architecture Lab ---")
    print("Testing: Dependency Inversion & Open/Closed Principles")

    while True:
        print("\n--- Scholarship Application System ---")
        user_input = input("Enter student score (0-20) or 'q' to quit: ")

        if user_input.lower() == 'q':
            break

        # The engine runs the logic regardless of the service type
        engine.run(user_input)

if __name__ == "__main__":
    run_interactive_solid()