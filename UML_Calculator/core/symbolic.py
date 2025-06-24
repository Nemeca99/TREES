"""
Mathematical expression handling with symbolic support for UML Calculator
"""
import sympy
import numpy as np
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from sympy import symbols, sympify, Eq
from core.ris import ris

def evaluate_expression(expr_str, x_value=None, symbolic=False, standard_mode=False):
    """
    Evaluate a mathematical expression with RIS operations
    
    Args:
        expr_str: String expression like "RIS(4,2) + 5" or "3*x^2 - 5*x + 2"
        x_value: Value to substitute for x if present
        symbolic: If True, return symbolic expression
        standard_mode: If True, prioritize standard math over RIS
        
    Returns:
        Evaluated result or symbolic expression
    """
    # Clean up the expression
    expr_str = expr_str.replace("^", "**")  # Replace ^ with ** for exponentiation
    
    # Handle equation with = sign
    if "=" in expr_str and not symbolic:
        sides = expr_str.split("=", 1)
        if len(sides) == 2 and sides[1].strip():
            # This is an equation to solve
            left = sides[0].strip()
            right = sides[1].strip()
            return solve_equation(left, right, x_value)
        else:
            # Just evaluate the left side
            expr_str = sides[0].strip()
    
    # Define symbols
    x, y, z = symbols('x y z')
    
    # Configure sympy parser with implicit multiplication
    transformations = standard_transformations + (implicit_multiplication_application,)
    
    # Replace RIS calls with sympy functions
    if "RIS" in expr_str.upper() and not standard_mode:
        # Create a temporary function that acts like RIS
        def sympy_ris(a, b):
            if symbolic:
                # For symbolic mode, return a special representation
                return sympy.Function('RIS')(a, b)
            else:
                # For numeric mode, evaluate RIS
                if isinstance(a, sympy.Basic) and a.is_number:
                    a = float(a)
                if isinstance(b, sympy.Basic) and b.is_number:
                    b = float(b)
                return ris(a, b)

        # Add the RIS function to sympy's namespace
        expr_str = expr_str.replace("RIS", "sympy_ris")
    
    try:
        # Parse the expression
        expr = parse_expr(expr_str, transformations=transformations)
        
        # Substitute x value if provided
        if x_value is not None and not symbolic:
            expr = expr.subs(x, x_value)
            
        if symbolic:
            return expr
        else:
            # Evaluate numerically if all symbols are substituted
            if expr.is_number:
                return float(expr)
            else:
                return expr
    except Exception as e:
        raise ValueError(f"Error in expression: {str(e)}")

def solve_equation(left_side, right_side, x_value=None):
    """Solve an equation for x or evaluate if x_value is provided"""
    x = symbols('x')
    try:
        # Parse both sides with implicit multiplication
        transformations = standard_transformations + (implicit_multiplication_application,)
        left = parse_expr(left_side, transformations=transformations)
        right = parse_expr(right_side, transformations=transformations)
        
        if x_value is not None:
            # Just evaluate both sides with the given x value
            left_val = left.subs(x, x_value)
            right_val = right.subs(x, x_value)
            return {
                'left_value': float(left_val) if left_val.is_number else left_val,
                'right_value': float(right_val) if right_val.is_number else right_val,
                'equal': left_val == right_val
            }
        else:
            # Solve for x
            equation = Eq(left, right)
            solution = sympy.solve(equation, x)
            return {
                'equation': str(equation),
                'solutions': [float(sol) if sol.is_number else sol for sol in solution]
            }
    except Exception as e:
        raise ValueError(f"Error solving equation: {str(e)}")

def generate_plot_data(expr_str, x_min=-10, x_max=10, points=100, standard_mode=False):
    """
    Generate x,y data for plotting an expression
    
    Args:
        expr_str: String expression like "RIS(x,2) + 5" or "3*x^2 - 5*x + 2"
        x_min, x_max: Range for x values
        points: Number of points to calculate
        standard_mode: If True, prioritize standard math over RIS
        
    Returns:
        (x_values, y_values) as numpy arrays
    """
    x = symbols('x')
    expr = evaluate_expression(expr_str, symbolic=True, standard_mode=standard_mode)
    
    x_values = np.linspace(x_min, x_max, points)
    y_values = []
    
    for x_val in x_values:
        try:
            result = expr.subs(x, x_val)
            if isinstance(result, sympy.Basic):
                if result.is_number:
                    y_values.append(float(result))
                else:
                    # If contains RIS function calls, evaluate them
                    if 'RIS' in str(result):
                        # Extract and evaluate RIS calls
                        ris_result = evaluate_expression(str(result), x_value=x_val, standard_mode=standard_mode)
                        y_values.append(float(ris_result))
                    else:
                        y_values.append(float(result))
            else:
                y_values.append(float(result))
        except:
            # If evaluation fails at this point, use NaN
            y_values.append(float('nan'))
    
    return x_values, np.array(y_values)
