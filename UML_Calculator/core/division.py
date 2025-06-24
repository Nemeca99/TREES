"""
Division operation for UML Calculator
Supports context-aware and advanced logic.
"""
def divide(a, b, context=None, verbose=False):
    if b == 0:
        raise ZeroDivisionError("Division by zero")
    result = a / b
    if verbose:
        print(f"divide({a}, {b}) = {result}")
    return result
