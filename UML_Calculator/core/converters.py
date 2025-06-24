"""
Enhanced Standard to UML Conversion Module
Provides functions to convert standard arithmetic expressions to UML notation.
"""

import re
from typing import Union, Dict, Any

def convert_standard_to_uml(expr: str) -> str:
    """
    Convert standard arithmetic expressions to UML notation.
    Enhanced with better handling of operators and nested expressions.
    
    Examples:
    - "2+3" becomes "[2,3]" (addition)
    - "6-2" becomes "{6,2}" (subtraction)
    - "4*5" becomes "<4,5>" (multiplication)
    - "8/2" becomes "<>8,2<>" (division)
    - "2+3*4" becomes "[2,<3,4>]" (respecting PEMDAS)
    
    Args:
        expr (str): Standard arithmetic expression
        
    Returns:
        str: Equivalent UML notation
    """
    # Handle already-UML notation
    if any(c in expr for c in "[]{}@<>!"):
        return expr

    # Remove spaces
    expr = expr.replace(" ", "")
    
    # Parentheses handling (recursive conversion)
    while "(" in expr:
        # Handle parentheses recursively
        expr = re.sub(r'\(([^()]+)\)',
                     lambda m: convert_standard_to_uml(m.group(1)), 
                     expr)
    
    # Handle operators with proper precedence
    # Order: ^ (power), * and / (same level), + and - (same level)
    
    # 1. Handle power ^
    while "^" in expr:
        expr = re.sub(r'(-?\d+(\.\d+)?)\^(-?\d+(\.\d+)?)', r'@(\1,\3)', expr)
    
    # 2. Handle multiplication and division
    while re.search(r'[*/]', expr):
        # Handle multiplication
        expr = re.sub(r'(-?\d+(\.\d+)?)\*(-?\d+(\.\d+)?)', r'<\1,\3>', expr)
        # Handle division
        expr = re.sub(r'(-?\d+(\.\d+)?)/(-?\d+(\.\d+)?)', r'<>\1,\3<>', expr)
    
    # 3. Handle addition and subtraction
    while re.search(r'[+\-]', expr):
        # Handle addition
        expr = re.sub(r'(-?\d+(\.\d+)?)\+(-?\d+(\.\d+)?)', r'[\1,\3]', expr)
        # Handle subtraction
        expr = re.sub(r'(-?\d+(\.\d+)?)-(-?\d+(\.\d+)?)', r'{\1,\3}', expr)
    
    return expr

# Test cases
if __name__ == "__main__":
    test_cases = [
        "2+3",
        "6-2",
        "4*5",
        "8/2",
        "2+3*4",  # Should respect precedence: 2+12 = 14
        "(2+3)*4", # Should be 20
        "2^3",    # Should be @(2,3)
        "10%3",   # Modulo not directly supported
        "1+2+3",  # Should be [1,[2,3]] or similar
        "2*(3+4)" # Should respect parentheses
    ]
    
    for test in test_cases:
        uml = convert_standard_to_uml(test)
        print(f"{test} → {uml}")
