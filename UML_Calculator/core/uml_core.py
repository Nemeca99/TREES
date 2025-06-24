"""
UML Core Logic Engine - Enhanced with Conversation Analysis Insights
This module implements the core logic for the Universal Mathematical Language (UML) symbolic calculator.
Supports parsing and evaluating UML symbolic expressions with RIS meta-operator, superposition logic,
recursive compression, and TFID identity anchoring.

Enhanced with empirical evidence from 189 conversation insights spanning May 2023 - June 2025.
Implements T.R.E.E.S. (The Recursive Entropy Engine System) principles in practical UML Calculator.
"""

# Fix import paths for operation modules and utils
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from core.addition import add
from core.subtraction import subtract
from core.multiplication import multiply
from core.division import divide
from core.ris import ris
from utils.safe_eval import safe_eval

import math
from typing import cast, Dict, List, Tuple, Optional, Union

# Letter-to-number mapping (A=1..Z=26, a=27..z=52)
def letter_to_number(s: str) -> int:
    """Convert a letter to its numerical value: A-Z = 1-26, a-z = 27-52"""
    if s.isupper():
        return ord(s) - ord('A') + 1
    elif s.islower():
        return ord(s) - ord('a') + 27
    else:
        raise ValueError(f"Invalid letter: {s}")

def parse_value(val: str) -> Union[float, int, str]:
    """Parse value as float or convert letter to number using base-52 mapping."""
    try:
        # Handle special values
        if val.lower() == "inf" or val.lower() == "infinity":
            return float('inf')
        elif val.lower() == "nan":
            return float('nan')
        return float(val)
    except ValueError:
        try:
            return float(letter_to_number(val))
        except ValueError:
            # Return the string itself if it's not a number or letter
            return val

# --- RIS Meta-Operator with Superposition & Quantum Logic ---
def ris_meta_operator(a: Union[float, complex, str], b: Union[float, complex, str], operation: Optional[str] = None) -> Tuple[Union[float, complex, str], str]:
    """
    RIS (Recursive Integration System) meta-operator with hybrid Wolfram-style precedence.
    - a == 0 or b == 0: addition
    - a == b: multiplication
    - a > b and a % b == 0 and a / b < a and a / b < b: division (compact compression)
    - a > 1 and b > 1: multiplication
    - else: addition
    """
    try:
        if isinstance(a, str):
            a = parse_value(a)
        if isinstance(b, str):
            b = parse_value(b)
        if not isinstance(a, (int, float)):
            if isinstance(a, str):
                a = float(a)
            elif isinstance(a, complex):
                a = a.real
        if not isinstance(b, (int, float)):
            if isinstance(b, str):
                b = float(b)
            elif isinstance(b, complex):
                b = b.real
        if a == 0 or b == 0:
            return a + b, "addition (zero operand)"
        elif a == b:
            return a * b, "multiplication (equal operands)"
        elif a > b and a % b == 0:
            quotient = a / b
            if quotient < a and quotient < b:
                return quotient, "division (compact compression)"
            else:
                return a * b, "multiplication (division ignored)"
        elif a > 1 and b > 1:
            return a * b, "multiplication (default)"
        else:
            return a + b, "addition (fallback)"
    except Exception as e:
        return f"RIS error: {e}", "error"

def recursive_compress(value: Union[float, complex, str]) -> Union[float, complex, str]:
    """
    Recursively compress a value by repeatedly taking the square root if it's a perfect square or > 10,
    or by taking the log if it's a power of e, or by dividing by 10 if it's a power of 10.
    Stops at a "natural attractor" (10, 16, π, etc.).
    """
    if not isinstance(value, (int, float)) or isinstance(value, complex) or (isinstance(value, float) and (math.isnan(value) or math.isinf(value))):
        return value
    # Special case: compress pi^2 to pi
    if math.isclose(value, math.pi ** 2, rel_tol=1e-9):
        return math.pi
    # Stop at natural attractors
    for attractor in [10, 16, math.pi]:
        if math.isclose(value, attractor, rel_tol=1e-9):
            return attractor
    # Prefer sqrt for perfect squares or > 10
    if value > 10:
        sqrt_val = math.sqrt(value)
        if sqrt_val.is_integer() or value in [100, 256, 1024, math.pi ** 2]:
            return recursive_compress(sqrt_val)
    # Prefer log for powers of e
    if value > 0 and math.isclose(math.log(value), round(math.log(value)), rel_tol=1e-9):
        log_val = math.log(value)
        return recursive_compress(log_val)
    # Prefer division by 10 for powers of 10
    if value > 10 and math.isclose(math.log10(value), round(math.log10(value)), rel_tol=1e-9):
        div_val = value / 10
        return recursive_compress(div_val)
    return value

def parse_uml(expression: str) -> Dict:
    """
    Parse a UML expression into its components and operation type.
    Now supports: +, -, *, /, ^, sqrt(), sin(), cos(), RIS()
    """
    expression = expression.strip()
    try:
        if expression.lower() == "inf" or expression.lower() == "infinity":
            return {"type": "value", "value": float('inf')}
        elif expression.lower() == "nan":
            return {"type": "value", "value": float('nan')}
        value = float(expression)
        return {"type": "value", "value": value}
    except ValueError:
        pass
    if len(expression) == 1 and expression.isalpha():
        return {"type": "value", "value": letter_to_number(expression)}
    # Handle sqrt(), sin(), cos(), RIS()
    if expression.startswith('sqrt(') and expression.endswith(')'):
        inner = expression[5:-1]
        return {"type": "sqrt", "operand": parse_uml(inner)}
    if expression.startswith('sin(') and expression.endswith(')'):
        inner = expression[4:-1]
        return {"type": "sin", "operand": parse_uml(inner)}
    if expression.startswith('cos(') and expression.endswith(')'):
        inner = expression[4:-1]
        return {"type": "cos", "operand": parse_uml(inner)}
    if expression.startswith('RIS(') and expression.endswith(')'):
        inner = expression[4:-1]
        operands = split_arguments(inner)
        if len(operands) != 2:
            raise ValueError(f"RIS expects 2 operands, got {len(operands)}: {expression}")
        return {"type": "ris", "operands": [parse_uml(op) for op in operands]}
    # Handle ^ as power
    if '^' in expression:
        parts = expression.split('^')
        if len(parts) == 2:
            return {"type": "power", "operands": [parse_uml(parts[0]), parse_uml(parts[1])]} 
    if expression.startswith('[') and expression.endswith(']'):
        inner = expression[1:-1]
        operands = split_arguments(inner)
        if len(operands) == 1:
            return {"type": "value", "value": parse_uml(operands[0])["value"]}
        return {"type": "addition", "operands": [parse_uml(op) for op in operands]}
    if expression.startswith('{') and expression.endswith('}'):
        inner = expression[1:-1]
        operands = split_arguments(inner)
        if len(operands) == 1:
            return {"type": "value", "value": parse_uml(operands[0])["value"]}
        return {"type": "subtraction", "operands": [parse_uml(op) for op in operands]}
    if expression.startswith('<') and expression.endswith('>') and not expression.startswith('<>'):
        inner = expression[1:-1]
        operands = split_arguments(inner)
        return {"type": "multiplication", "operands": [parse_uml(op) for op in operands]}
    if expression.startswith('<>') and expression.endswith('<>'):
        inner = expression[2:-2]
        operands = split_arguments(inner)
        if len(operands) != 2:
            raise ValueError(f"Division expects 2 operands, got {len(operands)}: {expression}")
        return {"type": "division", "operands": [parse_uml(op) for op in operands]}
    if expression.startswith('@(') and expression.endswith(')'):
        inner = expression[2:-1]
        operands = split_arguments(inner)
        if len(operands) != 2:
            raise ValueError(f"Power expects 2 operands, got {len(operands)}: {expression}")
        return {"type": "power", "operands": [parse_uml(op) for op in operands]}
    if expression.startswith('!(') and expression.endswith(')'):
        inner = expression[2:-1]
        operands = split_arguments(inner)
        if len(operands) != 2:
            raise ValueError(f"Complex number expects 2 operands, got {len(operands)}: {expression}")
        real = parse_uml(operands[0])["value"]
        imag = parse_uml(operands[1])["value"]
        return {"type": "value", "value": complex(real, imag)}
    return {"type": "symbol", "name": expression}

def split_arguments(arg_string: str) -> List[str]:
    """
    Split a UML argument string into separate operands, handling nested structures.
    """
    if not arg_string:
        return []
    args = []
    current = ""
    bracket_depth = 0
    paren_depth = 0
    angle_depth = 0
    brace_depth = 0
    for char in arg_string:
        if char == ',' and bracket_depth == 0 and paren_depth == 0 and angle_depth == 0 and brace_depth == 0:
            args.append(current)
            current = ""
        else:
            current += char
            if char == '[':
                bracket_depth += 1
            elif char == ']':
                bracket_depth -= 1
            elif char == '(': 
                paren_depth += 1
            elif char == ')':
                paren_depth -= 1
            elif char == '<':
                angle_depth += 1
            elif char == '>':
                angle_depth -= 1
            elif char == '{':
                brace_depth += 1
            elif char == '}':
                brace_depth -= 1
    if current:
        args.append(current)
    return args

def eval_uml(parsed_expr: Dict) -> Union[float, complex, str]:
    """
    Evaluate a parsed UML expression.
    """
    expr_type = parsed_expr["type"]
    if expr_type == "value":
        return parsed_expr["value"]
    if expr_type == "symbol":
        return parsed_expr["name"]
    operands = [eval_uml(op) for op in parsed_expr.get("operands", [])]
    # Addition [a,b]
    if expr_type == "addition":
        result = operands[0]
        for op in operands[1:]:
            result = add(result, op)
        return result
    # Subtraction {a,b}
    if expr_type == "subtraction":
        result = operands[0]
        for op in operands[1:]:
            result = subtract(result, op)
        return result
    # Multiplication <a,b>
    if expr_type == "multiplication":
        result = operands[0]
        for op in operands[1:]:
            result = multiply(result, op)
        return result
    # Division <>a,b<>
    if expr_type == "division":
        if len(operands) == 2:
            a, b = operands
            try:
                result = divide(a, b)
            except Exception:
                return f"<> {a},{b} <>"
            return result
        else:
            return f"<> {','.join(str(op) for op in operands)} <>"
    # Power @(a,b)
    if expr_type == "power":
        if len(operands) == 2:
            a, b = operands
            if isinstance(a, (int, float, complex)) and isinstance(b, (int, float, complex)):
                return a ** b
            else:
                return f"@({a},{b})"
        else:
            return f"@({','.join(str(op) for op in operands)})"
    # RIS meta-operator
    if expr_type == "ris":
        if len(operands) == 2:
            return ris(operands[0], operands[1])
        else:
            return f"RIS({','.join(str(op) for op in operands)})"
    # Sqrt, sin, cos
    if expr_type == "sqrt":
        operand = eval_uml(parsed_expr["operand"])
        if not isinstance(operand, (int, float)):
            if isinstance(operand, str):
                operand = float(operand)
            elif isinstance(operand, complex):
                operand = operand.real
        return math.sqrt(operand)
    if expr_type == "sin":
        operand = eval_uml(parsed_expr["operand"])
        if not isinstance(operand, (int, float)):
            if isinstance(operand, str):
                operand = float(operand)
            elif isinstance(operand, complex):
                operand = operand.real
        return math.sin(operand)
    if expr_type == "cos":
        operand = eval_uml(parsed_expr["operand"])
        if not isinstance(operand, (int, float)):
            if isinstance(operand, str):
                operand = float(operand)
            elif isinstance(operand, complex):
                operand = operand.real
        return math.cos(operand)
    # If none of the above, return as symbolic
    return str(parsed_expr)

def calculate(expr: str):
    """Parse and evaluate a UML expression, returning (uml_result, std_result)."""
    try:
        parsed = parse_uml(expr)
        uml_result = eval_uml(parsed)
        # If the result is a string and matches the input, try safe_eval as fallback
        if isinstance(uml_result, str) and uml_result == expr:
            try:
                uml_result = safe_eval(expr)
            except Exception:
                uml_result = None  # type: ignore
    except Exception:
        try:
            uml_result = safe_eval(expr)
        except Exception:
            uml_result = None  # type: ignore
    try:
        std_result = safe_eval(expr)
    except Exception:
        std_result = None
    return uml_result, std_result
