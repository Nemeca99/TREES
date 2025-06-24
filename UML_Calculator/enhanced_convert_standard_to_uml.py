"""
Enhanced conversion from standard mathematical notation to UML notation
"""

import re
from typing import Union

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
    """
    # Handle already-UML notation
    if any(c in expr for c in "[]{}()<>@?/"):
        return expr
        
    # Remove whitespace
    expr = expr.replace(' ', '')
    
    # Handle parentheses first by recursive conversion
    paren_pattern = r'\(([^()]+)\)'
    while re.search(paren_pattern, expr):
        expr = re.sub(paren_pattern, 
                     lambda m: convert_standard_to_uml(m.group(1)), 
                     expr)
    
    # Handle division operation
    div_pattern = r'(\d+(?:\.\d+)?|\w+)/(\d+(?:\.\d+)?|\w+)'
    expr = re.sub(div_pattern, r'<>\1,\2<>', expr)
    
    # Handle multiplication
    mul_pattern = r'(\d+(?:\.\d+)?|\w+)\*(\d+(?:\.\d+)?|\w+)'
    expr = re.sub(mul_pattern, r'<\1,\2>', expr)
    
    # Handle subtraction
    sub_pattern = r'(\d+(?:\.\d+)?|\w+)-(\d+(?:\.\d+)?|\w+)'
    expr = re.sub(sub_pattern, r'{\1,\2}', expr)
    
    # Handle addition
    add_pattern = r'(\d+(?:\.\d+)?|\w+)\+(\d+(?:\.\d+)?|\w+)'
    expr = re.sub(add_pattern, r'[\1,\2]', expr)
    
    # Handle exponents (using RIS convention)
    exp_pattern = r'(\d+(?:\.\d+)?|\w+)\^(\d+(?:\.\d+)?|\w+)'
    expr = re.sub(exp_pattern, r'@(\1,\2)', expr)
    
    # Handle modulo
    mod_pattern = r'(\d+(?:\.\d+)?|\w+)%(\d+(?:\.\d+)?|\w+)'
    expr = re.sub(mod_pattern, r'\1%\2', expr)
    
    return expr

if __name__ == "__main__":
    # Test the conversion function
    test_cases = [
        "2+3",
        "6-2",
        "4*5",
        "8/2",
        "2+3*4",
        "(2+3)*4",
        "2^3",
        "10%3"
    ]
    
    for test in test_cases:
        uml = convert_standard_to_uml(test)
        print(f"{test} → {uml}")
