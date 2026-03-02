class Student:
    def __init__(self, name, age):
        # Using setters in constructor to trigger validation
        self.name = name
        self.age = age

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Name must be a non-empty string.")
        self.__name = value

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Age must be a positive integer.")
        self.__age = value

    def info(self):
        return f"Student: {self.__name}, Age: {self.__age}"

if __name__ == "__main__":
    try:
        # Create a valid student
        s1 = Student("Hamza", 22)
        print(s1.info())

        # Test changing values via setters
        s1.age = 23
        print(f"Updated Info: {s1.info()}")

        # Test validation error 
        s1.age = -5
        
    except ValueError as e:
        print(f"Validation Error: {e}")