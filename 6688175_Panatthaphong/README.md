# Simple Python Calculator

## Description
A simple command-line calculator program written in Python that supports basic arithmetic operations.

## Features
- **Add**: Addition of two numbers
- **Subtract**: Subtraction of two numbers
- **Multiply**: Multiplication of two numbers
- **Divide**: Division of two numbers (with zero-division protection)

## Requirements
- Python 3.6 or higher

## How to Run
```bash
python calculator.py
```

## Usage
1. Run the program
2. Select an operation (1-4) or exit (5)
3. Enter two numbers when prompted
4. View the result
5. Repeat or exit

## Example
```
========================================
Simple Python Calculator
========================================

Operations:
1. Add
2. Subtract
3. Multiply
4. Divide
5. Exit

Enter your choice (1/2/3/4/5): 1
Enter first number: 10
Enter second number: 5

10.0 + 5.0 = 15.0
```

## Error Handling
- Division by zero is handled with an error message
- Invalid input (non-numeric) is caught and reported
- Invalid menu choices are rejected
