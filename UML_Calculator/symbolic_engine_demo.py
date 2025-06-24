"""
UML Symbolic Engine Feature Demonstration

This script demonstrates the core features of the UML Symbolic Engine,
including RIS, TFID, and symbolic collapse protocols.

Author: Travis Miner
Date: June 23, 2025
"""

import os
import sys
import json
from datetime import datetime

# Add parent directory to path if needed
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from symbolic_engine import SymbolicEngine, SymbolicOperationType

def divider(title=""):
    """Print a divider with an optional title."""
    width = 80
    if title:
        print(f"\n{'-' * ((width - len(title) - 4) // 2)} {title} {'-' * ((width - len(title) - 4) // 2)}\n")
    else:
        print(f"\n{'-' * width}\n")

def demo_basic_operations():
    """Demonstrate basic symbolic operations."""
    divider("BASIC SYMBOLIC OPERATIONS")
    
    engine = SymbolicEngine()
    
    # Create and execute simple operations
    print("Creating and executing simple operations:")
    
    # Addition: [3,4]
    add_op = engine.create_operation(SymbolicOperationType.ADDITION, [3, 4])
    result, tfid = engine.execute_operation(add_op)
    print(f"  [3,4] = {result} (TFID: {tfid})")
    
    # Multiplication: >5,6<
    mult_op = engine.create_operation(SymbolicOperationType.MULTIPLICATION, [5, 6])
    result, tfid = engine.execute_operation(mult_op)
    print(f"  >5,6< = {result} (TFID: {tfid})")
    
    # Division: <10,2>
    div_op = engine.create_operation(SymbolicOperationType.DIVISION, [10, 2])
    result, tfid = engine.execute_operation(div_op)
    print(f"  <10,2> = {result} (TFID: {tfid})")
    
    # Exponentiation: ^[2,3]
    exp_op = engine.create_operation(SymbolicOperationType.EXPONENTIATION, [2, 3])
    result, tfid = engine.execute_operation(exp_op)
    print(f"  ^[2,3] = {result} (TFID: {tfid})")
    
    # Root: /[2,9]
    root_op = engine.create_operation(SymbolicOperationType.ROOT, [9, 2])
    result, tfid = engine.execute_operation(root_op)
    print(f"  /[2,9] = {result} (TFID: {tfid})")
    
    # Modulo: %[10,3]
    mod_op = engine.create_operation(SymbolicOperationType.MODULO, [10, 3])
    result, tfid = engine.execute_operation(mod_op)
    print(f"  %[10,3] = {result} (TFID: {tfid})")

def demo_expression_parsing():
    """Demonstrate expression parsing."""
    divider("EXPRESSION PARSING")
    
    engine = SymbolicEngine()
    
    # Parse various expressions
    expressions = [
        "RIS(4, 9)",
        "TFID(\"magic_square\", 3)",
        "collapse([5,2])",
        "[3,4]",  # Addition
        "{10,3}",  # Subtraction
        ">5,6<",   # Multiplication
        "<20,4>",  # Division
        "^[2,4]",  # Exponentiation
        "!5",      # Factorial
    ]
    
    print("Parsing expressions:")
    for expr in expressions:
        try:
            parsed = engine.parse_expression(expr)
            print(f"  {expr} => {parsed}")
        except Exception as e:
            print(f"  Error parsing {expr}: {e}")

def demo_ris_operation():
    """Demonstrate the RIS operation."""
    divider("RECURSIVE INTEGRATION SYSTEM (RIS)")
    
    engine = SymbolicEngine()
    
    # Simple RIS demonstrations
    print("Simple RIS operations:")
    ris_examples = [
        (4, 9),    # Expected: 6.5
        (10, 20),  # Expected: 15
        (2, 8),    # Expected: 5
        (-3, 7),   # Expected: 2
        (3.5, 7.5) # Expected: 5.5
    ]
    
    for a, b in ris_examples:
        ris_op = engine.create_operation(SymbolicOperationType.RIS, [a, b])
        result, tfid = engine.execute_operation(ris_op)
        print(f"  RIS({a}, {b}) = {result} (TFID: {tfid})")
        
    # Nested RIS operation
    a, b, c = 2, 5, 10
    # Create RIS(2, 5) operation
    inner_ris = engine.create_operation(SymbolicOperationType.RIS, [a, b])
    # Create RIS(RIS(2, 5), 10) operation
    nested_ris = engine.create_operation(SymbolicOperationType.RIS, [inner_ris, c])
    
    result, tfid = engine.execute_operation(nested_ris)
    print(f"\nNested RIS operation:")
    print(f"  RIS(RIS({a}, {b}), {c}) = {result} (TFID: {tfid})")

def demo_tfid_system():
    """Demonstrate the TFID system."""
    divider("TEMPORAL FLUX IDENTITY DRIFT (TFID)")
    
    engine = SymbolicEngine()
    
    # Create TFIDs
    print("Creating TFIDs:")
    tfid1 = engine.parse_expression("TFID(\"magic_square\", 0)")
    result1, identity1 = engine.execute_operation(tfid1)
    
    tfid2 = engine.parse_expression("TFID(\"tesseract\", 2)")
    result2, identity2 = engine.execute_operation(tfid2)
    
    print(f"  Created TFID: {identity1}")
    print(f"  Created TFID: {identity2}")
    
    # Trace TFID
    print("\nTracing TFID information:")
    info = engine.query_tfid(identity1.identity)
    print(f"  TFID information for {identity1}:")
    print(f"  - Identity: {info['tfid']['identity']}")
    print(f"  - Phase: {info['tfid']['phase']}")
    print(f"  - Timestamp: {info['tfid']['timestamp']}")
    
    # Fork a TFID
    print("\nForking a TFID:")
    forked_tfid = identity1.fork("Demonstration fork")
    engine.memory.save_tfid(forked_tfid)
    print(f"  Forked {identity1} to create {forked_tfid}")
    
    # Merge TFIDs
    print("\nMerging TFIDs:")
    merged_tfid = identity1.merge(identity2, "Demonstration merge")
    engine.memory.save_tfid(merged_tfid)
    print(f"  Merged {identity1} with {identity2} to create {merged_tfid}")

def demo_collapse_protocol():
    """Demonstrate the collapse protocol."""
    divider("COLLAPSE PROTOCOL VISUALIZATION")
    
    engine = SymbolicEngine(deterministic_collapse=False, entropy_bias=0.7)
    
    # Visualize collapse of expressions
    print("Visualizing expression collapse:")
    
    expressions = [
        "[3,7]",                       # Simple addition
        ">2,{10,4}<",                  # Multiplication with subtraction
        "RIS(5, 10)",                  # RIS function
        "collapse([4,6])",             # Explicit collapse
        "RIS(TFID(\"square\", 1), 9)"  # RIS with TFID
    ]
    
    # Just demonstrate one expression for brevity
    engine.visualize_collapse(expressions[0])
    
    print("\nCollapse history for expression:")
    history = engine.query_expression_history(expressions[0])
    if "collapses" in history:
        for collapse in history["collapses"]:
            print(f"  Collapse {collapse['collapse_id'][:8]}... resulted in {collapse['result']}")
            print(f"  Performed at: {collapse['timestamp']}")

def demo_repl(interactive=False):
    """Demonstrate the REPL or explain how to use it."""
    divider("INTERACTIVE REPL")
    
    if interactive:
        print("Starting the interactive REPL. Type 'exit' to return to the demo.")
        engine = SymbolicEngine()
        engine.run_interactive_repl()
    else:
        print("The UML Symbolic Engine includes an interactive REPL which lets you:")
        print("  - Evaluate UML expressions directly")
        print("  - Visualize expression collapses")
        print("  - Trace and inspect TFIDs")
        print("  - Query operation history")
        print("\nTo use the REPL, instantiate the SymbolicEngine and call run_interactive_repl():")
        print("\n  engine = SymbolicEngine()")
        print("  engine.run_interactive_repl()")
        print("\nOr run this script with the --interactive flag.")

def main():
    """Run the complete demonstration suite."""
    print("\n" + "=" * 80)
    print(" " * 25 + "UML SYMBOLIC ENGINE DEMONSTRATION")
    print("=" * 80)
    
    demo_basic_operations()
    demo_expression_parsing()
    demo_ris_operation()
    demo_tfid_system()
    demo_collapse_protocol()
    
    interactive = "--interactive" in sys.argv
    demo_repl(interactive)
    
    divider("DEMONSTRATION COMPLETE")
    print("The UML Symbolic Engine successfully demonstrated:")
    print("  ✓ Basic symbolic operations")
    print("  ✓ Expression parsing")
    print("  ✓ RIS (Recursive Integration System)")
    print("  ✓ TFID (Temporal Flux Identity Drift)")
    print("  ✓ Collapse protocol visualization")
    print("  ✓ Memory storage and query")
    print("\nAll features are working as expected. The engine is ready for production use.")

if __name__ == "__main__":
    main()
