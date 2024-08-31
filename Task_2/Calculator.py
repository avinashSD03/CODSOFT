import operator

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error: Division by zero is undefined."
    return x / y

def show_history(history):
    if not history:
        print("No history available.")
    else:
        print("Calculation History:")
        i=1
        for entry in history:
            print(i,")",entry)
            i+=1

def main():
    history = []
    operations = {
        '1': ('Addition', add),
        '2': ('Subtraction', subtract),
        '3': ('Multiplication', multiply),
        '4': ('Division', divide)
    }
    
    while True:
        print("\nSimple Calculator")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Show History")
        print("6. Exit")

        choice = input("Enter choice (1/2/3/4/5/6): ")

        if choice == '6':
            print("Exiting the calculator. Thank you!")
            break

        if choice == '5':
            show_history(history)
            continue
        
        if choice not in operations:
            print("Invalid choice. Please choose a valid operation.")
            continue

        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            continue

        operation_name, operation_func = operations[choice]
        result = operation_func(num1, num2)

        if isinstance(result, str):
            print(result)  # This handles errors like division by zero.
        else:
            print(f"The result of {operation_name.lower()} is: {result}")
            history.append(f"{num1} {operation_name.lower()} {num2} = {result}")

if __name__ == "__main__":
    main()
