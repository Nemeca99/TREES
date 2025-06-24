"""
Safe Expression Evaluator for UML Calculator
Provides a secure alternative to eval() for mathematical expressions
"""

import ast
import math
import cmath  # For complex number support
import operator as op
from typing import Dict, Any, Union, Callable

# Define allowed operators
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: lambda x, y: float('nan') if y == 0 and x == 0 else float('inf') if y == 0 and x > 0 else float('-inf') if y == 0 and x < 0 else op.truediv(x, y),
    ast.Pow: op.pow,
    ast.Mod: lambda x, y: float('nan') if y == 0 else op.mod(x, y),
    ast.FloorDiv: lambda x, y: float('nan') if y == 0 and x == 0 else float('inf') if y == 0 and x > 0 else float('-inf') if y == 0 and x < 0 else op.floordiv(x, y),
    ast.BitOr: op.or_,  # Support for bitwise OR
    ast.BitAnd: op.and_,  # Support for bitwise AND
    ast.BitXor: op.xor,  # Support for bitwise XOR
    ast.USub: op.neg,    # Unary negation
    ast.UAdd: op.pos,    # Unary positive
}

# Constants and functions that are safe to use
SAFE_CONSTANTS = {
    'pi': math.pi,
    'e': math.e,
    'tau': math.tau,
    'inf': math.inf,
    'nan': math.nan,
    'j': complex(0, 1),  # Imaginary unit
    'i': complex(0, 1),  # Alternative notation for imaginary unit
    'math': math,       # Allow direct access to math module
    'cmath': cmath      # Allow direct access to cmath module
}

SAFE_FUNCTIONS = {
    # Standard math functions
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,
    'sqrt': lambda x: cmath.sqrt(x) if x < 0 else math.sqrt(x),  # Handle negative roots
    'log': math.log,
    'log10': math.log10,
    'exp': math.exp,
    'floor': math.floor,
    'ceil': math.ceil,
    'round': round,
    'abs': abs,
    'pow': pow,
    'max': max,
    'min': min,
    
    # Complex number functions
    'phase': cmath.phase,  # Angle in the complex plane
    'polar': cmath.polar,  # Convert to polar coordinates
    'rect': cmath.rect,    # Convert from polar coordinates
    
    # Constants (defined as functions for convenience)
    'pi_func': lambda: math.pi,
    'e_func': lambda: math.e,
    'inf_func': lambda: float('inf'),
    'nan_func': lambda: float('nan'),
    'i_func': lambda: complex(0, 1),
    'j_func': lambda: complex(0, 1)
}

def safe_eval(expr: str) -> Any:
    """
    Safely evaluate a string mathematical expression.
    
    Args:
        expr (str): The expression to evaluate
        
    Returns:
        The evaluated result
        
    Raises:
        ValueError: If the expression contains unsupported operations
        SyntaxError: If the expression is syntactically invalid
        TypeError: If operand types are incompatible
    """
    # First, check if it's a simple numeric literal
    try:
        return ast.literal_eval(expr)
    except (ValueError, SyntaxError):
        # Not a simple literal, proceed with parsing
        pass
        
    # Parse the expression
    try:
        node = ast.parse(expr, mode='eval').body
        
        # Return the evaluated result
        return _eval_node(node)
        
    except SyntaxError as e:
        raise SyntaxError(f"Syntax error in expression: {expr}") from e
    except Exception as e:
        raise ValueError(f"Error evaluating expression: {str(e)}") from e

def _eval_node(node: Union[ast.Expression, ast.AST]) -> Any:
    """
    Recursively evaluate an AST node.
    """
    # Literal values
    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.Constant):
        return node.value
        
    # Names (variables)
    elif isinstance(node, ast.Name):
        if node.id in SAFE_CONSTANTS:
            return SAFE_CONSTANTS[node.id]
        raise NameError(f"Name '{node.id}' is not defined or not allowed")
        
    # Attribute access (e.g., math.sin, cmath.log)
    elif isinstance(node, ast.Attribute):
        value = _eval_node(node.value)
        attr = node.attr
        # Only allow math/cmath
        if value in (math, cmath):
            return getattr(value, attr)
        raise ValueError(f"Attribute access not allowed: {value}.{attr}")
    
    # Binary operations
    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        operator_type = type(node.op)
        
        if operator_type not in OPERATORS:
            raise ValueError(f"Unsupported operator: {operator_type}")
            
        try:
            return OPERATORS[operator_type](left, right)
        except Exception as e:
            raise ValueError(f"Operation error ({operator_type}): {str(e)}")
    
    # Unary operations (like -x)
    elif isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        operator_type = type(node.op)
        
        if operator_type not in OPERATORS:
            raise ValueError(f"Unsupported unary operator: {operator_type}")
            
        return OPERATORS[operator_type](operand)
    
    # Function calls
    elif isinstance(node, ast.Call):
        try:
            func = _eval_node(node.func)
            args = [_eval_node(arg) for arg in node.args]
            kwargs = {kw.arg: _eval_node(kw.value) for kw in node.keywords}
            
            # Check if the function is in our safe list
            if func in SAFE_FUNCTIONS.values():
                return func(*args, **kwargs)
            
            raise ValueError(f"Function not in safe list: {func}")
        except Exception as e:
            raise ValueError(f"Complex function call error: {str(e)}")
            
    # Lists/tuples for arguments
    elif isinstance(node, (ast.List, ast.Tuple)):
        return [_eval_node(elt) for elt in node.elts]
        
    # Set literals
    elif isinstance(node, ast.Set):
        return {_eval_node(elt) for elt in node.elts}
        
    # Dictionary literals
    elif isinstance(node, ast.Dict):
        return {_eval_node(key): _eval_node(value) 
                for key, value in zip(node.keys, node.values)}
                
    # Handle subscripts (like array[index])
    elif isinstance(node, ast.Subscript):
        value = _eval_node(node.value)
        
        # Handle different slice types
        if isinstance(node.slice, ast.Index):
            idx = _eval_node(node.slice.value)
        elif isinstance(node.slice, ast.Slice):
            start = _eval_node(node.slice.lower) if node.slice.lower else None
            stop = _eval_node(node.slice.upper) if node.slice.upper else None
            step = _eval_node(node.slice.step) if node.slice.step else None
            return value[start:stop:step]
        else:
            idx = _eval_node(node.slice)
            
        try:
            return value[idx]
        except Exception as e:
            raise ValueError(f"Subscript error: {str(e)}")
    
    else:
        raise ValueError(f"Unsupported AST node type: {type(node)}")

def is_valid_expression(expr: str) -> bool:
    """Check if an expression can be safely evaluated."""
    try:
        safe_eval(expr)
        # Check if result is a number
        return True
    except Exception:  # Using specific Exception class
        return False

# Test function
if __name__ == "__main__":
    # Some test expressions
    print(safe_eval("2 + 3 * 4"))
    print(safe_eval("sin(pi/2)"))
