def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        raise ZeroDivisionError
    return x / y

def is_even(n):
    return n % 2 == 0

def greet():
    return "Hello, World!"
