def calc(op, *args):
    if not args:
        return 0 if op in ["sum", "prod"] else None

    if op == "sum":
        result = 0
        for x in args:
            result += x
        return result

    elif op == "prod":
        result = 1
        for x in args:
            result *= x
        return result

    elif op == "min":
        res_min = args[0]
        for x in args:
            if x < res_min:
                res_min = x
        return res_min

    elif op == "max":
        res_max = args[0]
        for x in args:
            if x > res_max:
                res_max = x
        return res_max

    else:
        raise ValueError(f"Unsupported operation: {op}")

if __name__ == "__main__":
    try:
        operation = input("Enter operation (sum, prod, min, max): ").strip().lower()
        numbers_input = input("Enter numbers separated by spaces: ")
        
        # Convert input string to a list of floats
        nums = [float(x) for x in numbers_input.split()]

        # Passing the list as variable arguments using *
        result = calc(operation, *nums)
        print(f"Result of {operation}: {result}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")