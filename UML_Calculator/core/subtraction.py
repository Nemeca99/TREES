"""
Subtraction operation for UML Calculator
Supports context-aware and advanced logic.
"""
def subtract(a, b, context=None, verbose=False):
    result = a - b
    if verbose:
        print(f"subtract({a}, {b}) = {result}")
    return result
