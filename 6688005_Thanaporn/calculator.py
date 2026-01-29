"""Simple calculator supporting basic arithmetic operations."""


def add(a: float, b: float) -> float:
	"""Return the sum of two numbers."""

	return a + b


def subtract(a: float, b: float) -> float:
	"""Return the difference of two numbers (a - b)."""

	return a - b


def multiply(a: float, b: float) -> float:
	"""Return the product of two numbers."""

	return a * b


def divide(a: float, b: float) -> float:
	"""Return the quotient of two numbers. Raise ValueError on division by zero."""

	if b == 0:
		raise ValueError("Cannot divide by zero.")
	return a / b


def calculate_velocity(distance: float, time: float) -> float:
	"""Return velocity given distance and time; raise ValueError for nonpositive time."""

	if time <= 0:
		raise ValueError("Time must be greater than zero")
	return distance / time


def main() -> None:
	print("Simple Calculator")
	print("Select operation:")
	print("1. Add")
	print("2. Subtract")
	print("3. Multiply")
	print("4. Divide")

	choice = input("Enter choice (1/2/3/4): ")
	if choice not in {"1", "2", "3", "4"}:
		print("Invalid choice.")
		return

	try:
		num1 = float(input("Enter first number: "))
		num2 = float(input("Enter second number: "))
	except ValueError:
		print("Invalid input. Please enter numeric values.")
		return

	try:
		if choice == "1":
			result = add(num1, num2)
		elif choice == "2":
			result = subtract(num1, num2)
		elif choice == "3":
			result = multiply(num1, num2)
		else:
			result = divide(num1, num2)

		print(f"Result: {result}")
	except ValueError as error:
		print(error)


if __name__ == "__main__":
	main()
