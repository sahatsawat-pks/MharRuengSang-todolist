"""
Simple Python Calculator Program
Supports basic operations: add, subtract, multiply, and divide
"""


def add(a, b):
    """Add two numbers."""
    return a + b


def subtract(a, b):
    """Subtract two numbers."""
    return a - b


def multiply(a, b):
    """Multiply two numbers."""
    return a * b


def divide(a, b):
    """Divide two numbers. Returns None if division by zero."""
    if b == 0:
        print("Error: Cannot divide by zero")
        return None
    return a / b


def calculator():
    """Main calculator function to handle user input and operations."""
    print("=" * 40)
    print("Simple Python Calculator")
    print("=" * 40)
    
    while True:
        print("\nOperations:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1/2/3/4/5): ").strip()
        
        if choice == '5':
            print("Thank you for using the calculator. Goodbye!")
            break
        
        if choice not in ['1', '2', '3', '4']:
            print("Invalid choice. Please enter a valid option (1/2/3/4/5).")
            continue
        
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            continue
        
        if choice == '1':
            result = add(num1, num2)
            print(f"\n{num1} + {num2} = {result}")
        elif choice == '2':
            result = subtract(num1, num2)
            print(f"\n{num1} - {num2} = {result}")
        elif choice == '3':
            result = multiply(num1, num2)
            print(f"\n{num1} * {num2} = {result}")
        elif choice == '4':
            result = divide(num1, num2)
            if result is not None:
                print(f"\n{num1} / {num2} = {result}")


if __name__ == "__main__":
    calculator()
