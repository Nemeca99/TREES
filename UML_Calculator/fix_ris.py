import re

with open('uml_core.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix ris_meta_operator to handle complex numbers
ris_pattern = re.compile(r'def ris_meta_operator\(a: float, b: float, operation: Optional\[str\] = None\) -> Tuple\[float, str\]:')

new_ris_signature = 'def ris_meta_operator(a: Union[float, complex], b: Union[float, complex], operation: Optional[str] = None) -> Tuple[Union[float, complex], str]:'

content = ris_pattern.sub(new_ris_signature, content)

# Fix the complex number handling for RIS in eval_uml
ris_eval_pattern = re.compile(r'''                if 'operation' in parsed_val:
                    result, _ = ris_meta_operator\(float\(args\[0\]\), float\(args\[1\]\), parsed_val\['operation'\]\)
                else:
                    result, _ = ris_meta_operator\(float\(args\[0\]\), float\(args\[1\]\)\)''')
                    
new_ris_eval = '''                if 'operation' in parsed_val:
                    result, _ = ris_meta_operator(args[0], args[1], parsed_val['operation'])
                else:
                    result, _ = ris_meta_operator(args[0], args[1])'''

content = ris_eval_pattern.sub(new_ris_eval, content)

# Fix superposition_collapse to handle complex numbers
collapse_pattern = re.compile(r'def superposition_collapse\(values: List\[float\], entropy_threshold: float = 0.1\) -> float:')

new_collapse_signature = 'def superposition_collapse(values: List[Union[float, complex]], entropy_threshold: float = 0.1) -> Union[float, complex]:'

content = collapse_pattern.sub(new_collapse_signature, content)

# Fix the superposition_collapse call
collapse_call_pattern = re.compile(r'                return superposition_collapse\(\[float\(arg\) for arg in args\]\)')
new_collapse_call = '                return superposition_collapse(args)'
content = collapse_call_pattern.sub(new_collapse_call, content)

with open('uml_core.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated uml_core.py with better complex number support in RIS operations.")
