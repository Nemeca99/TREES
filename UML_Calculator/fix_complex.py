import re

with open('uml_core.py', 'r', encoding='utf-8') as f:
    content = f.read()

# First, ensure we have the Union import
if 'from typing import Any, Dict, List, Tuple, Optional' in content:
    content = content.replace(
        'from typing import Any, Dict, List, Tuple, Optional', 
        'from typing import Any, Dict, List, Tuple, Optional, Union'
    )

# Fix the function signature
if 'def eval_uml(parsed_val: Any) -> float:' in content:
    content = content.replace(
        'def eval_uml(parsed_val: Any) -> float:',
        'def eval_uml(parsed_val: Any) -> Union[float, complex]:'
    )

# Complex pattern to find and replace the eval_uml function content while keeping indentation
eval_uml_pattern = re.compile(r'def eval_uml\(parsed_val: Any\).+?(?=def |$)', re.DOTALL)

def replacement(match):
    return '''def eval_uml(parsed_val: Any) -> Union[float, complex]:
    """
    Enhanced UML evaluator supporting RIS meta-operator, superposition logic,
    and recursive compression. Implements T.R.E.E.S. principles for entropy minimization.
    """
    if isinstance(parsed_val, dict):
        op = parsed_val['op']
        args = [eval_uml(a) for a in parsed_val['args']]
        
        if op == 'add':
            # Addition: 1D forward motion, growth
            result = sum(args)
            return recursive_compress(float(result)) if len(args) > 3 else result
            
        elif op == 'sub':
            # Subtraction: 1D reverse motion, negation
            result = args[0] - sum(args[1:])
            return result
            
        elif op == 'mul':
            # Multiplication: 2D expansion, tessellation
            result_mul = 1.0
            for a in args:
                result_mul *= a
            return result_mul
            
        elif op == 'div':
            # Division: 4D recursion, folding, superposition
            result_div = args[0]
            for a in args[1:]:
                if a == 0:
                    if args[0] == 0:
                        return float('nan')  # 0/0 = NaN
                    return float('inf')  # Handle division by zero
                result_div /= a
            return result_div
            
        elif op == 'root':
            # Root: recursive collapse in non-integer domains
            if len(args) == 1:
                if isinstance(args[0], (int, float)) and args[0] < 0:
                    return complex(0, math.sqrt(abs(args[0])))
                return math.sqrt(args[0])
            elif len(args) == 2:
                base, index = args
                if index == 0:
                    return float('inf')
                return base ** (1 / index)
            else:
                if isinstance(args[0], (int, float)) and args[0] < 0:
                    return complex(0, math.sqrt(abs(args[0])))
                return math.sqrt(args[0])
                
        elif op == 'log':
            # Logarithm: recursive compression and expansion
            if len(args) == 2:
                base, value = args
                if isinstance(base, (int, float)) and isinstance(value, (int, float)):
                    if base <= 0 or value <= 0:
                        return float('nan')
                    return math.log(value, base)
                return float('nan')
            else:
                if isinstance(args[0], (int, float)) and args[0] > 0:
                    return math.log(args[0])
                return float('nan')
                
        elif op == 'ris':
            # RIS Meta-operator: superposition and entropy collapse
            if len(args) == 2:
                # Check if an explicit operation was requested
                if 'operation' in parsed_val:
                    result, _ = ris_meta_operator(float(args[0]), float(args[1]), parsed_val['operation'])
                else:
                    result, _ = ris_meta_operator(float(args[0]), float(args[1]))
                return result
            else:
                # Apply superposition collapse to multiple arguments
                return superposition_collapse([float(arg) for arg in args])
                
        else:
            raise ValueError(f"Unknown operator: {op}")
            
    elif isinstance(parsed_val, (int, float, complex)):
        if isinstance(parsed_val, complex):
            return parsed_val
        return float(parsed_val)
    else:
        raise ValueError(f"Cannot evaluate: {parsed_val}")
'''

if eval_uml_pattern.search(content):
    content = eval_uml_pattern.sub(replacement, content)
else:
    print("Could not find the eval_uml function pattern in the file.")

# Add complex number support to parse_uml
parse_number_pattern = re.compile(r'''    # Try to parse as a number
    try:
        return float\(expr\)
    except ValueError:
        # If not a simple expression, try to handle function calls''')

new_parse_number = '''    # Try to parse as a number
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
                
        # If not a simple expression, try to handle function calls'''

content = parse_number_pattern.sub(new_parse_number, content)

with open('uml_core.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated uml_core.py with complex number support.")
