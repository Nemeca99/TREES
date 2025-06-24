# UML Symbolic Engine

## Universal Mathematical Language - Symbolic Reasoning System

**Author:** Travis Miner  
**Date:** June 23, 2025  
**Version:** 1.0

## Introduction

The UML Symbolic Engine is a powerful computational framework that goes beyond traditional mathematics by implementing symbolic reasoning with recursive integration and temporal identity tracking. This system represents a fundamentally different approach to mathematical computation through its novel concepts:

- **RIS (Recursive Integration System)**: A system for compressing mathematical expressions through entropy-guided collapse
- **TFID (Temporal Flux Identity Drift)**: A framework for tracking symbolic identities across time and transformations
- **Collapse Protocol**: Decision-making process for operations based on entropy minimization principles

## Key Features

- **Universal Mathematical Language (UML)**: A symbolic notation for expressing mathematical concepts
- **Symbolic Operations Suite**: Addition, subtraction, multiplication, division, exponentiation, roots, logarithms, factorials
- **Advanced Operations**: RIS, TFID, identity operations, collapse protocols
- **Memory System**: Persistent storage for symbolic operations, TFIDs, and collapse history
- **Visualization**: CLI visualization of expression trees and collapse pathways
- **Interactive REPL**: Command-line interface for exploring the symbolic system
- **Deterministic & Non-deterministic Modes**: Control collapse path selection based on entropy

## UML Notation

| UML Symbol | Operation | Example | Description |
|------------|-----------|---------|-------------|
| `[A,B]` | Addition | `[3,4] = 7` | Addition of A and B |
| `{A,B}` | Subtraction | `{10,4} = 6` | Subtraction of B from A |
| `>A,B<` | Multiplication | `>5,6< = 30` | Multiplication of A and B |
| `<A,B>` | Division | `<10,2> = 5` | Division of A by B |
| `^[A]` | Exponentiation | `^[2,3] = 8` | A raised to power B |
| `/[N,X]` | Root | `/[2,9] = 3` | Nth root of X |
| `?(A,B)` | Logarithm | `?(10,100) = 2` | Log base A of B |
| `!A` | Factorial | `!5 = 120` | Factorial of A |
| `%[A,B]` | Modulo | `%[10,3] = 1` | Remainder of A divided by B |
| `RIS(A,B)` | Recursive Integration | `RIS(4,9) = 6.5` | Recursive compression |
| `TFID(A,phase)` | Temporal Flux Identity | `TFID("x",3)` | Identity with phase |
| `collapse(expr)` | Collapse Protocol | `collapse([3,7])` | Explicit collapse |

## Getting Started

### Requirements

- Python 3.8+
- No external dependencies for the core symbolic engine

### Running the Engine

1. **Run the Launcher Script:**
   ```
   run_symbolic_engine.bat
   ```

2. **Run Demo Directly:**
   ```
   python UML_Core\symbolic_engine_demo.py
   ```

3. **Start REPL Directly:**
   ```python
   from UML_Core.symbolic_engine import SymbolicEngine
   engine = SymbolicEngine()
   engine.run_interactive_repl()
   ```

### REPL Commands

The REPL provides a direct interface to the symbolic engine:

- **Expressions:** Enter UML expressions to evaluate them
  ```
  UML> [3,7]
  ```

- **Special Functions:**
  ```
  UML> RIS(4, 9)                 # Recursive Integration
  UML> collapse([3,7])           # Visualize collapse steps
  UML> TFID("magic_square", 3)   # Create temporal flux identity
  UML> trace_TFID(id)            # Trace TFID history
  UML> memory_stats              # Show memory statistics
  UML> clear_memory              # Clear all memory
  ```

## Concepts

### Recursive Integration System (RIS)

RIS is a fundamental operation in UML that recursively compresses two values toward an "optimally compressed" result. In the simplest form, RIS acts as an averaging function, but its true power emerges in more complex scenarios where multiple possible compression paths exist.

```
RIS(4, 9) = 6.5
RIS(10, 20) = 15
RIS(-3, 7) = 2
```

### Temporal Flux Identity Drift (TFID)

TFID provides a framework for tracking symbolic identities through transformations over time. Each TFID has:

- A unique identifier
- A phase (integer representing evolution stage)
- A timestamp
- Optional parent relationship
- A history of changes

TFIDs enable backtracking through symbolic transformations and understanding the lineage of mathematical entities.

### Collapse Protocol

The Collapse Protocol guides the transformation of symbolic expressions through entropy-weighted decision paths. It can operate in:

- **Deterministic Mode:** Always selecting the lowest entropy path
- **Non-deterministic Mode:** Allowing some randomness weighted by entropy bias

This enables the system to find optimal simplification pathways through complex expression spaces.

## Architecture

The system consists of the following key components:

1. **SymbolicEngine:** Main controller for operations and user interaction
2. **SymbolicOperation:** Representation of operations with entropy weights
3. **TFID:** Identity tracking system across time and transformations
4. **MemoryStore:** Persistent storage for symbols, operations, and history
5. **CollapseProtocol:** Decision-making system for expression reduction
6. **ExpressionTree:** Visualization framework for symbolic operations

## License

Copyright © 2025 Travis Miner. All rights reserved.

---

*"Mathematics is the language with which God has written the universe."* - Galileo Galilei
