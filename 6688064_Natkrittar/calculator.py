"""Simple calculator with add, subtract, multiply, divide functions

Provides small CLI when run as a script:
	python 6688064_Natkrittar/calculator.py add 2 3
"""
from __future__ import annotations
from typing import Union
import argparse

Number = Union[int, float]


def add(a: Number, b: Number) -> Number:
	"""Return the sum of a and b."""
	return a + b


def subtract(a: Number, b: Number) -> Number:
	"""Return the difference a - b."""
	return a - b


def multiply(a: Number, b: Number) -> Number:
	"""Return the product of a and b."""
	return a * b


def divide(a: Number, b: Number) -> Number:
	"""Return the quotient a / b.

	Raises:
		ZeroDivisionError: if b is zero.
	"""
	if b == 0:
		raise ZeroDivisionError("division by zero")
	return a / b


__all__ = ["add", "subtract", "multiply", "divide"]


def _to_number(value: str) -> Number:
	"""Convert a string to int if possible, otherwise float.

	Raises ValueError on invalid input.
	"""
	try:
		return int(value)
	except ValueError:
		return float(value)


def _cli() -> None:
	parser = argparse.ArgumentParser(description="Simple calculator")
	parser.add_argument("operation", choices=["add", "subtract", "multiply", "divide"], help="operation")
	parser.add_argument("a", help="first operand")
	parser.add_argument("b", help="second operand")
	args = parser.parse_args()

	a = _to_number(args.a)
	b = _to_number(args.b)

	ops = {
		"add": add,
		"subtract": subtract,
		"multiply": multiply,
		"divide": divide,
	}

	func = ops[args.operation]
	try:
		result = func(a, b)
	except Exception as exc:  # keep CLI simple
		parser.error(str(exc))

	# Print integer results without decimal when possible
	if isinstance(result, float) and result.is_integer():
		print(int(result))
	else:
		print(result)


if __name__ == "__main__":
	_cli()

