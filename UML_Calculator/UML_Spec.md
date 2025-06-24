# UML Specification

## Universal Mathematical Language - Formal Specification Document

**Author:** Travis Miner  
**Date:** June 23, 2025  
**Version:** 1.0

## 1. Introduction

This document provides a formal specification of the Universal Mathematical Language (UML), a symbolic system designed for advanced mathematical reasoning with recursive compression and identity tracking. UML serves as both a notation for expressing mathematical concepts and a computational framework with novel operations.

## 2. Notation

### 2.1 Basic Operation Syntax

| UML Symbol | Operation | Example | Description |
|------------|-----------|---------|-------------|
| `[A,B]` | Addition | `[3,4] = 7` | Addition of A and B |
| `{A,B}` | Subtraction | `{10,4} = 6` | Subtraction of B from A |
| `>A,B<` | Multiplication | `>5,6< = 30` | Multiplication of A and B |
| `<A,B>` | Division | `<10,2> = 5` | Division of A by B |
| `^[A,B]` | Exponentiation | `^[2,3] = 8` | A raised to power B |
| `/[N,X]` | Root | `/[2,9] = 3` | Nth root of X |
| `?(A,B)` | Logarithm | `?(10,100) = 2` | Log base A of B |
| `!A` | Factorial | `!5 = 120` | Factorial of A |
| `%[A,B]` | Modulo | `%[10,3] = 1` | Remainder of A divided by B |

### 2.2 Advanced Operation Syntax

| UML Symbol | Operation | Example | Description |
|------------|-----------|---------|-------------|
| `RIS(A,B)` | Recursive Integration | `RIS(4,9) = 6.5` | Recursive compression |
| `TFID(A,phase)` | Temporal Flux Identity | `TFID("x",3)` | Identity with phase |
| `collapse(expr)` | Collapse Protocol | `collapse([3,7])` | Explicit collapse |
| `identity(A)` | Identity | `identity(x)` | Identity of value |

### 2.3 Grammar

The UML language can be defined with the following grammar in EBNF notation:

```
expr ::= term | addition | subtraction | function | identity

addition ::= '[' expr (',' expr)+ ']'
subtraction ::= '{' expr (',' expr)+ '}'
multiplication ::= '>' expr (',' expr)+ '<'
division ::= '<' expr (',' expr)+ '>'
exponentiation ::= '^[' expr ',' expr ']'
root ::= '/[' expr ',' expr ']'
logarithm ::= '?(' expr ',' expr ')'
factorial ::= '!' expr
modulo ::= '%[' expr ',' expr ']'

function ::= name '(' expr_list ')'
expr_list ::= expr (',' expr)*
identity ::= IDENTIFIER | NUMBER

name ::= 'RIS' | 'TFID' | 'collapse' | 'identity'
IDENTIFIER ::= LETTER (LETTER | DIGIT)*
NUMBER ::= DIGIT+ ('.' DIGIT+)?
```

## 3. Entropy and Weights

### 3.1 Operation Entropy Weights

Each operation type in UML has an associated entropy weight that represents its relative complexity:

| Operation | Base Entropy Weight | Notes |
|-----------|---------------------|-------|
| Addition | 1.0 | Lowest entropy basic operation |
| Subtraction | 1.1 | Slightly higher than addition |
| Multiplication | 1.3 | Moderate entropy |
| Division | 1.5 | Higher entropy than multiplication |
| Exponentiation | 1.8 | High entropy operation |
| Root | 1.9 | High entropy operation |
| Logarithm | 2.0 | High entropy operation |
| Factorial | 2.2 | Highest entropy basic operation |
| Modulo | 1.4 | Moderate entropy |
| RIS | 0.8 | Tends toward stability/lower entropy |
| TFID | 0.9 | Identity anchoring lowers entropy |
| Collapse | 0.7 | Explicit collapse has low entropy |
| Identity | 0.5 | Pure identity has lowest entropy |

### 3.2 Entropy Calculation

The total entropy of an operation is calculated as:

```
total_entropy = base_weight * (0.8 + 0.4 * operand_complexity)
```

where operand complexity is:

```
operand_complexity = sum(1.0 if simple_value else 1.5 + op.entropy_weight/5 
                         for op in operands) / len(operands)
```

For interactions between operations, an interaction factor is applied:

```
interaction_factor = 0.9 if same_operation_type else 1.1
```

## 4. RIS (Recursive Integration System)

### 4.1 Definition

RIS is a binary operation that recursively compresses two values toward an optimally stable intermediate value. In its simplest implementation, RIS acts as an averaging function, but is more generally a weighted compression based on entropy.

### 4.2 Properties

- **Commutativity**: `RIS(A,B) = RIS(B,A)`
- **Fixed-point**: `RIS(A,A) = A`
- **Boundary**: `min(A,B) ≤ RIS(A,B) ≤ max(A,B)`
- **Convergence**: Repeated application of RIS converges to a stable value

### 4.3 Implementation

The base implementation of RIS for numerical values is:

```python
def eval_recursive_compress(a, b):
    return (a + b) / 2
```

For more complex types, RIS should minimize the mutual entropy between the operands.

## 5. TFID (Temporal Flux Identity Drift)

### 5.1 Definition

A TFID is a unique identifier for a symbolic entity that tracks its evolution over time through different phases and transformations.

### 5.2 Structure

A TFID consists of:

- **Identity**: A unique string identifier (UUID)
- **Phase**: An integer representing the current evolution stage
- **Timestamp**: Creation time
- **Parent Identity**: Optional reference to parent TFID
- **History**: Record of transformations
- **Entropy State**: Initial entropy value

### 5.3 Operations

- **Fork**: Create a derived identity
- **Merge**: Combine two identities
- **Advance Phase**: Progress to next evolution stage

### 5.4 Specification

```json
{
  "timestamp": "ISO-8601-timestamp",
  "identity": "uuid-string",
  "phase": integer,
  "parent_identity": "uuid-string or null",
  "creation_entropy": float,
  "history": [
    {
      "timestamp": "ISO-8601-timestamp",
      "action": "string (fork|merge|advance)",
      "reason": "string"
    }
  ]
}
```

## 6. Collapse Protocol

### 6.1 Definition

The Collapse Protocol defines how symbolic expressions are evaluated and simplified based on entropy minimization principles.

### 6.2 Path Selection

The protocol selects from possible evaluation paths based on:

1. **Deterministic Mode**: Always choose path with lowest total entropy
2. **Non-deterministic Mode**: Choose path with probability weighted by inverse entropy

### 6.3 Entropy Bias

Entropy bias (0-1) controls how strongly the selection favors low-entropy paths:

```
bias_factor = 1.0 + entropy_bias * (paths_count - path_rank) / paths_count
```

### 6.4 Path Generation

Multiple valid collapse paths are generated for complex expressions by:

1. Analyzing the expression tree
2. Identifying possible operation sequences
3. Calculating entropy for each sequence
4. Selecting optimal or probabilistically weighted path

## 7. Memory System

### 7.1 Structure

The memory system consists of:

1. **TFID Store**: Repository of all TFIDs
2. **Operations Store**: Record of all operations
3. **Collapses Store**: History of expression collapses

### 7.2 Formats

#### TFID Record:
```json
{
  "identity": "uuid-string",
  "tfid": {
    "timestamp": "ISO-8601-timestamp",
    "identity": "uuid-string",
    "phase": integer,
    "parent_identity": "uuid-string or null",
    "creation_entropy": float,
    "history": []
  }
}
```

#### Operation Record:
```json
{
  "operation_id": "uuid-string",
  "timestamp": "ISO-8601-timestamp",
  "operation": {
    "type": "string",
    "operands": ["string"],
    "entropy_weight": float
  },
  "result_tfid": "uuid-string"
}
```

#### Collapse Record:
```json
{
  "collapse_id": "uuid-string",
  "timestamp": "ISO-8601-timestamp",
  "source_expression": "string",
  "collapse_path": [
    {
      "operation": "string",
      "result": "string",
      "tfid": "uuid-string",
      "entropy_delta": float
    }
  ],
  "result": "string",
  "result_tfid": "uuid-string"
}
```

## 8. Primitive Operations

The UML system is based on a foundational set of primitive operations:

```python
primitives = {
    'addition': lambda a, b: a + b,
    'subtraction': lambda a, b: a - b,
    'multiplication': lambda a, b: a * b,
    'division': lambda a, b: a / b if b != 0 else "!0",
    'exponentiation': lambda a, n: a ** n,
    'root': lambda a, n: a ** (1/n) if n != 0 else "!0",
    'logarithm': lambda base, x: math.log(x, base) if x > 0 and base > 0 and base != 1 else "!0",
    'factorial': lambda n: math.gamma(n+1) if n >= 0 else "!0",
    'modulo': lambda a, b: a % b if b != 0 else "!0",
    'identity': lambda x: x,
    'ris': eval_recursive_compress
}
```

## 9. Expression Trees

Expression trees provide visualizations of symbolic operations and their collapse pathways.

### 9.1 Node Structure

```
Node:
  - Type: operation | value
  - If operation:
    - op_type: SymbolicOperationType
    - entropy_weight: float
    - operands: [Node]
    - metadata: Dict
  - If value:
    - value: string representation
```

### 9.2 Collapse Steps

```
CollapseStep:
  - operation: SymbolicOperation
  - result: Any
  - entropy_delta: float
  - timestamp: ISO-8601-timestamp
```

## 10. Examples

### 10.1 Basic UML Operations

```
[3,4] = 7
>5,6< = 30
<21,3> = 7
^[2,4] = 16
/[2,9] = 3
```

### 10.2 RIS Examples

```
RIS(4, 9) = 6.5
RIS(10, 20) = 15
RIS(2, 8) = 5
RIS(-3, 7) = 2
RIS(3.5, 7.5) = 5.5
```

### 10.3 TFID Examples

```
TFID("magic_square", 0) = "magic_square" with phase 0
TFID("tesseract", 2) = "tesseract" with phase 2
```

### 10.4 Collapse Examples

```
collapse([3,7]) = 10 with visualization
```

## 11. Conclusion

This specification defines the UML symbolic system's notation, operations, and behaviors. Implementations should adhere to these guidelines to ensure consistent behavior and interoperability.

---

© 2025 Travis Miner. All Rights Reserved.
