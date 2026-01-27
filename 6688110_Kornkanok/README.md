# Simple Calculator

A simple calculator that supports addition, subtraction, multiplication, division, and velocity calculation.

## Usage

Run the calculator from the command line:

```bash
python calculator.py <num1> <operator> <num2>
```

### Examples

- Addition: `python calculator.py 5 + 3` → `5 + 3 = 8`
- Subtraction: `python calculator.py 10 - 4` → `10 - 4 = 6`
- Multiplication: `python calculator.py 2 * 6` → `2 * 6 = 12`
- Division: `python calculator.py 8 / 2` → `8 / 2 = 4.0`

## Functions

The calculator also provides a `velocity(distance, time)` function for calculating velocity as distance divided by time.

## Running Tests

To run the tests, use pytest:

```bash
pytest test_calculator.py
```