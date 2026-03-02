class BankAccount:
    def __init__(self, owner, balance=0.0):
        self.__owner = owner
        self.__balance = float(balance)

    @property
    def owner(self):
        return self.__owner

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Deposited {amount:.2f}. New balance: {self.__balance:.2f}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > self.__balance:
            print("Insufficient funds.")
        elif amount <= 0:
            print("Withdrawal amount must be positive.")
        else:
            self.__balance -= amount
            print(f"Withdrew {amount:.2f}. Remaining balance: {self.__balance:.2f}")

    def transfer_to(self, other_account, amount):
        if not isinstance(other_account, BankAccount):
            print("Invalid target account.")
            return

        if amount > self.__balance:
            print("Insufficient funds for transfer.")
        elif amount <= 0:
            print("Transfer amount must be positive.")
        else:
            self.__balance -= amount
            other_account.__balance += amount
            print(f"Transferred {amount:.2f} to {other_account.owner}.")
            print(f"New balance: {self.__balance:.2f}")

if __name__ == "__main__":
    # Test Scenario
    acc1 = BankAccount("Hamza", 1000)
    acc2 = BankAccount("Niama mrati", 500)

    print(f"--- {acc1.owner}'s Account ---")
    acc1.deposit(500)
    acc1.withdraw(200)

    print(f"\n--- Transferring from {acc1.owner} to {acc2.owner} ---")
    acc1.transfer_to(acc2, 300)

    print(f"\nFinal Balances:")
    print(f"{acc1.owner}: {acc1.balance}DH")
    print(f"{acc2.owner}: {acc2.balance}DH")