import re

with open('uml_core.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the standard_to_uml conversion function to handle division and other operations better
conversion_pattern = re.compile(r'def convert_standard_to_uml\(expr: str\) -> str:.*?return expr', re.DOTALL)

new_conversion_function = '''def convert_standard_to_uml(expr: str) -> str:
    """
    Convert standard arithmetic expressions to UML notation.
    This allows traditional math notation to be parsed by UML.
    
    Examples:
    - "2+3" becomes "[2,3]" (addition)
    - "6-2" becomes "{6,2}" (subtraction)
    - "4*5" becomes "<4,5>" (multiplication)
    - "8/2" becomes "<>8,2<>" (division)
    - "2+3*4" becomes "[2,<3,4>]" (respecting PEMDAS)
    
    Evidence: Bridge function allowing UML to parse traditional notation.
    """
    # Handle already-UML notation
    if any(c in expr for c in "[]{}()<>@?/"):
        return expr
    
    # Handle common operators directly
    if '/' in expr and '*' not in expr and '+' not in expr and '-' not in expr:
        parts = expr.split('/')
        if len(parts) == 2:
            return f"<>{parts[0].strip()},{parts[1].strip()}<>"
    
    # First handle parentheses recursively
    paren_pattern = re.compile(r'\\(([^()]+)\\)')
    while '(' in expr:
        expr = re.sub(r'\\(([^()]+)\\)', lambda m: convert_standard_to_uml(m.group(1)), expr)
    
    # Convert basic operations (respecting PEMDAS)
    # Multiplication and division first
    expr = re.sub(r'(\\d+(?:\\.\\d+)?|\\w+)\\s*([*/])\\s*(\\d+(?:\\.\\d+)?|\\w+)',
                  lambda m: f"<{m.group(1)},{m.group(3)}>" if m.group(2) == '*' else f"<>{m.group(1)},{m.group(3)}<>",
                  expr)
    
    # Addition and subtraction last
    expr = re.sub(r'(\\d+(?:\\.\\d+)?|\\w+|\\<.+\\>)\\s*([+\\-])\\s*(\\d+(?:\\.\\d+)?|\\w+|\\<.+\\>)', 
                  lambda m: f"[{m.group(1)},{m.group(3)}]" if m.group(2) == '+' else f"{{{m.group(1)},{m.group(3)}}}",
                  expr)
    
    return expr'''

# We need to escape the regex pattern properly
new_conversion_function = new_conversion_function.replace('\\(', '\\\\(').replace('\\)', '\\\\)')
new_conversion_function = new_conversion_function.replace('\\d', '\\\\d').replace('\\s', '\\\\s')
new_conversion_function = new_conversion_function.replace('\\w', '\\\\w').replace('\\<', '\\\\<')
new_conversion_function = new_conversion_function.replace('\\>', '\\\\>').replace('\\.', '\\\\.')
new_conversion_function = new_conversion_function.replace('\\[', '\\\\[').replace('\\]', '\\\\]')
new_conversion_function = new_conversion_function.replace('\\+', '\\\\+').replace('\\-', '\\\\-')
new_conversion_function = new_conversion_function.replace('\\*', '\\\\*').replace('\\/', '\\\\/')

content = conversion_pattern.sub(new_conversion_function, content)

with open('uml_core.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated convert_standard_to_uml function for better operator handling.")
