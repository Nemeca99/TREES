with open('uml_core.py', 'r') as f:
    content = f.read()

# Fix imports
if 'from typing import Any, Dict, List, Tuple, Optional' in content:
    content = content.replace('from typing import Any, Dict, List, Tuple, Optional', 'from typing import Any, Dict, List, Tuple, Optional, Union')

# Fix the eval_uml function
if 'def eval_uml(parsed_val: Any) -> float:' in content:
    content = content.replace('def eval_uml(parsed_val: Any) -> float:', 'def eval_uml(parsed_val: Any) -> Union[float, complex]:')

# Fix the handling of complex numbers in parsing
if 'Try to parse as a number' in content:
    old_parse = '''    # Try to parse as a number
    try:
        return float(expr)
    except ValueError:
        # If not a simple expression, try to handle function calls'''
    
    new_parse = '''    # Try to parse as a number
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
    
    content = content.replace(old_parse, new_parse)

# Fix the return type in eval_uml
if 'elif isinstance(parsed_val, (int, float)):' in content:
    old_return = '''    elif isinstance(parsed_val, (int, float)):
        return float(parsed_val)
    else:
        raise ValueError(f"Cannot evaluate: {parsed_val}")'''
    
    new_return = '''    elif isinstance(parsed_val, (int, float, complex)):
        if isinstance(parsed_val, complex):
            return parsed_val
        return float(parsed_val)
    else:
        raise ValueError(f"Cannot evaluate: {parsed_val}")'''
    
    content = content.replace(old_return, new_return)

# Write the updated content back
with open('uml_core.py', 'w') as f:
    f.write(content)

print("Fixed the UML core file for complex number support.")
