"""
UML Calculator Feature Demonstration

This module demonstrates the core features of the UML Calculator, including:
1. Basic UML syntax and operations
2. RIS meta-operator with explicit operations
3. Symbolic identity and fingerprinting
4. Recursive compression
5. Magic squares and tesseract projections
6. T.R.E.E.S principles in action

Run this script to see interactive demonstrations of key UML features.
"""

import sys
import os
from datetime import datetime
import time

# Import UML core modules using relative imports
try:
    # Direct import when running from UML_Core
    from uml_core import (
        parse_uml, eval_uml, recursive_compress,
        ris_meta_operator, tfid_anchor, superposition_collapse,
        validate_magic_square
    )
    from safe_eval import safe_eval
    from symbolic_extensions import demo_symbolic_extensions
except ImportError:
    # Fallback for different directory structures
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from uml_core import (
        parse_uml, eval_uml, recursive_compress,
        ris_meta_operator, tfid_anchor, superposition_collapse,
        validate_magic_square
    )
    from safe_eval import safe_eval
    from symbolic_extensions import demo_symbolic_extensions

def print_header(title):
    """Print a formatted header for sections."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def demonstrate_basic_uml():
    """Demonstrate basic UML syntax and operations."""
    print_header("Basic UML Syntax and Operations")
    examples = [
        ("[3,4]", "Addition: 3 + 4"),
        ("{10,3}", "Subtraction: 10 - 3"),
        ("<5,6>", "Multiplication: 5 * 6"),
        ("<>20,4<>", "Division: 20 / 4"),
        ("@(2,8)", "Power (RIS): 2^8"),
        ("[<3,4>,{10,2}]", "Complex: (3*4)+(10-2)"),
    ]
    
    for uml_expr, description in examples:
        parsed = parse_uml(uml_expr)
        result = eval_uml(parsed)
        print(f"{description:<30} | {uml_expr:<20} = {result}")

def demonstrate_ris_operator():
    """Demonstrate the RIS meta-operator with various operations."""
    print_header("RIS Meta-Operator with Explicit Operations")
    
    operations = [
        (5, 2, None),      # Auto-select based on entropy
        (5, 2, "add"),     # Addition: 5+2=7
        (5, 2, "sub"),     # Subtraction: 5-2=3
        (5, 2, "mul"),     # Multiplication: 5*2=10
        (5, 2, "div"),     # Division: 5/2=2.5
        (5, 2, "pow"),     # Power: 5^2=25
        (5, 2, "root"),    # Root: 5^(1/2)≈2.236
        (100, 10, "log"),  # Log: log_10(100)=2
    ]
    
    print("a | b | operation | result | selected_op")
    print("-"*50)
    for a, b, op in operations:
        result, selected_op = ris_meta_operator(a, b, op)
        print(f"{a:<3} | {b:<3} | {str(op):<10} | {result:<10.4f} | {selected_op}")

def demonstrate_symbolic_identity():
    """Demonstrate symbolic identity and fingerprinting."""
    print_header("Symbolic Identity and Fingerprinting")
    
    expressions = [
        "3 + 4",
        "[3,4]",  # UML equivalent
        "(3+4)*5",
        "<[3,4],5>"  # UML equivalent
    ]
    
    print("Expression | Value | Compressed Value | TFID Hash")
    print("-"*70)
    for expr in expressions:
        if expr[0] in "[{<@":  # UML syntax
            parsed = parse_uml(expr)
            value = eval_uml(parsed)
        else:  # Standard syntax
            value = safe_eval(expr)
            
        compressed = recursive_compress(value)
        tfid = tfid_anchor(value)
        
        print(f"{expr:<15} | {value:<6} | {compressed:<16.4f} | {tfid['tfid_hash']}")

def demonstrate_magic_squares():
    """Demonstrate magic square validation and properties."""
    print_header("Magic Square Validation")
    
    # Standard 3x3 magic square
    magic_square = [
        [8, 1, 6],
        [3, 5, 7],
        [4, 9, 2]
    ]
      # Non-magic square
    non_magic = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    
    result = validate_magic_square(magic_square)
    print(f"Standard 3x3 Magic Square is valid: {result['line_sum_uniform']}, Magic sum: {result['target_sum']}")
    
    result = validate_magic_square(non_magic)
    print(f"Non-magic Square is valid: {result['line_sum_uniform']}")
    
    print("\nMagic Square Transformation using Recursive Compression:")
    transformed = [[recursive_compress(cell) for cell in row] for row in magic_square]
    for row in transformed:
        print(row)

def demonstrate_trees_principles():
    """Demonstrate T.R.E.E.S principles in action."""
    print_header("T.R.E.E.S. Principles in Action")
    
    # Demonstrate superposition collapse with entropy-based selection
    values = [3.14159, 3.1, 3.14, 3.142]
    result = superposition_collapse(values)
    print(f"Superposition collapse of {values} -> {result}")
    
    # Demonstrate recursive compression with phase-locked timing
    value = 3.14159265358979323846
    start = time.time()
    compressed = recursive_compress(value)
    duration = time.time() - start
    
    print(f"Recursive compression of {value} -> {compressed}")
    print(f"Compression duration: {duration:.8f} seconds")
    
    # Demonstrate TFID anchoring with phase timing
    tfid = tfid_anchor(value)
    print(f"TFID anchor for {value}:")
    for k, v in tfid.items():
        print(f"  {k}: {v}")

def main():
    """Run all demonstrations."""
    print("\nUML CALCULATOR FEATURE DEMONSTRATION")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nThis demonstration showcases the core capabilities of the UML Calculator")
    print("and Universal Mathematical Language system.\n")
    
    # Run demos
    demonstrate_basic_uml()
    demonstrate_ris_operator()
    demonstrate_symbolic_identity()
    demonstrate_magic_squares()
    demonstrate_trees_principles()
    
    # Additional demos from symbolic extensions
    demo_symbolic_extensions()

if __name__ == "__main__":
    main()
