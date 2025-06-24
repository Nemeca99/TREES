"""
UML Core Logic Engine - Enhanced with Conversation Analysis Insights
This module implements the core logic for the Universal Mathematical Language (UML) symbolic calculator.
Supports parsing and evaluating UML symbolic expressions with RIS meta-operator, superposition logic,
recursive compression, and TFID identity anchoring.

Enhanced with empirical evidence from 189 conversation insights spanning May 2023 - June 2025.
Implements T.R.E.E.S. (The Recursive Entropy Engine System) principles in practical UML Calculator.
"""

import math
import time
import re  # Added import for regex pattern matching
from typing import Any, Dict, List, Tuple, Optional, Union

# Letter-to-number mapping (A=1..Z=26, a=27..z=52)
def letter_to_number(s: str) -> int:
    if s.isupper():
        return ord(s) - ord('A') + 1
    elif s.islower():
        return ord(s) - ord('a') + 27
    else:
        raise ValueError(f"Invalid letter: {s}")

def parse_value(val: str) -> float:
    """Parse value as float or convert letter to number using base-52 mapping."""
    try:
        return float(val)
    except ValueError:
        return float(letter_to_number(val))

# --- RIS Meta-Operator with Superposition & Quantum Logic ---
def ris_meta_operator(a: Union[float, complex, str], b: Union[float, complex, str], operation: Optional[str] = None) -> Dict[str, Any]:
    """
    RIS (Recursive Integration System) meta-operator with superposition and entropy-based collapse.
    Runs all four basic operations (+, -, *, /) in parallel, holding them in superposition.
    The system then collapses to the result with the lowest entropy or best fit for the context.
    
    Enhanced with improved entropy calculation, better edge case handling, and symbolic fallback.
    
    Args:
        a (float/complex): First operand
        b (float/complex): Second operand
        operation (str, optional): Force a specific operation instead of using entropy-based collapse
        
    Returns:
        Dict: {'result': value, 'operation': operation_name, 'entropy': entropy_score, 'all_results': {}}
    """
    import cmath
    # Symbolic fallback for nested RIS or string inputs
    if isinstance(a, str) or isinstance(b, str):
        return {
            'result': f"RIS({a}, {b})",
            'operation': 'symbolic',
            'entropy': float('inf'),
            'all_results': {}
        }
    # Enhanced entropy calculation
    def calc_entropy(n):
        if isinstance(n, complex):
            real_entropy = abs(n.real - round(n.real)) + abs(n.real) / 100
            imag_entropy = abs(n.imag - round(n.imag)) + abs(n.imag) / 100
            if n.imag == 0:
                return calc_entropy(n.real)
            if n.real == 0:
                return 5 + calc_entropy(n.imag)
            return 10 + real_entropy + imag_entropy
        if math.isnan(n) or math.isinf(n):
            return float('inf')
        integer_part = abs(n - round(n))
        magnitude_part = abs(n) / 100
        digits = len(str(abs(int(n)))) if n != 0 else 0
        bonus = 0
        if n > 0 and n == int(n) and math.sqrt(n).is_integer():
            bonus -= 0.5
        if n > 0 and n == int(n) and round(n**(1/3))**3 == n:
            bonus -= 0.3
        if n > 0 and n == int(n) and n & (n-1) == 0:
            bonus -= 0.4
        if n > 0 and n == int(n) and math.log10(n).is_integer():
            bonus -= 0.35
        if n in (1,2,3,4,5,6,7,8,9,10):
            bonus -= 0.6
        fibonacci = {1,2,3,5,8,13,21,34,55,89,144}
        if n == int(n) and int(n) in fibonacci:
            bonus -= 0.25
        return integer_part + magnitude_part + 0.05 * digits + bonus
    # Edge cases
    if ((isinstance(a, (int, float)) and a == 0) and (isinstance(b, (int, float)) and b == 0)):
        return {'result': 0, 'operation': 'add', 'entropy': 0.0, 'explanation': 'Addition for (0,0)', 'all_results': {'add': 0, 'mul': 0, 'sub': 0}}
    if ((isinstance(a, (int, float)) and math.isinf(a)) or (isinstance(b, (int, float)) and math.isinf(b))):
        if isinstance(b, (int, float)) and b > 1:
            return {'result': float('inf'), 'operation': 'mul', 'entropy': float('inf'), 'explanation': 'Multiplication for inf', 'all_results': {'add': float('inf'), 'mul': float('inf')}}
        elif isinstance(b, (int, float)) and b == 0:
            return {'result': float('inf') if math.isinf(a) else b, 'operation': 'add', 'entropy': float('inf'), 'explanation': 'Addition for inf+0', 'all_results': {'add': float('inf') if math.isinf(a) else b}}
        else:
            return {'result': float('inf'), 'operation': 'add', 'entropy': float('inf'), 'explanation': 'Addition for inf', 'all_results': {'add': float('inf')}}
    # Explicit operation
    if operation:
        try:
            if operation == 'add':
                result = a + b
            elif operation == 'sub':
                result = a - b
            elif operation == 'mul':
                result = a * b
            elif operation == 'div':
                if b == 0:
                    if a == 0:
                        return {'result': float('nan'), 'operation': operation, 'entropy': float('inf'), 'explanation': '0/0 undefined', 'all_results': {}}
                    return {'result': float('inf') if a > 0 else float('-inf'), 'operation': operation, 'entropy': float('inf'), 'explanation': 'Div by zero', 'all_results': {}}
                result = a / b
            elif operation == 'pow':
                result = a ** b
            elif operation == 'root':
                if b == 0:
                    return {'result': float('inf'), 'operation': operation, 'entropy': float('inf'), 'explanation': 'Root 0 index', 'all_results': {}}
                result = a ** (1/b)
            elif operation == 'log':
                if a <= 0 or b <= 0:
                    return {'result': float('nan'), 'operation': operation, 'entropy': float('inf'), 'explanation': 'Log requires positive', 'all_results': {}}
                result = math.log(b, a)
            elif operation == 'mod':
                if b == 0:
                    return {'result': float('nan'), 'operation': operation, 'entropy': float('inf'), 'explanation': 'Modulo by zero', 'all_results': {}}
                result = a % b
            else:
                raise ValueError(f"Unsupported operation: {operation}")
            return {'result': result, 'operation': operation, 'entropy': calc_entropy(result), 'explanation': f'Explicit {operation}', 'all_results': {operation: result}}
        except Exception as e:
            return {'result': f"Error: {str(e)}", 'operation': 'error', 'entropy': float('inf'), 'explanation': f'Error in {operation}: {str(e)}', 'all_results': {}}
    # All operations, select by entropy
    operations = {'add': a + b, 'sub': a - b, 'mul': a * b}
    if b != 0:
        operations['div'] = a / b
    else:
        operations['div'] = float('nan')
    entropies = {op: calc_entropy(val) for op, val in operations.items()}
    min_entropy_op = min(entropies.items(), key=lambda x: x[1])
    selected_op = min_entropy_op[0]
    selected_result = operations[selected_op]
    return {'result': selected_result, 'operation': selected_op, 'entropy': min_entropy_op[1], 'explanation': f'Selected {selected_op} (entropy {min_entropy_op[1]:.4f})', 'all_results': operations}
# --- Enhanced Recursive Compression Function ---
def recursive_compress(a: Union[float, complex], iterations: int = 1) -> Union[float, complex]:
    """
    Recursive compression function: f(a) = a / (1 + log(a+1))
    Handles both float and complex input.
    """
    import cmath
    if (isinstance(a, (int, float)) and a <= 0) or (isinstance(a, complex) and a.real <= 0 and a.imag == 0):
        return 0.0
    result = a
    for _ in range(iterations):
        if isinstance(result, complex):
            result = result / (1 + cmath.log(result + 1))
        else:
            result = result / (1 + math.log(result + 1))
    return result

# --- TFID (Temporal Frequency Identity) Anchoring ---
def tfid_anchor(value: Any, timestamp: Optional[float] = None) -> Dict[str, Any]:
    """
    Enhanced TFID (Temporal Frequency Identity) phase-locked identity anchor.
    Now with improved support for grid transformations and symbolic identity preservation.
    Able to maintain identity under rotation, transposition, and other grid transformations.
    
    Args:
        value: The value to create an identity anchor for
        timestamp: Optional timestamp to use for phase-locking
        
    Returns:
        Dict containing the identity signature
    """
    if timestamp is None:
        timestamp = time.time()
    
    # Special handling for grids (2D arrays)
    if isinstance(value, list) and all(isinstance(row, list) for row in value):
        # For grids, we compute a structure-preserving signature
        try:
            # Extract structural properties that are invariant under transformations
            grid = value
            grid_size = len(grid)
            
            # Check if it's a valid square grid
            is_square = all(len(row) == grid_size for row in grid)
            
            # Calculate grid sum for any grid type
            grid_sum = sum(sum(row) for row in grid if all(isinstance(x, (int, float)) for x in row))
            
            # Use a float to avoid overflow
            grid_product = 1.0
            for row in grid:
                for item in row:
                    if isinstance(item, (int, float)):
                        grid_product *= (item + 0.1)  # Add 0.1 to avoid multiplying by zero
            
            # For square grids, calculate additional invariant properties
            if is_square:
                # Calculate invariant sums (rows, columns, diagonals)
                row_sums = [sum(row) for row in grid]
                col_sums = [sum(col) for col in zip(*grid)]
                diag1_sum = sum(grid[i][i] for i in range(grid_size))
                diag2_sum = sum(grid[i][grid_size-1-i] for i in range(grid_size))
                
                # Sort invariant sums to ensure they're the same regardless of rotation
                invariant_sums = sorted(row_sums + col_sums + [diag1_sum, diag2_sum])
                invariant_hash = hash(tuple(invariant_sums))
            else:
                # For non-square grids, use a simpler invariant hash
                invariant_hash = hash(grid_sum)
            
            # Central element is often invariant in mathematical objects
            if grid_size % 2 == 1 and is_square:
                center = grid[grid_size // 2][grid_size // 2]
            else:
                # For even-sized grids, use the average of the center elements if possible
                if is_square and grid_size >= 2:
                    mid = grid_size // 2
                    center = (grid[mid-1][mid-1] + grid[mid-1][mid] + 
                             grid[mid][mid-1] + grid[mid][mid]) / 4
                else:
                    center = None
                
            # Create a transformation-invariant signature
            structure_hash = hash(grid_sum) ^ hash(grid_product) ^ (hash(center) if center is not None else 0)
            structure_hash ^= invariant_hash
                
            phase_signature = math.sin(timestamp * 0.001) * recursive_compress(abs(structure_hash))
            
            return {
                'value': value,
                'timestamp': timestamp,
                'grid_size': grid_size,
                'grid_sum': grid_sum,
                'center': center,
                'structure_hash': structure_hash,
                'phase_signature': phase_signature,
                'invariant_properties': {'product': grid_product, 'center': center},
                'tfid_hash': abs(structure_hash ^ int(timestamp * 1000))
            }
        except Exception as e:
            # Fall back to regular method for non-numeric grids
            print(f"TFID calculation error: {str(e)}")
      # Regular method for non-grid values
    # Generate phase-locked identity signature
    phase_signature = math.sin(timestamp * 0.001) * recursive_compress(abs(hash(str(value))))
    
    return {
        'value': value,
        'timestamp': timestamp,
        'phase_signature': phase_signature,
        'tfid_hash': abs(hash(str(value) + str(timestamp)))
    }
    
    return {
        'value': value,
        'timestamp': timestamp,
        'phase_signature': phase_signature,
        'tfid_hash': abs(hash(str(value) + str(timestamp)))
    }

# --- Superposition and Quantum Logic Functions ---
def superposition_collapse(values: List[Union[float, complex]], entropy_threshold: float = 0.1) -> Union[float, complex]:
    """
    Implements superposition of multiple values with entropy-based collapse.
    All possible outcomes are held simultaneously until collapse is triggered.
    
    Evidence: BlackwallV2 implements entropy-aware memory management with 
    documented stable operation across conversation sessions.
    """
    if not values:
        return 0.0
    
    # Calculate entropy for each value
    entropies = [len(str(abs(v)).replace('.', '')) for v in values]
    min_entropy_idx = entropies.index(min(entropies))
    
    # Collapse to lowest entropy value if below threshold
    if min(entropies) <= entropy_threshold * max(entropies):
        return values[min_entropy_idx]
    
    # Otherwise return compressed average
    avg = sum(values) / len(values)
    return recursive_compress(avg)

def split_args(argstr: str) -> list:
    """
    Split arguments by commas, ignoring nested brackets and complex structures.
    Enhanced to handle nested expressions and function calls more robustly.
    """
    args = []
    depth = 0
    last = 0
    bracket_pairs = {
        '[': ']',
        '{': '}',
        '(': ')',
        '<': '>'
    }
    
    i = 0
    while i < len(argstr):
        c = argstr[i]
        if c in bracket_pairs.keys():
            depth += 1
        elif c in bracket_pairs.values():
            depth -= 1
        elif c == ',' and depth == 0:
            args.append(argstr[last:i])
            last = i + 1
            
        # Handle special case for division <>...<> 
        if i < len(argstr) - 1 and c == '<' and argstr[i + 1] == '>':
            depth += 1
            i += 1  # Skip the next character
            
        # Handle special case for division close <> 
        if i > 0 and c == '>' and argstr[i - 1] == '<':
            depth -= 1
            
        i += 1
        
    if last < len(argstr):
        args.append(argstr[last:])
    return args

# Parse UML expressions with enhanced nesting, RIS operators, and recursive evaluation
def parse_uml(expr: str) -> Any:
    """
    Enhanced UML expression parser supporting:
    - Traditional math uses linearity and PEMDAS; RIS uses nesting, identity compression, and recursive resolution
    - Each operation is interpreted as a recursive instruction, not just a static calculation
    - Supports superposition logic and entropy-based collapse
    - Improved handling of complex expressions and nested structures
    - Now supports hybrid expressions: 2+<3,4>, [1,2]+3, 2*(3+4), etc.
    """
    expr = expr.replace(' ', '')

    # --- Hybrid infix operator parsing (IMPROVED) ---
    # Operator precedence: ^, *, /, +, -
    # We parse from lowest to highest precedence (rightmost lowest binds last)
    def split_top_level(expr, ops):
        depth = 0
        result = []
        for i, c in enumerate(expr):
            if c in '([{<':
                depth += 1
            elif c in ')]}>':
                depth -= 1
            elif depth == 0 and c in ops:
                result.append((i, c))
        return result

    # Try each operator in order of precedence (lowest first)
    for ops, op_name in [
        ('+-', None),
        ('*/', None),
        ('^', None)
    ]:
        splits = split_top_level(expr, ops)
        if splits:
            # For left-associative ops (+, -, *, /), split at the leftmost
            idx, op = splits[0] if ops != '^' else splits[-1]  # ^ is right-associative
            left = expr[:idx]
            right = expr[idx+1:]
            left_parsed = parse_uml(left)
            right_parsed = parse_uml(right)
            if op == '+':
                # Flatten nested additions for n-ary support
                if isinstance(left_parsed, dict) and left_parsed.get('op') == 'add':
                    return {'op': 'add', 'args': left_parsed['args'] + [right_parsed], 'type': 'hybrid'}
                if isinstance(right_parsed, dict) and right_parsed.get('op') == 'add':
                    return {'op': 'add', 'args': [left_parsed] + right_parsed['args'], 'type': 'hybrid'}
                return {'op': 'add', 'args': [left_parsed, right_parsed], 'type': 'hybrid'}
            elif op == '-':
                return {'op': 'sub', 'args': [left_parsed, right_parsed], 'type': 'hybrid'}
            elif op == '*':
                if isinstance(left_parsed, dict) and left_parsed.get('op') == 'mul':
                    return {'op': 'mul', 'args': left_parsed['args'] + [right_parsed], 'type': 'hybrid'}
                if isinstance(right_parsed, dict) and right_parsed.get('op') == 'mul':
                    return {'op': 'mul', 'args': [left_parsed] + right_parsed['args'], 'type': 'hybrid'}
                return {'op': 'mul', 'args': [left_parsed, right_parsed], 'type': 'hybrid'}
            elif op == '/':
                return {'op': 'div', 'args': [left_parsed, right_parsed], 'type': 'hybrid'}
            elif op == '^':
                return {'op': 'ris', 'args': [left_parsed, right_parsed], 'operation': 'pow', 'type': 'hybrid'}

    # --- Existing parsing logic ---
    # Handle priority nest (parentheses) - recursive evaluation
    if expr.startswith('(') and expr.endswith(')'):
        return parse_uml(expr[1:-1])
    
    # Addition nest: [ ... ] - 1D forward motion, growth, time steps
    if expr.startswith('[') and expr.endswith(']'):
        args = [parse_uml(x) for x in split_args(expr[1:-1])]
        return {'op': 'add', 'args': args, 'dimension': '1D', 'type': 'expansion'}
    
    # Subtraction nest: { ... } - 1D reverse motion, negation, backtracking
    if expr.startswith('{') and expr.endswith('}'):
        args = [parse_uml(x) for x in split_args(expr[1:-1])]
        return {'op': 'sub', 'args': args, 'dimension': '1D', 'type': 'collapse'}
    
    # Multiplication nest: < ... > - 2D expansion, scaling, tessellation
    if expr.startswith('<') and expr.endswith('>') and not (expr.startswith('<>') and expr.endswith('<>')):
        args = [parse_uml(x) for x in split_args(expr[1:-1])]
        return {'op': 'mul', 'args': args, 'dimension': '2D', 'type': 'tessellation'}
    
    # Division nest: <>...< > - 4D recursion, folding, superposition
    if '<>' in expr:
        # Enhanced division handling to properly match <>x,y<> pattern
        if expr.startswith('<>') and expr.endswith('<>'):
            content = expr[2:-2]
            if not content:
                raise ValueError(f"Empty division expression: {expr}")
                
            # Use the enhanced split_args to properly handle nested expressions
            args = [parse_uml(x) for x in split_args(content)]
            
            if not args:
                raise ValueError(f"Invalid division expression: {expr}")
            
            return {'op': 'div', 'args': args, 'dimension': '4D', 'type': 'recursion'}
        
        # Handle complex nested divisions like {10,<>5,2<>}
        # Look for a complete <>x,y<> pattern inside the expression
        match = re.search(r'<>([^<>]+)<>', expr)
        if match:
            # Process the non-division parts first
            inner_expr = match.group(1)
            inner_args = [parse_uml(x) for x in split_args(inner_expr)]
            div_expr = {'op': 'div', 'args': inner_args, 'dimension': '4D', 'type': 'recursion'}
            
            # Replace the division part with a placeholder for further parsing
            placeholder = "DIV_PLACEHOLDER"
            new_expr = expr.replace(f"<>{inner_expr}<>", placeholder)
            
            # If the placeholder is the entire expression, return the division
            if new_expr == placeholder:
                return div_expr
            
            # Otherwise, we need to parse the outer expression and substitute the division
            outer_parse = parse_uml(new_expr)
            
            if isinstance(outer_parse, dict) and 'args' in outer_parse:
                # Find and replace the placeholder in args
                for i, arg in enumerate(outer_parse['args']):
                    if arg == placeholder:
                        outer_parse['args'][i] = div_expr
                return outer_parse
    
    # Root: /x< - recursive collapse or expansion in non-integer domains
    if expr.startswith('/') and expr.endswith('<'):
        val = parse_uml(expr[1:-1])
        return {'op': 'root', 'args': [val], 'type': 'recursive_collapse'}
    
    # Logarithm: ?(a,b) - recursive compression and expansion
    if expr.startswith('?(') and expr.endswith(')'):
        vals = split_args(expr[2:-1])
        args = [parse_uml(x) for x in vals]
        return {'op': 'log', 'args': args, 'type': 'recursive_compression'}
    
    # RIS Meta-operator: @(a,b[,operation]) - superposition and entropy collapse
    if expr.startswith('@(') and expr.endswith(')'):
        vals = split_args(expr[2:-1])
        if len(vals) >= 2:
            args = [parse_uml(x) for x in vals[:2]]  # First two arguments are always the operands
            # Check for an explicit operation parameter
            operation = 'pow'  # Default operation
            if len(vals) > 2:
                # Remove quotes if present
                op_str = vals[2].strip("'\"")
                if op_str in ['pow', 'root', 'log', 'mod', 'add', 'sub', 'mul', 'div']:
                    operation = op_str
            
            return {'op': 'ris', 'args': args, 'operation': operation, 'type': 'meta_operator'}
    
    # Handle complex numbers: !(real,imag) - complex number representation
    if expr.startswith('!(') and expr.endswith(')'):
        vals = split_args(expr[2:-1])
        if len(vals) == 2:
            real = parse_uml(vals[0])
            imag = parse_uml(vals[1])
            return complex(real, imag)
    
    # Handle modulo operations like 10%3
    if '%' in expr and not (expr.startswith('[') or expr.startswith('{') or expr.startswith('<')):
        parts = expr.split('%')
        if len(parts) == 2:
            a = parse_uml(parts[0])
            b = parse_uml(parts[1])
            return a % b
    
    # Handle special constants
    if expr.lower() == 'pi':
        return math.pi
    elif expr.lower() == 'e':
        return math.e
    elif expr.lower() == 'inf':
        return float('inf')
    elif expr.lower() == 'nan':
        return float('nan')
    elif expr.lower() in ['i', 'j']:
        return complex(0, 1)
    
    # Single value (number or letter) with base-52 mapping
    if expr.isalpha() and len(expr) == 1:
        return parse_value(expr)
    
    # Multi-letter base-52 encoding
    if expr.isalpha():
        value = 0
        for char in expr:
            value = value * 52 + letter_to_number(char)
        return value
    
    # Try to parse as a number
    try:
        return float(expr)
    except ValueError:
        # Check if it's a complex number
        if expr == 'i' or expr == 'j':
            return complex(0, 1)
        elif expr.endswith('j') or expr.endswith('i'):
            try:
                return complex(expr.replace('i', 'j'))
            except ValueError:
                pass
        # If not a simple expression, try to handle function calls
        if '(' in expr and ')' in expr and expr.index('(') < expr.index(')'):
            func_name = expr[:expr.index('(')].strip()
            args_str = expr[expr.index('(')+1:expr.rindex(')')].strip()
            args = [parse_uml(x) for x in split_args(args_str)]
            
            # Handle RIS function call syntax explicitly
            if func_name.upper() == 'RIS':
                if len(args) < 2:
                    raise ValueError(f"RIS requires at least 2 arguments, got {len(args)}")
                    
                operation = 'auto'  # Default to auto operation selection
                if len(args) > 2:
                    operation_arg = args[2]
                    if isinstance(operation_arg, str) and operation_arg in ['add', 'sub', 'mul', 'div', 'pow', 'root', 'log', 'mod']:
                        operation = operation_arg
                
                return {'op': 'ris', 'args': args[:2], 'operation': operation, 'type': 'meta_operator'}
            
            # Handle common math functions
            if func_name == 'sin':
                return math.sin(args[0])
            elif func_name == 'cos':
                return math.cos(args[0])
            elif func_name == 'tan':
                return math.tan(args[0])
            elif func_name == 'sqrt':
                return math.sqrt(args[0]) if args[0] >= 0 else complex(0, math.sqrt(abs(args[0])))
            elif func_name == 'abs':
                return abs(args[0])
            elif func_name == 'log':
                if len(args) == 2:
                    return math.log(args[0], args[1])
                return math.log(args[0])
            else:
                raise ValueError(f"Unknown function: {func_name}")
        
        raise ValueError(f"Unsupported or invalid UML expression: {expr}")

# Enhanced UML evaluation with RIS meta-operator and recursive compression
def eval_uml(parsed_val: Any) -> Union[float, complex, str]:
    """
    Enhanced UML evaluation with RIS meta-operator, recursive compression, and symbolic preservation.
    Refactored for clarity and maintainability.
    """
    import cmath

    def eval_add(args):
        result = sum(args)
        return recursive_compress(result) if len(args) > 3 else result

    def eval_sub(args):
        return args[0] - sum(args[1:])

    def eval_mul(args):
        result = 1.0
        for a in args:
            result *= a
        return result

    def eval_div(args):
        result = args[0]
        for a in args[1:]:
            if a == 0:
                if args[0] == 0:
                    return float('nan')
                return float('inf')
            result /= a
        return result

    def eval_root(args):
        if len(args) == 1:
            val = args[0]
            if isinstance(val, complex) or (isinstance(val, (int, float)) and val < 0):
                return cmath.sqrt(val)
            return math.sqrt(val)
        elif len(args) == 2:
            base, index = args
            if index == 0:
                return float('inf')
            if isinstance(base, complex) or isinstance(index, complex):
                return base ** (1 / index)
            return base ** (1 / index)
        else:
            val = args[0]
            if isinstance(val, complex) or (isinstance(val, (int, float)) and val < 0):
                return cmath.sqrt(val)
            return math.sqrt(val)

    def eval_log(args):
        if len(args) == 2:
            base, value = args
            if isinstance(base, complex) or isinstance(value, complex) or base <= 0 or value <= 0:
                return cmath.log(value, base)
            return math.log(value, base)
        else:
            val = args[0]
            if isinstance(val, complex) or val <= 0:
                return cmath.log(val)
            return math.log(val)

    def eval_ris(parsed_val, args):
        a, b = args
        op = parsed_val.get('operation')
        if op == 'symbolic':
            return f"RIS({a}, {b})"
        if op == 'auto':
            try:
                operations = {
                    'add': a + b,
                    'mul': a * b,
                    'sub': a - b,
                    'div': a / b if b != 0 else float('inf')
                }
                def entropy_score(n):
                    if isinstance(n, complex):
                        real_entropy = abs(n.real - round(n.real)) + abs(n.real) / 100
                        imag_entropy = abs(n.imag - round(n.imag)) + abs(n.imag) / 100
                        if n.imag == 0:
                            return abs(n.real - round(n.real)) + abs(n.real) / 100
                        if n.real == 0:
                            return 5 + abs(n.imag - round(n.imag)) + abs(n.imag) / 100
                        return 10 + real_entropy + imag_entropy
                    if isinstance(n, (int, float)):
                        if math.isnan(n) or math.isinf(n):
                            return float('inf')
                        integer_part = abs(n - round(n))
                        magnitude_part = abs(n) / 100
                        digits = len(str(abs(int(n)))) if n != 0 else 0
                        bonus = 0
                        if n > 0 and n == int(n) and math.sqrt(n).is_integer():
                            bonus -= 0.5
                        if n > 0 and n == int(n) and round(n**(1/3))**3 == n:
                            bonus -= 0.3
                        if n > 0 and n == int(n) and n & (n-1) == 0:
                            bonus -= 0.4
                        if n > 0 and n == int(n) and math.log10(n).is_integer():
                            bonus -= 0.35
                        if n in (1,2,3,4,5,6,7,8,9,10):
                            bonus -= 0.6
                        fibonacci = {1,2,3,5,8,13,21,34,55,89,144}
                        if n == int(n) and int(n) in fibonacci:
                            bonus -= 0.25
                        return integer_part + magnitude_part + 0.05 * digits + bonus
                    return 100
                return min(operations.items(), key=lambda x: entropy_score(x[1]))[1]
            except Exception:
                return a + b
        try:
            if op == 'pow':
                return a ** b
            elif op == 'root':
                if b == 0:
                    return float('inf')
                if isinstance(a, (int, float)) and a < 0 and isinstance(b, (int, float)) and b % 2 == 0:
                    return complex(0, abs(a) ** (1/b))
                return a ** (1/b)
            elif op == 'log':
                if (isinstance(a, complex) or isinstance(b, complex) or (isinstance(a, (int, float)) and a <= 0) or (isinstance(b, (int, float)) and b <= 0)):
                    return cmath.log(b) / cmath.log(a) if a != 1 else float('inf')
                return math.log(b, a)
            elif op == 'mod':
                if isinstance(a, complex) and isinstance(b, complex):
                    return complex(a.real % b.real, a.imag % b.imag) if b != 0 else float('nan')
                elif isinstance(a, complex):
                    return complex(a.real % b, a.imag) if b != 0 else float('nan')
                elif isinstance(b, complex):
                    return complex(a % b.real, 0) if b.real != 0 else float('nan')
                return a % b if b != 0 else float('nan')
            elif op == 'add':
                return a + b
            elif op == 'sub':
                return a - b
            elif op == 'mul':
                return a * b
            elif op == 'div':
                return a / b if b != 0 else float('inf')
            else:
                return a + b
        except Exception:
            return float('nan')

    if isinstance(parsed_val, dict):
        op = parsed_val['op']
        args = [eval_uml(a) for a in parsed_val['args']]
        if op == 'add':
            return eval_add(args)
        if op == 'sub':
            return eval_sub(args)
        if op == 'mul':
            return eval_mul(args)
        if op == 'div':
            return eval_div(args)
        if op == 'root':
            return eval_root(args)
        if op == 'log':
            return eval_log(args)
        if op == 'ris':
            return eval_ris(parsed_val, args)
        # fallback for unknown op
        return float('nan')
    if isinstance(parsed_val, (int, float, complex)):
        return parsed_val
    return float('nan')
def eval_recursive_compress(expr_str: str) -> Union[float, complex, str]:
    """
    Evaluate UML expression and apply recursive compression.
    This combines parsing, evaluation, and compression in a single operation.
    """
    val = eval_uml(parse_uml(expr_str))
    # Handle string values (symbolic expressions) - don't compress them
    if isinstance(val, str):
        return val
    # Apply recursive compression for large numeric values
    if abs(val) > 10:
        return recursive_compress(val)
    else:
        return val
