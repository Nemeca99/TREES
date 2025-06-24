import re

with open('safe_eval.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the function calls issue in _eval_node
call_pattern = re.compile(r'''    # Function calls
    elif isinstance\(node, ast\.Call\):
        if not isinstance\(node\.func, ast\.Name\):
            raise ValueError\("Complex function calls not supported"\)''')

new_call_code = '''    # Function calls
    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            # Try to handle more complex function calls by evaluating the function first
            try:
                func = _eval_node(node.func)
                args = [_eval_node(arg) for arg in node.args]
                return func(*args)
            except Exception as e:
                raise ValueError(f"Complex function call error: {str(e)}")'''

content = call_pattern.sub(new_call_code, content)

with open('safe_eval.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated safe_eval.py to support more complex function calls.")
