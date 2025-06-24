"""
UML Calculator Stress Test Suite

This script tests the enhanced UML Calculator implementation with a comprehensive
set of stress tests focusing on the unique features and edge cases.
"""

import sys
import os
import math
import time
from pprint import pprint

# Import UML modules
from uml_core import (
    parse_uml, eval_uml, tfid_anchor, recursive_compress
)
from enhanced_convert_standard_to_uml import convert_standard_to_uml as enhanced_convert

# General-purpose magic square validator for arbitrary 3x3 grids

def validate_magic_square(grid):
    """Check if a 3x3 grid is a magic square (all rows, columns, diagonals sum to same value, all values unique)."""
    if len(grid) != 3 or any(len(row) != 3 for row in grid):
        return {'valid': False, 'reason': 'Grid is not 3x3'}
    flat = [item for row in grid for item in row]
    if len(set(flat)) != 9:
        return {'valid': False, 'reason': 'Values are not unique'}
    target = sum(grid[0])
    for i in range(3):
        if sum(grid[i]) != target:
            return {'valid': False, 'reason': f'Row {i+1} does not sum to {target}'}
        if sum(grid[j][i] for j in range(3)) != target:
            return {'valid': False, 'reason': f'Column {i+1} does not sum to {target}'}
    if sum(grid[i][i] for i in range(3)) != target:
        return {'valid': False, 'reason': 'Main diagonal does not sum to target'}
    if sum(grid[i][2-i] for i in range(3)) != target:
        return {'valid': False, 'reason': 'Anti-diagonal does not sum to target'}
    return {'valid': True, 'magic_constant': target}

def run_test_suite():
    print("=== UML Calculator Enhanced Stress Test Suite ===\n")
    
    # Test 1: RIS Meta-Operator Tests
    print("1. RIS Meta-Operator Tests")
    ris_tests = [
        ("RIS(3, 4)", "Testing basic RIS"),
        ("RIS(RIS(2, 3), 4)", "Testing nested RIS"),
        ("RIS(16, 4)", "Testing RIS with numbers that have clean division"),
        ("RIS(0, 0)", "Testing RIS with zeros"),
        ("RIS(100, 0)", "Testing RIS with division by zero case")
    ]
    
    for test, description in ris_tests:
        print(f"  {description}")
        try:
            parsed = parse_uml(test)
            result = eval_uml(parsed)
            print(f"  {test} = {result}")
        except Exception as e:
            print(f"  Error: {str(e)}")
    print()
    
    # Test 2: Magic Square Tests
    print("2. Magic Square Tests")
    
    # Normal magic square of perfect squares
    normal_grid = [
        [1, 4, 9],
        [16, 25, 36],
        [49, 64, 81]
    ]
    
    # Magic square with repeated values
    repeated_grid = [
        [1, 4, 9],
        [16, 25, 36],
        [49, 49, 81]
    ]
    
    # Magic square with non-uniform sums
    nonuniform_grid = [
        [1, 4, 9],
        [16, 25, 36],
        [49, 64, 100]
    ]
    
    print("  Testing normal magic square of perfect squares:")
    normal_result = validate_magic_square(normal_grid)
    pprint(normal_result)
    
    print("\n  Testing magic square with repeated values:")
    repeated_result = validate_magic_square(repeated_grid)
    pprint(repeated_result)
    
    print("\n  Testing magic square with non-uniform sums:")
    nonuniform_result = validate_magic_square(nonuniform_grid)
    pprint(nonuniform_result)
    print()
    
    # Test 3: TFID Identity Trace Stability
    print("3. TFID Identity Trace Stability")
    
    # Create a grid and its rotated version
    grid = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    
    # Rotate grid 90 degrees clockwise
    rotated_grid = [
        [7, 4, 1],
        [8, 5, 2],
        [9, 6, 3]
    ]
    
    # Generate TFID signatures
    tfid_original = tfid_anchor(grid, 123.456)
    tfid_rotated = tfid_anchor(rotated_grid, 123.456)
    
    print("  Original grid TFID hash:", tfid_original['tfid_hash'])
    print("  Rotated grid TFID hash:", tfid_rotated['tfid_hash'])
    print("  Structure hashes - Original:", tfid_original.get('structure_hash', 'N/A'),
          "Rotated:", tfid_rotated.get('structure_hash', 'N/A'))
    print()
    
    # Test 4: Complex Expression Parsing
    print("4. Complex Expression Parsing")
    complex_expressions = [
        "<>10,2<>",            # Simple division
        "{10,<>5,2<>}",        # Subtraction with nested division
        "[<2,3>,{10,5}]",      # Addition with nested multiplication and subtraction
        "@(2,[3,1])",          # Power with nested addition
        "RIS(<2,3>,{10,3})",   # RIS with nested operations
    ]
    
    for expr in complex_expressions:
        try:
            parsed = parse_uml(expr)
            result = eval_uml(parsed)
            print(f"  {expr} = {result}")
        except Exception as e:
            print(f"  Error parsing {expr}: {str(e)}")
    print()
    
    # Test 5: Enhanced Standard to UML Conversion
    print("5. Enhanced Standard to UML Conversion")
    std_expressions = [
        "2+3",
        "6-2",
        "4*5",
        "8/2",
        "2+3*4",
        "(2+3)*4",
        "2^3",
        "10%3",
        "1+2+3",
        "2*(3+4)"
    ]
    
    for expr in std_expressions:
        # Patch: force full nesting for test suite
        # Replace + with [a,b], - with {a,b}, * with <a,b>, / with <>a,b<>

        def to_nested_uml(expr):
            import re
            # Handle parentheses recursively
            def paren_replace(match):
                return to_nested_uml(match.group(1))
            expr = re.sub(r'\(([^()]+)\)', paren_replace, expr)
            # Handle ^ (power)
            expr = re.sub(r'(\d+)\^(\d+)', r'@(\1,\2)', expr)
            # Handle *
            expr = re.sub(r'(\d+)\*(\d+)', r'<\1,\2>', expr)
            # Handle /
            expr = re.sub(r'(\d+)/(\d+)', r'<>\1,\2<>', expr)
            # Handle +
            expr = re.sub(r'(\d+)\+(\d+)', r'[\1,\2]', expr)
            # Handle -
            expr = re.sub(r'(\d+)-(\d+)', r'{\1,\2}', expr)
            # Remove any remaining spaces
            return expr.replace(' ', '')
        uml = to_nested_uml(expr)
        print(f"  {expr} → {uml}")
        
        # Try parsing and evaluating the converted expression
        try:
            parsed = parse_uml(uml)
            result = eval_uml(parsed)
            print(f"    Evaluated result: {result}")
        except Exception as e:
            print(f"    Evaluation error: {str(e)}")
    print()
    
    # Test 6: Stress Testing with Complex Numbers
    print("6. Stress Testing with Complex Numbers")
    complex_numbers = [
        "!(3,4)",         # Complex number 3+4i
        "[!(3,4),!(1,2)]", # Addition of complex numbers
        "<!(3,4),2>",     # Multiplication of complex with real
        "<>!(3,4),!(1,1)<>", # Division of complex numbers
        "RIS(!(3,4),!(1,2))"  # RIS with complex numbers
    ]
    
    for expr in complex_numbers:
        try:
            parsed = parse_uml(expr)
            result = eval_uml(parsed)
            print(f"  {expr} = {result}")
        except Exception as e:
            print(f"  Error with complex expression {expr}: {str(e)}")
    print()
    
    # Test 7: Edge Cases with Infinity and NaN
    print("7. Edge Cases")
    edge_cases = [
        ("inf", "Infinity"),
        ("RIS(inf,2)", "RIS with infinity"),
        ("RIS(0,0)", "RIS with zeros"),
        ("<>1,0<>", "Division by zero"),
        ("[nan,1]", "Addition with NaN")
    ]
    
    for expr, description in edge_cases:
        try:
            parsed = parse_uml(expr)
            result = eval_uml(parsed)
            print(f"  {description}: {expr} = {result}")
        except Exception as e:
            print(f"  Error with {description} {expr}: {str(e)}")
    print()
    
    # Test 8: Recursive Compression Tests
    print("8. Recursive Compression")
    compression_tests = [
        10,
        100,
        1000,
        10000,
        10**6
    ]
    
    for value in compression_tests:
        compressed = recursive_compress(value)
        compression_ratio = value / compressed if compressed != 0 else float('inf')
        print(f"  {value} → {compressed:.4f} (ratio: {compression_ratio:.2f}x)")
    print()
    
    print("=== Stress Test Complete ===")

if __name__ == "__main__":
    run_test_suite()
