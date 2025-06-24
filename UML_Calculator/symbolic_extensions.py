"""
Symbolic Extensions for UML Calculator
Additional symbolic and numeric features extracted from Algebra/Calculator
Integrates with the enhanced UML core for extended mathematical capabilities.
"""

from typing import Callable, List, Any
import math

# --- Base52 Encoding ---
BASE52_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
BASE52_MAP = {c: i+1 for i, c in enumerate(BASE52_CHARS)}

def base52_decode(token):
    """Decode a base52 token (e.g., 'A', 'z', 'AA') to integer."""
    value = 0
    for c in token:
        value = value * 52 + BASE52_MAP.get(c, 0)
    return value

def base52_encode(n):
    """
    Encode an integer n to base52 symbolic token.
    
    Args:
        n (int): The integer to encode
        
    Returns:
        str: The base52 encoded string
        
    Raises:
        ValueError: If n is less than or equal to 0
    """
    if n <= 0:
        raise ValueError("Base52 encoding requires positive integers (n > 0)")
    
    chars = []
    while n > 0:
        n, rem = divmod(n - 1, 52)
        chars.append(BASE52_CHARS[rem])
    return ''.join(reversed(chars))

# --- SI Prefixes ---
SI_PREFIXES = {
    'k': 1e3, 'M': 1e6, 'G': 1e9, 'T': 1e12,
    'm': 1e-3, 'u': 1e-6, 'n': 1e-9, 'p': 1e-12
}

def apply_si_prefix(value, prefix):
    """Apply SI prefix to a value"""
    return value * SI_PREFIXES.get(prefix, 1)

# --- Vector Operations ---
def vector_add(v1, v2):
    """Add two vectors element-wise"""
    return [a + b for a, b in zip(v1, v2)]

def vector_dot(v1, v2):
    """Compute dot product of two vectors"""
    return sum(a * b for a, b in zip(v1, v2))

def vector_cross(v1, v2):
    """Compute cross product of two 3D vectors"""
    if len(v1) != 3 or len(v2) != 3:
        raise ValueError("Cross product requires 3D vectors")
    return [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    ]

def vector_magnitude(v):
    """Compute magnitude of a vector"""
    return math.sqrt(sum(x**2 for x in v))

# --- Matrix Operations ---
def matrix_transpose(m):
    """Transpose a matrix"""
    return list(map(list, zip(*m)))

def matrix_multiply(m1, m2):
    """Multiply two matrices"""
    rows_m1, cols_m1 = len(m1), len(m1[0])
    rows_m2, cols_m2 = len(m2), len(m2[0])
    
    if cols_m1 != rows_m2:
        raise ValueError("Matrix dimensions don't match for multiplication")
    
    result = [[0 for _ in range(cols_m2)] for _ in range(rows_m1)]
    for i in range(rows_m1):
        for j in range(cols_m2):
            for k in range(cols_m1):
                result[i][j] += m1[i][k] * m2[k][j]
    return result

def matrix_determinant(m):
    """Calculate determinant of a square matrix"""
    n = len(m)
    if n != len(m[0]):
        raise ValueError("Matrix must be square")
    
    if n == 1:
        return m[0][0]
    elif n == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    else:
        # Use cofactor expansion
        det = 0
        for c in range(n):
            minor = [row[:c] + row[c+1:] for row in m[1:]]
            det += ((-1) ** c) * m[0][c] * matrix_determinant(minor)
        return det

# --- Prime and Number Theory ---
def is_prime(n):
    """Check if a number is prime"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def prime_factors(n):
    """Get prime factors of a number"""
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

def gcd(a, b):
    """Greatest common divisor using Euclidean algorithm"""
    while b:
        a, b = b, a % b
    return abs(a)

def lcm(a, b):
    """Least common multiple"""
    return abs(a * b) // gcd(a, b)

# --- Statistical Functions ---
def mean(values):
    """Calculate arithmetic mean"""
    return sum(values) / len(values) if values else 0

def median(values):
    """Calculate median"""
    if not values:
        return 0
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    if n % 2 == 0:
        return (sorted_vals[n//2 - 1] + sorted_vals[n//2]) / 2
    else:
        return sorted_vals[n//2]

def mode(values):
    """Calculate mode (most frequent value)"""
    if not values:
        return None
    freq = {}
    for val in values:
        freq[val] = freq.get(val, 0) + 1
    return max(freq, key=freq.get)

def standard_deviation(values):
    """Calculate standard deviation"""
    if len(values) < 2:
        return 0
    avg = mean(values)
    variance = sum((x - avg) ** 2 for x in values) / (len(values) - 1)
    return math.sqrt(variance)

# --- Advanced Mathematical Functions ---
def fibonacci(n):
    """Calculate nth Fibonacci number"""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def factorial(n):
    """Calculate factorial"""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def combinations(n, r):
    """Calculate binomial coefficient C(n,r)"""
    if r > n or r < 0:
        return 0
    return factorial(n) // (factorial(r) * factorial(n - r))

def permutations(n, r):
    """Calculate permutations P(n,r)"""
    if r > n or r < 0:
        return 0
    return factorial(n) // factorial(n - r)

# --- Extended UML Operators ---
def uml_root(args):
    """Root operator: /[N, X] means X^(1/N)"""
    if len(args) != 2:
        raise ValueError("Root operator expects two arguments: N (degree), X (radicand)")
    n, x = args
    if n == 0:
        raise ZeroDivisionError("Root degree cannot be zero")
    return x ** (1 / n)

def uml_log(args):
    """Logarithm operator: ?(A,B) means log base A of B"""
    if len(args) != 2:
        raise ValueError("Log operator expects two arguments: base, value")
    base, value = args
    if base <= 0 or value <= 0:
        raise ValueError("Log base and value must be positive")
    if base == 1:
        raise ValueError("Log base cannot be 1")
    return math.log(value) / math.log(base)

def uml_factorial(args):
    """Factorial operator: !A means A!"""
    if len(args) != 1:
        raise ValueError("Factorial operator expects one argument")
    n = int(args[0])
    return factorial(n)

def uml_modulo(args):
    """Modulo operator: %[A,B] means A mod B"""
    if len(args) != 2:
        raise ValueError("Modulo operator expects two arguments")
    a, b = args
    if b == 0:
        raise ZeroDivisionError("Modulo by zero")
    return a % b

def uml_gcd(args):
    """GCD operator: &[A,B] means gcd(A,B)"""
    if len(args) != 2:
        raise ValueError("GCD operator expects two arguments")
    a, b = int(args[0]), int(args[1])
    return gcd(a, b)

def uml_lcm(args):
    """LCM operator: |[A,B] means lcm(A,B)"""
    if len(args) != 2:
        raise ValueError("LCM operator expects two arguments")
    a, b = int(args[0]), int(args[1])
    return lcm(a, b)

def uml_fibonacci(args):
    """Fibonacci operator: F[N] means nth Fibonacci number"""
    if len(args) != 1:
        raise ValueError("Fibonacci operator expects one argument")
    n = int(args[0])
    return fibonacci(n)

def uml_prime_check(args):
    """Prime check operator: P[N] returns 1 if N is prime, 0 otherwise"""
    if len(args) != 1:
        raise ValueError("Prime check operator expects one argument")
    n = int(args[0])
    return 1 if is_prime(n) else 0

# Extended UML operator table
EXTENDED_UML_OPERATORS = {
    '/': uml_root,      # Root
    '?': uml_log,       # Logarithm  
    '!': uml_factorial, # Factorial
    '%': uml_modulo,    # Modulo
    '&': uml_gcd,       # GCD
    '|': uml_lcm,       # LCM
    'F': uml_fibonacci, # Fibonacci
    'P': uml_prime_check, # Prime check
}

# --- Demonstration Functions ---
def demo_symbolic_extensions():
    """Demonstrate symbolic extension capabilities"""
    print("\n🔧 Symbolic Extensions Demo")
    print("=" * 40)
    
    # Base52 encoding
    print(f"Base52: 1='A', 27='{base52_encode(27)}', 53='{base52_encode(53)}'")
    print(f"Base52 decode: 'A'={base52_decode('A')}, 'z'={base52_decode('z')}")
    
    # SI Prefixes
    print(f"SI: 5k = {apply_si_prefix(5, 'k')}, 3.2M = {apply_si_prefix(3.2, 'M')}")
    
    # Vector operations
    v1, v2 = [1, 2, 3], [4, 5, 6]
    print(f"Vectors: {v1} + {v2} = {vector_add(v1, v2)}")
    print(f"Dot product: {vector_dot(v1, v2)}")
    print(f"Cross product: {vector_cross(v1, v2)}")
    print(f"Magnitude of {v1}: {vector_magnitude(v1):.3f}")
    
    # Matrix operations
    m1 = [[1, 2], [3, 4]]
    m2 = [[5, 6], [7, 8]]
    print(f"Matrix multiply: {m1} × {m2} = {matrix_multiply(m1, m2)}")
    print(f"Determinant of {m1}: {matrix_determinant(m1)}")
    
    # Number theory
    print(f"Prime factors of 60: {prime_factors(60)}")
    print(f"GCD(48, 18) = {gcd(48, 18)}")
    print(f"LCM(12, 15) = {lcm(12, 15)}")
    
    # Statistics
    data = [1, 2, 3, 4, 5, 5, 6, 7, 8, 9]
    print(f"Stats for {data}:")
    print(f"  Mean: {mean(data):.2f}")
    print(f"  Median: {median(data)}")
    print(f"  Mode: {mode(data)}")
    print(f"  Std Dev: {standard_deviation(data):.3f}")
    
    # Advanced functions
    print(f"Fibonacci(10) = {fibonacci(10)}")
    print(f"Factorial(5) = {factorial(5)}")
    print(f"C(10,3) = {combinations(10, 3)}")
    print(f"P(10,3) = {permutations(10, 3)}")

if __name__ == "__main__":
    demo_symbolic_extensions()
