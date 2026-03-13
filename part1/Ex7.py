class Employee:
    def __init__(self, name, emp_id):
        self._name = name
        self._emp_id = emp_id

    def monthly_pay(self):
        """Base method to be overridden"""
        return 0.0

    def __str__(self):
        return f"{self.__class__.__name__}: {self._name} (ID: {self._emp_id})"

class FullTimeEmployee(Employee):
    def __init__(self, name, emp_id, salary):
        super().__init__(name, emp_id)
        self.__salary = salary

    def monthly_pay(self):
        # Full time gets flat salary
        return self.__salary

class PartTimeEmployee(Employee):
    def __init__(self, name, emp_id, hourly_rate, hours_worked):
        super().__init__(name, emp_id)
        self.__hourly_rate = hourly_rate
        self.__hours_worked = hours_worked

    def monthly_pay(self):
        # Part time gets paid by hour
        return self.__hourly_rate * self.__hours_worked

# Polymorphic function
def process_payroll(employees):
    total_payroll = 0.0
    print("--- Payroll Processing ---")
    for emp in employees:
        pay = emp.monthly_pay()
        print(f"{emp} - Pay: ${pay:,.2f}")
        total_payroll += pay
    print("-" * 30)
    print(f"Total Payroll: ${total_payroll:,.2f}")

if __name__ == "__main__":
    # Test Scenario
    emp1 = FullTimeEmployee("Hamza", "FT01", 5000.0)
    emp2 = PartTimeEmployee("Niama", "PT01", 20.0, 100) # 20/hr * 100 hrs
    emp3 = FullTimeEmployee("Meriam", "FT02", 6000.0)

    staff = [emp1, emp2, emp3]
    
    process_payroll(staff)