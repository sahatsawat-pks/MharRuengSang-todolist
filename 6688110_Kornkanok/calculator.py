def add(a, b):
    """Add two numbers."""
    return a + b

def subtract(a, b):
    """Subtract b from a."""
    return a - b

def multiply(a, b):
    """Multiply two numbers."""
    return a * b

def divide(a, b):
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python calculator.py <num1> <op> <num2>")
        print("Operators: +, -, *, /")
        sys.exit(1)
    try:
        num1 = float(sys.argv[1])
        op = sys.argv[2]
        num2 = float(sys.argv[3])
    except ValueError:
        print("Invalid numbers")
        sys.exit(1)
    
    if op == '+':
        result = add(num1, num2)
    elif op == '-':
        result = subtract(num1, num2)
    elif op == '*':
        result = multiply(num1, num2)
    elif op == '/':
        try:
            result = divide(num1, num2)
        except ValueError as e:
            print(e)
            sys.exit(1)
    else:
        print("Invalid operator. Use +, -, *, /")
        sys.exit(1)
    
    print(f"{num1} {op} {num2} = {result}")