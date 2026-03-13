from abc import ABC, abstractmethod

# --- 1. THE STRATEGY INTERFACE ---
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

# --- 3. & 4. CONCRETE STRATEGIES ---
class CreditCardStrategy(PaymentStrategy):
    def pay(self, amount):
        return f"Processed {amount:.2f} DH via Credit Card (Encrypted)."

class PaypalStrategy(PaymentStrategy):
    def pay(self, amount):
        return f"Processed {amount:.2f} DH via PayPal (Secure Redirect)."

class CryptoStrategy(PaymentStrategy):
    def pay(self, amount):
        return f"Processed {amount:.2f} DH via Crypto Wallet (Blockchain)."

# --- 5. & 6. THE CONTEXT (PaymentService) ---
class PaymentService:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy):
        print(f"  [SYSTEM] Strategy swapped to: {strategy.__class__.__name__}")
        self.strategy = strategy

    def validate(self, amount):
        try: return float(amount) > 0
        except: return False

    def calculate_total(self, amount):
        # 2.50 DH flat fee for all transactions
        return float(amount) + 2.50

    def execute(self, amount):
        if self.validate(amount):
            total = self.calculate_total(amount)
            # Delegation: The service doesn't know HOW to pay, it just tells the strategy to do it
            result = self.strategy.pay(total)
            print(f"  [SUCCESS] {result}")
        else:
            print("  [ERROR] Invalid amount provided.")

# --- INTERACTIVE TESTING ---

def run_interactive_strategy():
    # Initialize with a default strategy
    service = PaymentService(CreditCardStrategy())
    
    strategies = {
        "1": CreditCardStrategy(),
        "2": PaypalStrategy(),
        "3": CryptoStrategy()
    }

    print("--- 💳 Dynamic Payment Strategy Lab ---")
    print("The 'PaymentService' stays the same, but its behavior changes.")

    while True:
        print("\nOptions:")
        print("1. Use Credit Card")
        print("2. Use PayPal")
        print("3. Use Crypto")
        print("q. Quit")
        
        choice = input("\nSelect payment method (1/2/3/q): ")

        if choice == 'q':
            break

        if choice in strategies:
            # Change behavior at runtime
            service.set_strategy(strategies[choice])
            
            amount_in = input("Enter amount to pay (DH): ")
            service.execute(amount_in)
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    run_interactive_strategy()