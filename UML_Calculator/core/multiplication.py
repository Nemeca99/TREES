"""
Multiplication operation for UML Calculator
Supports context-aware and advanced logic.
"""
def multiply(a, b, context=None, verbose=False):
    result = a * b
    if verbose:
        print(f"multiply({a}, {b}) = {result}")
    return result
