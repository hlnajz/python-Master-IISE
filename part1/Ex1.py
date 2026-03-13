def is_even(n):
    if not isinstance(n, int):
        raise TypeError("Input must be an integer.")
    return n % 2 == 0

def sum_list(values):
    if not isinstance(values, list):
        raise TypeError("Input must be a list.")
    total = 0
    for val in values:
        if not isinstance(val, (int, float)):
            raise ValueError("List must contain only numbers.")
        total += val
    return total

def max_list(values):
    if not isinstance(values, list):
        raise TypeError("Input must be a list.")
    if not values:
        raise ValueError("List cannot be empty.")
    
    current_max = values[0]
    for val in values:
        if not isinstance(val, (int, float)):
            raise ValueError("List must contain only numbers.")
        if val > current_max:
            current_max = val
    return current_max

if __name__ == "__main__":
    try:
        # User input for is_even
        num = int(input("Enter an integer to check if it's even: "))
        print(f"Is {num} even? {is_even(num)}")

        # User input for sum and max
        user_input = input("\nEnter a list of numbers separated by spaces: ")
        # Convert string input into a list of floats
        num_list = [float(x) for x in user_input.split()]

        print(f"List: {num_list}")
        print(f"Sum: {sum_list(num_list)}")
        print(f"Max: {max_list(num_list)}")

    except ValueError as e:
        print(f"Input Error: {e}. Please enter valid numbers.")
    except Exception as e:
        print(f"An error occurred: {e}")