"""
UML Symbolic Engine - Core implementation of the Universal Mathematical Language
symbolic reasoning system with RIS (Recursive Integration System) and TFID (Temporal
Flux Identity Drift) capabilities.

Author: Travis Miner
Date: June 23, 2025
"""

import json
import os
import time
import uuid
import math
import logging
from enum import Enum, auto
from typing import Dict, List, Union, Tuple, Optional, Any, Callable
from datetime import datetime
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("UMLSymbolicEngine")

# Import existing UML core functions if available
try:
    from uml_core import parse_uml, eval_uml, eval_recursive_compress

    logger.info("Successfully imported UML core functions")
except ImportError:
    logger.warning("UML core functions not found, using placeholder implementations")

    # Placeholder implementations for standalone testing
    def parse_uml(expr):
        return expr

    def eval_uml(expr):
        return expr

    def eval_recursive_compress(a, b):
        return (a + b) / 2


class SymbolicOperationType(Enum):
    """Enumeration of symbolic operation types in UML."""

    ADDITION = auto()  # [A,B]
    SUBTRACTION = auto()  # {A,B}
    MULTIPLICATION = auto()  # >A,B<
    DIVISION = auto()  # <A,B>
    EXPONENTIATION = auto()  # ^[A]
    ROOT = auto()  # /[N,X]
    LOGARITHM = auto()  # ?(A,B)
    FACTORIAL = auto()  # !A
    MODULO = auto()  # %[A,B]
    RIS = auto()  # RIS(A,B)
    TFID = auto()  # TFID(A,phase)
    COLLAPSE = auto()  # collapse(expr)
    IDENTITY = auto()  # identity(A)

    @classmethod
    def from_symbol(cls, symbol: str) -> "SymbolicOperationType":
        """Convert UML symbol to operation type."""
        symbol_map = {
            "[": cls.ADDITION,
            "{": cls.SUBTRACTION,
            ">": cls.MULTIPLICATION,
            "<": cls.DIVISION,
            "^": cls.EXPONENTIATION,
            "/": cls.ROOT,
            "?": cls.LOGARITHM,
            "!": cls.FACTORIAL,
            "%": cls.MODULO,
            "RIS": cls.RIS,
            "TFID": cls.TFID,
            "collapse": cls.COLLAPSE,
            "identity": cls.IDENTITY,
        }
        return symbol_map.get(symbol, None)


class SymbolicOperation:
    """Represents a symbolic operation in UML with intent and compression logic."""

    def __init__(
        self,
        op_type: SymbolicOperationType,
        operands: List[Union[str, int, float, "SymbolicOperation"]],
        metadata: Dict[str, Any] = None,
    ):
        self.op_type = op_type
        self.operands = operands
        self.metadata = metadata or {}
        self.entropy_weight = self._calculate_entropy_weight()
        self.tfid = None  # Will be assigned when operation is executed

    def _calculate_entropy_weight(self) -> float:
        """Calculate entropy weight for this operation."""
        # Base weights for different operation types
        base_weights = {
            SymbolicOperationType.ADDITION: 1.0,
            SymbolicOperationType.SUBTRACTION: 1.1,
            SymbolicOperationType.MULTIPLICATION: 1.3,
            SymbolicOperationType.DIVISION: 1.5,
            SymbolicOperationType.EXPONENTIATION: 1.8,
            SymbolicOperationType.ROOT: 1.9,
            SymbolicOperationType.LOGARITHM: 2.0,
            SymbolicOperationType.FACTORIAL: 2.2,
            SymbolicOperationType.MODULO: 1.4,
            SymbolicOperationType.RIS: 0.8,  # RIS tends toward stability/lower entropy
            SymbolicOperationType.TFID: 0.9,
            SymbolicOperationType.COLLAPSE: 0.7,
            SymbolicOperationType.IDENTITY: 0.5,  # Identity operations have lowest entropy
        }

        # Start with base weight for operation type
        weight = base_weights.get(self.op_type, 1.0)

        # Adjust for operand complexity
        operand_complexity = sum(
            1.0 if isinstance(op, (int, float, str)) else 1.5 + op.entropy_weight / 5
            for op in self.operands
        )

        # Normalize by number of operands
        if self.operands:
            operand_complexity /= len(self.operands)

        # Final weight is a combination of operation type and operand complexity
        return weight * (0.8 + 0.4 * operand_complexity)

    def __str__(self) -> str:
        """String representation of the symbolic operation."""
        if self.op_type == SymbolicOperationType.ADDITION:
            return f"[{','.join(str(op) for op in self.operands)}]"
        elif self.op_type == SymbolicOperationType.SUBTRACTION:
            return f"{{{','.join(str(op) for op in self.operands)}}}"
        elif self.op_type == SymbolicOperationType.MULTIPLICATION:
            return f">{','.join(str(op) for op in self.operands)}<"
        elif self.op_type == SymbolicOperationType.DIVISION:
            return f"<{','.join(str(op) for op in self.operands)}>"
        elif self.op_type == SymbolicOperationType.EXPONENTIATION:
            return f"^[{','.join(str(op) for op in self.operands)}]"
        elif self.op_type == SymbolicOperationType.ROOT:
            return f"/[{','.join(str(op) for op in self.operands)}]"
        elif self.op_type == SymbolicOperationType.LOGARITHM:
            return f"?({','.join(str(op) for op in self.operands)})"
        elif self.op_type == SymbolicOperationType.FACTORIAL:
            return f"!{self.operands[0]}" if self.operands else "!?"
        elif self.op_type == SymbolicOperationType.MODULO:
            return f"%[{','.join(str(op) for op in self.operands)}]"
        elif self.op_type == SymbolicOperationType.RIS:
            return f"RIS({','.join(str(op) for op in self.operands)})"
        elif self.op_type == SymbolicOperationType.TFID:
            return f"TFID({','.join(str(op) for op in self.operands)})"
        elif self.op_type == SymbolicOperationType.COLLAPSE:
            return f"collapse({','.join(str(op) for op in self.operands)})"
        elif self.op_type == SymbolicOperationType.IDENTITY:
            return f"identity({self.operands[0]})" if self.operands else "identity(?)"
        else:
            return f"{self.op_type}({','.join(str(op) for op in self.operands)})"


class TFID:
    """Temporal Flux Identity Drift - Tracks symbolic identity across time and phase."""

    def __init__(
        self, identity: str = None, phase: int = 0, parent_tfid: "TFID" = None
    ):
        """
        Initialize a new TFID.

        Args:
            identity: Unique identifier for this entity, or None to auto-generate
            phase: Current phase of this identity in its lifecycle
            parent_tfid: Parent TFID if this is derived from another identity
        """
        self.timestamp = datetime.now().isoformat()
        self.identity = identity or str(uuid.uuid4())
        self.phase = phase
        self.parent_identity = parent_tfid.identity if parent_tfid else None
        self.creation_entropy = random.random()  # Simulated initial entropy state
        self.history = []

    def advance_phase(self, reason: str = "Natural progression") -> None:
        """Advance this identity to the next phase."""
        self.history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "old_phase": self.phase,
                "new_phase": self.phase + 1,
                "reason": reason,
            }
        )
        self.phase += 1

    def fork(self, reason: str = "Identity fork") -> "TFID":
        """Create a forked version of this identity."""
        forked = TFID(phase=self.phase, parent_tfid=self)
        self.history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "action": "fork",
                "child_identity": forked.identity,
                "reason": reason,
            }
        )
        return forked

    def merge(self, other_tfid: "TFID", reason: str = "Identity merger") -> "TFID":
        """Merge this identity with another, creating a new composite identity."""
        # Create new identity with combined phase (avg of both rounded up)
        merged_phase = math.ceil((self.phase + other_tfid.phase) / 2)
        merged = TFID(phase=merged_phase)

        # Record merger in both parent identities
        merge_record = {
            "timestamp": datetime.now().isoformat(),
            "action": "merge",
            "merged_with": other_tfid.identity,
            "resulting_identity": merged.identity,
            "reason": reason,
        }
        self.history.append(merge_record)

        other_record = merge_record.copy()
        other_record["merged_with"] = self.identity
        other_tfid.history.append(other_record)

        return merged

    def to_dict(self) -> Dict[str, Any]:
        """Convert TFID to dictionary for storage."""
        return {
            "timestamp": self.timestamp,
            "identity": self.identity,
            "phase": self.phase,
            "parent_identity": self.parent_identity,
            "creation_entropy": self.creation_entropy,
            "history": self.history,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TFID":
        """Recreate TFID from dictionary."""
        tfid = cls.__new__(cls)
        tfid.timestamp = data["timestamp"]
        tfid.identity = data["identity"]
        tfid.phase = data["phase"]
        tfid.parent_identity = data["parent_identity"]
        tfid.creation_entropy = data["creation_entropy"]
        tfid.history = data["history"]
        return tfid

    def __str__(self) -> str:
        """String representation of TFID."""
        parent_info = (
            f" (from {self.parent_identity[:8]})" if self.parent_identity else ""
        )
        return f"TFID:{self.identity[:8]}.p{self.phase}{parent_info}"


class MemoryStore:
    """Persistent storage for symbolic operations, TFIDs and RIS events."""

    def __init__(self, store_path: str = None):
        """
        Initialize the memory store.

        Args:
            store_path: Directory to store memory files. Defaults to UML_Memory
                       in the current directory.
        """
        self.store_path = store_path or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "UML_Memory"
        )
        os.makedirs(self.store_path, exist_ok=True)

        self.tfid_path = os.path.join(self.store_path, "tfids.json")
        self.operations_path = os.path.join(self.store_path, "operations.json")
        self.collapse_path = os.path.join(self.store_path, "collapses.json")

        self.tfids = self._load_json(self.tfid_path, {})
        self.operations = self._load_json(self.operations_path, {})
        self.collapses = self._load_json(self.collapse_path, {})

        logger.info(f"Memory store initialized at {self.store_path}")

    def _load_json(self, path: str, default: Any) -> Any:
        """Load JSON from file or return default if file doesn't exist."""
        try:
            with open(path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return default

    def _save_json(self, data: Any, path: str) -> None:
        """Save data as JSON to file."""
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def save_tfid(self, tfid: TFID) -> None:
        """Save a TFID to the memory store."""
        self.tfids[tfid.identity] = tfid.to_dict()
        self._save_json(self.tfids, self.tfid_path)

    def get_tfid(self, identity: str) -> Optional[TFID]:
        """Retrieve a TFID by identity."""
        if identity in self.tfids:
            return TFID.from_dict(self.tfids[identity])
        return None

    def save_operation(
        self, op_id: str, operation: Dict[str, Any], result_tfid: str
    ) -> None:
        """Save an operation to the memory store."""
        self.operations[op_id] = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "result_tfid": result_tfid,
        }
        self._save_json(self.operations, self.operations_path)

    def save_collapse(
        self,
        collapse_id: str,
        source_expr: str,
        collapse_path: List[Dict[str, Any]],
        result: Any,
        result_tfid: str,
    ) -> None:
        """Save a collapse sequence to the memory store."""
        self.collapses[collapse_id] = {
            "timestamp": datetime.now().isoformat(),
            "source_expression": source_expr,
            "collapse_path": collapse_path,
            "result": result,
            "result_tfid": result_tfid,
        }
        self._save_json(self.collapses, self.collapse_path)

    def get_collapse_by_expression(self, expr: str) -> List[Dict[str, Any]]:
        """Find all collapses for a given expression."""
        results = []
        for collapse_id, collapse_data in self.collapses.items():
            if collapse_data["source_expression"] == expr:
                results.append({"collapse_id": collapse_id, **collapse_data})
        return results

    def get_operations_by_tfid(self, tfid_identity: str) -> List[Dict[str, Any]]:
        """Find all operations associated with a given TFID."""
        results = []
        for op_id, op_data in self.operations.items():
            if op_data["result_tfid"] == tfid_identity:
                results.append({"operation_id": op_id, **op_data})
        return results


class ExpressionTree:
    """Tree representation of a UML symbolic expression for visualization."""

    def __init__(self, root_op: Union[SymbolicOperation, str, int, float]):
        """Initialize an expression tree with a root operation or value."""
        self.root = root_op
        self.collapse_steps = []

    def add_collapse_step(
        self, operation: SymbolicOperation, result: Any, entropy_delta: float
    ) -> None:
        """Add a collapse step to the visualization history."""
        self.collapse_steps.append(
            {
                "operation": operation,
                "result": result,
                "entropy_delta": entropy_delta,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def visualize_cli(self) -> None:
        """Visualize the expression tree and collapse steps in the terminal."""
        print("\n=== UML Expression Tree Visualization ===\n")
        print("Original Expression:")
        self._print_tree(self.root)

        print("\nCollapse Steps:")
        for i, step in enumerate(self.collapse_steps):
            print(f"Step {i+1}: {step['operation']} -> {step['result']}")
            print(f"  Entropy Change: {step['entropy_delta']:.4f}")

    def _print_tree(self, node, depth=0):
        """Recursively print the expression tree."""
        indent = "  " * depth
        if isinstance(node, SymbolicOperation):
            print(f"{indent}{node.op_type.name} (w={node.entropy_weight:.2f}):")
            for op in node.operands:
                self._print_tree(op, depth + 1)
        else:
            print(f"{indent}VALUE: {node}")

    def get_visualization_data(self) -> Dict[str, Any]:
        """Get visualization data for external renderers."""
        return {
            "root": self._serialize_node(self.root),
            "collapse_steps": self.collapse_steps,
        }

    def _serialize_node(self, node: Union[SymbolicOperation, Any]) -> Dict[str, Any]:
        """Convert a node to a serializable format for visualization."""
        if isinstance(node, SymbolicOperation):
            return {
                "type": "operation",
                "op_type": node.op_type.name,
                "entropy_weight": node.entropy_weight,
                "operands": [self._serialize_node(op) for op in node.operands],
                "metadata": node.metadata,
            }
        else:
            return {"type": "value", "value": str(node)}


class CollapseProtocol:
    """Defines the protocol for collapsing symbolic expressions in UML."""

    def __init__(self, deterministic: bool = False, entropy_bias: float = 0.8):
        """
        Initialize the collapse protocol.

        Args:
            deterministic: If True, always choose the lowest entropy path.
                          If False, allow some randomness based on entropy_bias.
            entropy_bias: How strongly to bias toward lower entropy paths (0-1).
        """
        self.deterministic = deterministic
        self.entropy_bias = max(0.0, min(1.0, entropy_bias))

    def calculate_path_entropy(self, operations: List[SymbolicOperation]) -> float:
        """Calculate the entropy of a potential collapse path."""
        # Base entropy is sum of operation entropies
        base_entropy = sum(op.entropy_weight for op in operations)

        # Adjust for interaction effects between operations
        interaction_factor = 1.0
        for i in range(len(operations) - 1):
            # Operations of same type have lower interaction entropy
            if operations[i].op_type == operations[i + 1].op_type:
                interaction_factor *= 0.9
            else:
                interaction_factor *= 1.1

        return base_entropy * interaction_factor

    def select_collapse_path(
        self, paths: List[List[SymbolicOperation]]
    ) -> Tuple[int, float]:
        """
        Select a collapse path from available options.

        Args:
            paths: List of potential collapse paths (each a list of operations)

        Returns:
            Tuple of (selected path index, path entropy)
        """
        # Calculate entropy for each path
        entropies = [self.calculate_path_entropy(path) for path in paths]

        if self.deterministic:
            # Select path with lowest entropy
            selected_idx = entropies.index(min(entropies))
        else:
            # Calculate probability weights based on inverse entropy
            inverse_entropies = [1.0 / e for e in entropies]
            total = sum(inverse_entropies)
            weights = [e / total for e in inverse_entropies]

            # Adjust weights based on entropy bias
            if self.entropy_bias > 0:
                # Sort paths by entropy (ascending)
                sorted_indices = sorted(
                    range(len(entropies)), key=lambda i: entropies[i]
                )

                # Apply bias toward lower entropy paths
                for i, idx in enumerate(sorted_indices):
                    bias_factor = 1.0 + self.entropy_bias * (len(paths) - i) / len(
                        paths
                    )
                    weights[idx] *= bias_factor

                # Renormalize weights
                total = sum(weights)
                weights = [w / total for w in weights]

            # Select based on weighted probabilities
            selected_idx = random.choices(range(len(paths)), weights=weights)[0]

        return selected_idx, entropies[selected_idx]


class SymbolicEngine:
    """Main engine for UML symbolic operations, RIS, and TFID functionality."""

    def __init__(
        self,
        memory_path: str = None,
        deterministic_collapse: bool = False,
        entropy_bias: float = 0.8,
    ):
        """
        Initialize the symbolic engine.

        Args:
            memory_path: Path for storing symbolic memory
            deterministic_collapse: Whether collapse protocol is deterministic
            entropy_bias: Bias toward lower entropy paths in non-deterministic mode
        """
        self.memory = MemoryStore(memory_path)
        self.collapse_protocol = CollapseProtocol(
            deterministic=deterministic_collapse, entropy_bias=entropy_bias
        )

        # Set of primitive operations that form the foundation of the system
        self.primitives = {
            "addition": lambda a, b: a + b,
            "subtraction": lambda a, b: a - b,
            "multiplication": lambda a, b: a * b,
            "division": lambda a, b: a / b if b != 0 else "!0",  # Division by zero
            "exponentiation": lambda a, n: a**n,
            "root": lambda a, n: a ** (1 / n) if n != 0 else "!0",
            "logarithm": lambda base, x: (
                math.log(x, base) if x > 0 and base > 0 and base != 1 else "!0"
            ),
            "factorial": lambda n: math.gamma(n + 1) if n >= 0 else "!0",
            "modulo": lambda a, b: a % b if b != 0 else "!0",
            "identity": lambda x: x,
            "ris": eval_recursive_compress,
        }

    def create_operation(
        self,
        op_type: Union[str, SymbolicOperationType],
        operands: List[Any],
        metadata: Dict[str, Any] = None,
    ) -> SymbolicOperation:
        """Create a new symbolic operation."""
        # Convert string type to enum if needed
        if isinstance(op_type, str):
            if op_type.upper() in SymbolicOperationType.__members__:
                op_type = SymbolicOperationType[op_type.upper()]
            else:
                op_type = SymbolicOperationType.from_symbol(op_type)

        return SymbolicOperation(op_type, operands, metadata)

    def parse_expression(self, expr_str: str) -> SymbolicOperation:
        """Parse a UML expression string into a SymbolicOperation tree."""
        # Simple recursive descent parser for UML expressions
        # For now, this is a placeholder that would need to be expanded
        # to handle the full UML grammar

        expr_str = expr_str.strip()

        # Handle RIS function call
        if expr_str.startswith("RIS(") and expr_str.endswith(")"):
            args = expr_str[4:-1].split(",")
            if len(args) >= 2:
                operands = [self.parse_expression(arg.strip()) for arg in args]
                return SymbolicOperation(SymbolicOperationType.RIS, operands)

        # Handle TFID function call
        if expr_str.startswith("TFID(") and expr_str.endswith(")"):
            args = expr_str[5:-1].split(",")
            if len(args) >= 1:
                operands = [self.parse_expression(arg.strip()) for arg in args]
                return SymbolicOperation(SymbolicOperationType.TFID, operands)

        # Handle collapse function call
        if expr_str.startswith("collapse(") and expr_str.endswith(")"):
            inner_expr = expr_str[9:-1].strip()
            return SymbolicOperation(
                SymbolicOperationType.COLLAPSE, [self.parse_expression(inner_expr)]
            )

        # Handle literal values
        try:
            # Try to parse as number
            return float(expr_str)
        except ValueError:
            # If not a number or recognized function, treat as identity
            if not any(c in expr_str for c in "[]{}()<>,^!%?"):
                return SymbolicOperation(SymbolicOperationType.IDENTITY, [expr_str])

        # For now, default to using existing UML parser for other expressions
        # This would be expanded in a full implementation
        return parse_uml(expr_str)

    def execute_operation(self, operation: SymbolicOperation) -> Tuple[Any, TFID]:
        """
        Execute a symbolic operation and assign it a TFID.

        Args:
            operation: The symbolic operation to execute

        Returns:
            Tuple of (result, tfid of result)
        """
        # Create a TFID for this operation
        op_tfid = TFID()

        # Handle different operation types
        if operation.op_type == SymbolicOperationType.ADDITION:
            evaluated_operands = []
            for op in operation.operands[:2]:
                if isinstance(op, SymbolicOperation):
                    val, _ = self.execute_operation(op)
                    evaluated_operands.append(val)
                else:
                    evaluated_operands.append(op)            # Ensure operands are numeric
            try:
                numeric_operands = [float(val) for val in evaluated_operands]
            except Exception:
                numeric_operands = evaluated_operands
            addition_func = self.primitives.get("addition")
            if callable(addition_func):
                result = addition_func(*numeric_operands)
            else:
                raise TypeError("Primitive 'addition' is not callable.")
                
        elif operation.op_type == SymbolicOperationType.SUBTRACTION:
            evaluated_operands = []
            for op in operation.operands[:2]:
                if isinstance(op, SymbolicOperation):
                    val, _ = self.execute_operation(op)
                    evaluated_operands.append(val)
                else:
                    evaluated_operands.append(op)
            # Ensure operands are numeric
            try:
                numeric_operands = [float(val) for val in evaluated_operands]
            except Exception:
                numeric_operands = evaluated_operands
            subtraction_func = self.primitives.get("subtraction")
            if callable(subtraction_func):
                result = subtraction_func(*numeric_operands)
            else:
                raise TypeError("Primitive 'subtraction' is not callable.")
                
        elif operation.op_type == SymbolicOperationType.MULTIPLICATION:
            evaluated_operands = []
            for op in operation.operands[:2]:
                if isinstance(op, SymbolicOperation):
                    val, _ = self.execute_operation(op)
                    evaluated_operands.append(val)
                else:
                    evaluated_operands.append(op)
            # Ensure operands are numeric
            try:
                numeric_operands = [float(val) for val in evaluated_operands]
            except Exception:
                numeric_operands = evaluated_operands
            multiplication_func = self.primitives.get("multiplication")
            if callable(multiplication_func):
                result = multiplication_func(*numeric_operands)
            else:
                raise TypeError("Primitive 'multiplication' is not callable.")
                
        elif operation.op_type == SymbolicOperationType.DIVISION:
            evaluated_operands = []
            for op in operation.operands[:2]:
                if isinstance(op, SymbolicOperation):
                    val, _ = self.execute_operation(op)
                    evaluated_operands.append(val)
                else:
                    evaluated_operands.append(op)
            # Ensure operands are numeric
            try:
                numeric_operands = [float(val) for val in evaluated_operands]
            except Exception:
                numeric_operands = evaluated_operands
            division_func = self.primitives.get("division")
            if callable(division_func):
                result = division_func(*numeric_operands)
            else:
                raise TypeError("Primitive 'division' is not callable.")
                
        elif operation.op_type == SymbolicOperationType.EXPONENTIATION:
            evaluated_operands = []
            for op in operation.operands[:2]:
                if isinstance(op, SymbolicOperation):
                    val, _ = self.execute_operation(op)
                    evaluated_operands.append(val)
                else:
                    evaluated_operands.append(op)
            # Ensure operands are numeric
            try:
                numeric_operands = [float(val) for val in evaluated_operands]
            except Exception:
                numeric_operands = evaluated_operands
            exponentiation_func = self.primitives.get("exponentiation")
            if callable(exponentiation_func):
                result = exponentiation_func(*numeric_operands)
            else:
                raise TypeError("Primitive 'exponentiation' is not callable.")
                
        elif operation.op_type == SymbolicOperationType.ROOT:
            evaluated_operands = []
            for op in operation.operands[:2]:
                if isinstance(op, SymbolicOperation):
                    val, _ = self.execute_operation(op)
                    evaluated_operands.append(val)
                else:
                    evaluated_operands.append(op)
            # Ensure operands are numeric
            try:
                numeric_operands = [float(val) for val in evaluated_operands]
            except Exception:
                numeric_operands = evaluated_operands
            root_func = self.primitives.get("root")
            if callable(root_func):
                result = root_func(*numeric_operands)
            else:
                raise TypeError("Primitive 'root' is not callable.")
                
        elif operation.op_type == SymbolicOperationType.LOGARITHM:
            evaluated_operands = []
            for op in operation.operands[:2]:
                if isinstance(op, SymbolicOperation):
                    val, _ = self.execute_operation(op)
                    evaluated_operands.append(val)
                else:
                    evaluated_operands.append(op)
            # Ensure operands are numeric
            try:
                numeric_operands = [float(val) for val in evaluated_operands]
            except Exception:
                numeric_operands = evaluated_operands
            logarithm_func = self.primitives.get("logarithm")
            if callable(logarithm_func):
                result = logarithm_func(*numeric_operands)
            else:
                raise TypeError("Primitive 'logarithm' is not callable.")
                
        elif operation.op_type == SymbolicOperationType.FACTORIAL:
            op_val = (
                self.execute_operation(operation.operands[0])[0]
                if isinstance(operation.operands[0], SymbolicOperation)
                else operation.operands[0]
            )
            try:
                numeric_val = float(op_val)
            except Exception:
                numeric_val = op_val
                
            factorial_func = self.primitives.get("factorial")
            if callable(factorial_func):
                result = factorial_func(numeric_val)
            else:
                raise TypeError("Primitive 'factorial' is not callable.")
                
        elif operation.op_type == SymbolicOperationType.MODULO:
            evaluated_operands = []
            for op in operation.operands[:2]:
                if isinstance(op, SymbolicOperation):
                    val, _ = self.execute_operation(op)
                    evaluated_operands.append(val)
                else:
                    evaluated_operands.append(op)
            # Ensure operands are numeric
            try:
                numeric_operands = [float(val) for val in evaluated_operands]
            except Exception:
                numeric_operands = evaluated_operands
            modulo_func = self.primitives.get("modulo")
            if callable(modulo_func):
                result = modulo_func(*numeric_operands)
            else:
                raise TypeError("Primitive 'modulo' is not callable.")
                
        elif operation.op_type == SymbolicOperationType.RIS:
            # RIS operation executes recursive compression
            ops = []
            for op in operation.operands:
                if isinstance(op, SymbolicOperation):
                    val, _ = self.execute_operation(op)
                    ops.append(val)
                else:
                    ops.append(op)
            
            # Ensure operands are numeric
            try:
                numeric_ops = [float(val) for val in ops]
            except Exception:
                numeric_ops = ops
                
            ris_func = self.primitives.get("ris")
            if callable(ris_func) and len(numeric_ops) >= 2:
                result = ris_func(numeric_ops[0], numeric_ops[1])
            elif len(numeric_ops) > 0:
                result = numeric_ops[0]
            else:
                raise ValueError("RIS operation requires at least one operand")

        elif operation.op_type == SymbolicOperationType.TFID:
            # TFID operation returns an identity with optional phase
            identity = str(
                self.execute_operation(operation.operands[0])[0]
                if isinstance(operation.operands[0], SymbolicOperation)
                else operation.operands[0]
            )

            phase = 0
            if len(operation.operands) > 1:
                phase = int(
                    self.execute_operation(operation.operands[1])[0]
                    if isinstance(operation.operands[1], SymbolicOperation)
                    else operation.operands[1]
                )

            # Create a TFID for this identity and return it
            op_tfid = TFID(identity=identity, phase=phase)
            result = identity

        elif operation.op_type == SymbolicOperationType.COLLAPSE:
            # Collapse operation resolves an expression through the collapse protocol
            inner_result, inner_tfid = (
                self.execute_operation(operation.operands[0])
                if isinstance(operation.operands[0], SymbolicOperation)
                else (operation.operands[0], TFID())
            )

            # The collapse operation itself gets a new TFID derived from the inner one
            op_tfid = inner_tfid.fork("Collapse operation")
            result = inner_result

        elif operation.op_type == SymbolicOperationType.IDENTITY:
            # Identity operation just returns its argument with a new TFID
            identity_val = (
                self.execute_operation(operation.operands[0])[0]
                if isinstance(operation.operands[0], SymbolicOperation)
                else operation.operands[0]
            )
            result = identity_val

        else:
            # Unrecognized operation type
            logger.warning(f"Unrecognized operation type: {operation.op_type}")
            result = None

        # Save operation and TFID to memory store
        op_id = str(uuid.uuid4())
        self.memory.save_tfid(op_tfid)
        self.memory.save_operation(
            op_id,
            {
                "type": operation.op_type.name,
                "operands": [
                    (
                        str(op)
                        if not isinstance(op, SymbolicOperation)
                        else op.op_type.name
                    )
                    for op in operation.operands
                ],
                "entropy_weight": operation.entropy_weight,
            },
            op_tfid.identity,
        )

        return result, op_tfid

    def collapse_expression(self, expr_str: str) -> Tuple[Any, ExpressionTree]:
        """
        Collapse a UML expression using the collapse protocol, with visualization.

        Args:
            expr_str: UML expression string

        Returns:
            Tuple of (result, expression tree with collapse visualization)
        """
        # Parse the expression into an operation tree
        operation = self.parse_expression(expr_str)

        # Create expression tree for visualization
        tree = ExpressionTree(operation)

        # Generate possible collapse paths
        collapse_paths = self._generate_collapse_paths(operation)

        # Select a path using the collapse protocol
        path_idx, path_entropy = self.collapse_protocol.select_collapse_path(
            collapse_paths
        )
        selected_path = collapse_paths[path_idx]

        # Execute each step in the selected path
        result = None
        collapse_steps = []
        total_entropy_delta = 0

        for step_op in selected_path:
            # Execute the operation
            step_result, step_tfid = self.execute_operation(step_op)

            # Calculate entropy change
            if result is None:
                entropy_delta = -step_op.entropy_weight  # Initial entropy reduction
            else:
                # Entropy change is difference between previous and current complexity
                prev_complexity = len(str(result)) / 10 + 1.0
                new_complexity = len(str(step_result)) / 10 + 1.0
                entropy_delta = (
                    new_complexity - prev_complexity - step_op.entropy_weight / 2
                )

            total_entropy_delta += entropy_delta

            # Record step for visualization
            tree.add_collapse_step(step_op, step_result, entropy_delta)

            # Save step information
            collapse_steps.append(
                {
                    "operation": str(step_op),
                    "result": str(step_result),
                    "tfid": step_tfid.identity,
                    "entropy_delta": entropy_delta,
                }
            )

            # Update result for next iteration
            result = step_result

        # Save complete collapse to memory
        collapse_id = str(uuid.uuid4())
        final_tfid = TFID()  # Create final identity for the complete collapse
        self.memory.save_tfid(final_tfid)
        self.memory.save_collapse(
            collapse_id, expr_str, collapse_steps, str(result), final_tfid.identity
        )

        return result, tree

    def _generate_collapse_paths(
        self, operation: SymbolicOperation
    ) -> List[List[SymbolicOperation]]:
        """Generate possible collapse paths for an operation."""
        # In a full implementation, this would analyze the expression tree
        # and generate multiple valid collapse sequences.
        # For now, we'll return a single path as a placeholder
        return [[operation]]

    def visualize_collapse(self, expr_str: str, mode: str = "cli") -> None:
        """
        Visualize the collapse of an expression.

        Args:
            expr_str: UML expression string
            mode: Visualization mode ("cli" for command line)
        """
        result, tree = self.collapse_expression(expr_str)

        if mode == "cli":
            tree.visualize_cli()
            print(f"\nFinal result: {result}")
        else:
            # Other visualization modes would be implemented here
            logger.warning(f"Unsupported visualization mode: {mode}")

    def query_tfid(self, identity_str: str) -> Dict[str, Any]:
        """
        Query information about a TFID.

        Args:
            identity_str: TFID identity string

        Returns:
            Dictionary of TFID information including history and related operations
        """
        tfid = self.memory.get_tfid(identity_str)
        if not tfid:
            return {"error": f"TFID {identity_str} not found"}
        # Get operations related to this TFID
        operations = self.memory.get_operations_by_tfid(identity_str)

        return {"tfid": tfid.to_dict(), "operations": operations}

    def query_expression_history(self, expr_str: str) -> Dict[str, Any]:
        """
        Query the collapse history of an expression.

        Args:
            expr_str: Expression string

        Returns:
            Dictionary of collapse history information
        """
        collapses = self.memory.get_collapse_by_expression(expr_str)

        if not collapses:
            return {"error": f"No collapse history found for expression: {expr_str}"}

        return {"expression": expr_str, "collapses": collapses}

    def run_interactive_repl(self) -> None:
        """Run an interactive REPL for UML symbolic queries."""
        print("=== UML Symbolic Engine REPL ===")
        print("Universal Mathematical Language - Offline Symbolic Calculator")
        print("Enter UML expressions or commands (exit/quit to end)")
        print("\nExample commands:")
        print("  RIS(4, 9)         - Recursive integration")
        print("  collapse([3,7])   - Visualize collapse steps")
        print('  TFID("x", 3)     - Create temporal flux identity')
        print("  trace_TFID(id)    - Trace TFID history")
        print("  memory_stats      - Show memory store statistics")
        print("  clear_memory      - Clear memory store")

        while True:
            try:
                user_input = input("\nUML> ").strip()

                if user_input.lower() in ("exit", "quit"):
                    print("Exiting UML Symbolic Engine. Memory preserved.")
                    break

                if user_input.startswith("trace_TFID("):
                    # Extract TFID identity from command
                    tfid_id = user_input[len("trace_TFID(") : -1].strip().strip("\"'")
                    result = self.query_tfid(tfid_id)
                    print(json.dumps(result, indent=2))

                elif user_input.startswith("collapse("):
                    # Visualize collapse of expression
                    expr = user_input[len("collapse(") : -1].strip()
                    self.visualize_collapse(expr)

                elif user_input.lower() == "memory_stats":
                    # Show memory store statistics
                    stats = {
                        "tfids_stored": len(self.memory.tfids),
                        "operations_stored": len(self.memory.operations),
                        "collapses_stored": len(self.memory.collapses),
                        "memory_path": self.memory.store_path,
                    }
                    print(json.dumps(stats, indent=2))

                elif user_input.lower() == "clear_memory":
                    # Clear memory store
                    confirm = input(
                        "Are you sure you want to clear all memory? (yes/no): "
                    )
                    if confirm.lower() == "yes":
                        self.memory.tfids.clear()
                        self.memory.operations.clear()
                        self.memory.collapses.clear()
                        self.memory._save_json(self.memory.tfids, self.memory.tfid_path)
                        self.memory._save_json(
                            self.memory.operations, self.memory.operations_path
                        )
                        self.memory._save_json(
                            self.memory.collapses, self.memory.collapse_path
                        )
                        print("Memory cleared.")
                    else:
                        print("Memory clear cancelled.")

                else:
                    # Treat as UML expression
                    result, tfid = self.execute_operation(
                        self.parse_expression(user_input)
                    )
                    print(f"Result: {result}")
                    print(f"TFID: {tfid}")

            except KeyboardInterrupt:
                print("\nExiting UML Symbolic Engine. Memory preserved.")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
                logger.exception("Error in REPL")


if __name__ == "__main__":
    # Example usage
    engine = SymbolicEngine()
    engine.run_interactive_repl()
