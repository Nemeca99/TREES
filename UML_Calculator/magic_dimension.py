"""
Magic Square and Dimensional Expansion Tests for UML

This module provides validation and testing tools for:
1. Magic squares of perfect squares
2. 4D tesseract projections
3. Magic cubes
4. Nested squares (Magic Squares of Magic Squares)

It applies recursive_compress for fingerprint validation across all lines.
"""

import sys
import os
import math
import numpy as np
from typing import List, Tuple, Optional, Dict, Any

# Add the UML_Core directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from UML_Core.uml_core import recursive_compress, validate_magic_square
except ImportError:
    # Provide fallback implementations if the imports fail
    def recursive_compress(value):
        """Simple implementation of recursive compression"""
        if isinstance(value, (int, float)):
            return round(value * 100) / 100
        return value
    
    def validate_magic_square(grid):
        """Simple implementation of magic square validation"""
        if not grid or not grid[0]:
            return False, 0
            
        n = len(grid)
        if any(len(row) != n for row in grid):
            return False, 0
            
        # Calculate the expected sum: n(n²+1)/2
        expected_sum = n * (n**2 + 1) // 2
        
        # Check rows
        row_sums = [sum(row) for row in grid]
        if not all(s == expected_sum for s in row_sums):
            return False, 0
            
        # Check columns
        col_sums = [sum(grid[i][j] for i in range(n)) for j in range(n)]
        if not all(s == expected_sum for s in col_sums):
            return False, 0
            
        # Check main diagonal
        diag1_sum = sum(grid[i][i] for i in range(n))
        if diag1_sum != expected_sum:
            return False, 0
            
        # Check other diagonal
        diag2_sum = sum(grid[i][n-i-1] for i in range(n))
        if diag2_sum != expected_sum:
            return False, 0
            
        return True, expected_sum

# --- Enhanced Magic Square Validation ---
def validate_magic_square_of_squares(grid: List[List[int]]) -> Tuple[bool, int]:
    """
    Validates if a grid is a magic square where all entries are perfect squares.
    
    Args:
        grid: A 2D array representing the magic square
        
    Returns:
        Tuple[bool, int]: (is_valid, magic_sum)
    """
    # First check if it's a magic square
    is_magic, magic_sum = validate_magic_square(grid)
    if not is_magic:
        return False, 0
    
    # Check if all entries are perfect squares
    for row in grid:
        for value in row:
            # Check if value is a perfect square
            root = math.sqrt(value)
            if int(root) ** 2 != value:
                return False, 0
    
    return True, magic_sum

# --- Magic Cube Validation ---
def validate_magic_cube(cube: List[List[List[int]]]) -> Tuple[bool, int]:
    """
    Validates if a 3D cube is a magic cube.
    
    Args:
        cube: A 3D array representing the magic cube
        
    Returns:
        Tuple[bool, int]: (is_valid, magic_sum)
    """
    if not cube or not cube[0] or not cube[0][0]:
        return False, 0
    
    n = len(cube)
    if any(len(plane) != n for plane in cube) or any(len(row) != n for plane in cube for row in plane):
        return False, 0
    
    # Calculate the expected sum: n(n³+1)/2
    expected_sum = n * (n**3 + 1) // 2
    
    # Convert to numpy array for easier slicing
    cube_np = np.array(cube)
    
    # Check all rows along each dimension
    for dim in range(3):
        for i in range(n):
            for j in range(n):
                # Get line along dimension dim
                if dim == 0:
                    line = cube_np[i, j, :]
                elif dim == 1:
                    line = cube_np[i, :, j]
                else:  # dim == 2
                    line = cube_np[:, i, j]
                
                if sum(line) != expected_sum:
                    return False, 0
    
    # Check all diagonals (there are 4 space diagonals in a cube)
    diag1 = [cube_np[i, i, i] for i in range(n)]
    diag2 = [cube_np[i, i, n-i-1] for i in range(n)]
    diag3 = [cube_np[i, n-i-1, i] for i in range(n)]
    diag4 = [cube_np[i, n-i-1, n-i-1] for i in range(n)]
    
    if any(sum(diag) != expected_sum for diag in [diag1, diag2, diag3, diag4]):
        return False, 0
    
    return True, expected_sum

# --- Tesseract (4D) Projection Validation ---
def validate_tesseract_projection(projection: List[List[int]]) -> bool:
    """
    Validates if a 2D grid represents a valid projection of a 4D tesseract.
    This checks if the projection preserves certain mathematical properties.
    
    Args:
        projection: A 2D array representing the projection
        
    Returns:
        bool: Whether the projection is valid
    """
    if not projection or not projection[0]:
        return False
    
    # A 4D tesseract projection should have symmetry properties
    rows, cols = len(projection), len(projection[0])
    
    # Create fingerprints for each row and column
    row_fingerprints = [recursive_compress(sum(row)) for row in projection]
    col_fingerprints = [recursive_compress(sum(projection[i][j] for i in range(rows))) for j in range(cols)]
    
    # Check if the fingerprints have the expected patterns for tesseract projection
    # In a valid projection, certain symmetries should be preserved
    
    # Check for axial symmetry
    for i in range(rows // 2):
        if abs(row_fingerprints[i] - row_fingerprints[rows-i-1]) > 1e-10:
            return False
    
    for j in range(cols // 2):
        if abs(col_fingerprints[j] - col_fingerprints[cols-j-1]) > 1e-10:
            return False
    
    return True

# --- Nested Magic Squares Validation ---
def validate_nested_magic_squares(grid: List[List[List[List[int]]]]) -> bool:
    """
    Validates if a grid is a magic square of magic squares.
    Each cell in the outer magic square should itself be a valid magic square.
    
    Args:
        grid: A 4D array where grid[i][j] is a magic square at position (i,j) of the outer square
        
    Returns:
        bool: Whether it's a valid magic square of magic squares
    """
    if not grid or not grid[0]:
        return False
    
    outer_size = len(grid)
    if any(len(row) != outer_size for row in grid):
        return False
    
    # Check if each inner grid is a magic square
    inner_sums = []
    for i in range(outer_size):
        inner_row_sums = []
        for j in range(outer_size):
            inner_grid = grid[i][j]
            is_magic, magic_sum = validate_magic_square(inner_grid)
            if not is_magic:
                return False
            inner_row_sums.append(magic_sum)
        inner_sums.append(inner_row_sums)
    
    # Now check if the outer grid (made of inner magic sums) is itself a magic square
    is_outer_magic, _ = validate_magic_square(inner_sums)
    return is_outer_magic

# --- Test Functions ---

def test_magic_squares():
    """Test various types of magic squares"""
    print("\n=== Magic Square Tests ===")
    
    # Standard 3x3 magic square
    standard_magic_square = [
        [8, 1, 6],
        [3, 5, 7],
        [4, 9, 2]
    ]
    is_valid, magic_sum = validate_magic_square(standard_magic_square)
    print(f"Standard 3x3 Magic Square is valid: {is_valid}, Magic sum: {magic_sum}")
    
    # Magic square of perfect squares
    square_magic_square = [
        [16, 9, 25],
        [36, 49, 4],
        [64, 81, 1]
    ]
    is_valid, magic_sum = validate_magic_square_of_squares(square_magic_square)
    print(f"Magic Square of Perfect Squares is valid: {is_valid}, Magic sum: {magic_sum}")
    
    # 4x4 magic square
    magic_4x4 = [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1]
    ]
    is_valid, magic_sum = validate_magic_square(magic_4x4)
    print(f"4x4 Magic Square is valid: {is_valid}, Magic sum: {magic_sum}")
    
    # Apply recursive compression to get fingerprints
    print("\nRecursive Compression Fingerprints:")
    for row in standard_magic_square:
        compressed = [recursive_compress(val) for val in row]
        print(f"Row: {row} -> Compressed: {compressed}")

def test_magic_cube():
    """Test magic cube validation"""
    print("\n=== Magic Cube Tests ===")
    
    # Basic 3x3x3 magic cube
    magic_cube = np.zeros((3, 3, 3), dtype=int)
    
    # Fill with values from 1 to 27
    values = list(range(1, 28))
    
    # This is a simplified example, not a real magic cube
    for i in range(3):
        for j in range(3):
            for k in range(3):
                magic_cube[i, j, k] = values.pop(0)
    
    is_valid, magic_sum = validate_magic_cube(magic_cube.tolist())
    print(f"3x3x3 Cube is a magic cube: {is_valid}")
    
    # For demonstration - a correctly constructed magic cube would be valid

def test_tesseract_projection():
    """Test tesseract projection validation"""
    print("\n=== Tesseract Projection Tests ===")
    
    # Simple symmetric projection (not an actual tesseract, but with the right symmetry)
    symmetric_projection = [
        [1, 2, 2, 1],
        [2, 4, 4, 2],
        [2, 4, 4, 2],
        [1, 2, 2, 1]
    ]
    
    is_valid = validate_tesseract_projection(symmetric_projection)
    print(f"Symmetric projection is valid tesseract projection: {is_valid}")
    
    # Non-symmetric projection
    non_symmetric = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 8, 7, 6],
        [5, 4, 3, 2]
    ]
    
    is_valid = validate_tesseract_projection(non_symmetric)
    print(f"Non-symmetric projection is valid tesseract projection: {is_valid}")

def test_nested_squares():
    """Test nested magic squares validation"""
    print("\n=== Nested Magic Squares Tests ===")
    
    # Create a 2x2 outer square, where each cell is a 3x3 magic square
    nested_squares = []
    
    # Top-left: standard 3x3 magic square
    tl_square = [
        [8, 1, 6],
        [3, 5, 7],
        [4, 9, 2]
    ]
    
    # Top-right: another 3x3 magic square (rotated)
    tr_square = [
        [6, 1, 8],
        [7, 5, 3],
        [2, 9, 4]
    ]
    
    # Bottom-left: another variation
    bl_square = [
        [8, 3, 4],
        [1, 5, 9],
        [6, 7, 2]
    ]
    
    # Bottom-right: another variation
    br_square = [
        [4, 3, 8],
        [9, 5, 1],
        [2, 7, 6]
    ]
    
    nested_squares = [[tl_square, tr_square], [bl_square, br_square]]
    
    is_valid = validate_nested_magic_squares(nested_squares)
    print(f"Nested Magic Squares is valid: {is_valid}")

def main():
    """Run all tests"""
    test_magic_squares()
    test_magic_cube()
    test_tesseract_projection()
    test_nested_squares()

if __name__ == "__main__":
    main()
