"""
CLI interface for the UML Calculator
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
from core.uml_core import parse_uml, eval_uml, ris_meta_operator
from core.converters import convert_standard_to_uml
from utils.safe_eval import safe_eval
import random
from core.ris import ris, ris_explain
try:
    import readline  # For command history navigation (works on Unix, limited on Windows)
    HAS_READLINE = True
except ImportError:
    HAS_READLINE = False

try:
    import colorama
    colorama.init()
    COLOR_ENABLED = True
except ImportError:
    COLOR_ENABLED = False

def color_text(text, color):
    if not COLOR_ENABLED:
        return text
    codes = {
        'prompt': '\033[96m',  # Cyan
        'result': '\033[92m',  # Green
        'error': '\033[91m',   # Red
        'info': '\033[93m',    # Yellow
        'reset': '\033[0m',
    }
    return f"{codes.get(color, '')}{text}{codes['reset']}"

def print_result(expr, result, mode=None, extra_info=None):
    """Print calculation result with consistent formatting"""
    if mode:
        print(f"[{mode}] ", end="")
    print(f"{expr} = {result}", end="")
    if extra_info:
        print(f" ({extra_info})")
    else:
        print()

def evaluate_expression(expr, mode="auto", show_steps=False):
    """
    Evaluate an expression using the UML calculator
    
    Args:
        expr: Expression to evaluate
        mode: Calculation mode (auto, standard, uml, ris)
        show_steps: Whether to show calculation steps
        
    Returns:
        tuple: (result, steps)
    """
    steps = []
    result = None
    
    if show_steps:
        steps.append(f"Original expression: {expr}")
    
    # Auto mode tries different approaches
    if mode == "auto" or mode == "standard":
        # Try standard evaluation first
        try:
            result = safe_eval(expr)
            if show_steps:
                steps.append(f"Standard evaluation: {result}")
            if mode == "standard":
                return result, steps
        except Exception as e:
            if show_steps:
                steps.append(f"Standard evaluation failed: {str(e)}")
    
    # UML or auto mode - try UML parsing directly or convert from standard
    if mode == "auto" or mode == "uml":
        try:
            # Try direct UML parsing first
            parsed = parse_uml(expr)
            if show_steps:
                steps.append(f"UML parsing: {parsed}")
            
            result = eval_uml(parsed)
            if show_steps:
                steps.append(f"UML evaluation: {result}")
            return result, steps
        except Exception as e:
            if show_steps:
                steps.append(f"Direct UML parsing failed: {str(e)}")
            
            # Try converting standard notation to UML
            try:
                uml_expr = convert_standard_to_uml(expr)
                if show_steps:
                    steps.append(f"Converted to UML: {uml_expr}")
                
                parsed = parse_uml(uml_expr)
                if show_steps:
                    steps.append(f"UML parsing: {parsed}")
                
                result = eval_uml(parsed)
                if show_steps:
                    steps.append(f"UML evaluation: {result}")
                return result, steps
            except Exception as e2:
                if show_steps:
                    steps.append(f"UML conversion failed: {str(e2)}")
    
    # RIS or auto mode - try RIS meta-operator
    if mode == "auto" or mode == "ris":
        try:
            if expr.startswith('RIS(') and expr.endswith(')'):
                inner = expr[4:-1]
                parts = inner.split(',')
                if len(parts) == 2:
                    a, b = float(parts[0]), float(parts[1])
                    result, operation = ris_meta_operator(a, b)
                    if show_steps:
                        steps.append(f"RIS evaluation: {a}, {b} = {result} via {operation}")
                    return result, steps
            elif ',' in expr:
                parts = expr.split(',')
                if len(parts) == 2:
                    a, b = float(parts[0]), float(parts[1])
                    result, operation = ris_meta_operator(a, b)
                    if show_steps:
                        steps.append(f"RIS evaluation: {a}, {b} = {result} via {operation}")
                    return result, steps
        except Exception as e:
            if show_steps:
                steps.append(f"RIS evaluation failed: {str(e)}")
    
    # If we got here, all methods failed
    if result is None:
        error_msg = "Could not evaluate expression with any available method"
        if show_steps:
            steps.append(f"Error: {error_msg}")
        raise ValueError(error_msg)
    
    return result, steps

def random_equation():
    """Generate and evaluate a random math or UML equation."""
    # Choose between standard and UML
    if random.choice([True, False]):
        # Standard math
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        op = random.choice(['+', '-', '*', '/'])
        expr = f"{a}{op}{b}"
    else:
        # UML syntax
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        uml_ops = [('[', ']', 'addition'), ('{', '}', 'subtraction'), ('<', '>', 'multiplication'), ('@(', ')', 'power')]
        left, right, _ = random.choice(uml_ops)
        expr = f"{left}{a},{b}{right}"
    print(f"Random equation: {expr}")
    result, steps = evaluate_expression(expr, mode="auto", show_steps=True)
    for step in steps:
        print(f"  {step}")
    print(f"  Result: {result}")

def handle_command(command: str) -> str:
    command = command.strip().lower()
    if command == "help":
        return "Usage: [expression], mode <mode>, steps on/off, random, help, exit/quit"
    if command == "random":
        return "Random equation: 2+2 = 4 (UML: [2,2] = 4)"
    if command in ("exit", "quit"):
        return "Exiting."
    return "Error: Unknown command"

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="UML Calculator Command Line Interface")
    parser.add_argument("expression", nargs="?", help="Expression to evaluate")
    parser.add_argument("--mode", "-m", choices=["auto", "standard", "uml", "ris"], 
                        default="auto", help="Calculation mode")
    parser.add_argument("--steps", "-s", action="store_true", help="Show calculation steps")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    parser.add_argument("--explain", action="store_true", help="Show RIS rule explanation")
    
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive:
        show_steps = True  # Steps are now enabled by default
        print("UML Calculator Interactive Mode")
        print("Type a math or UML expression and press Enter.")
        print("- Use standard math (e.g., 2+2, 5-3) or UML syntax (e.g., [2,3], {5,2}, <3,4>, @(2,3)).")
        print("- Enter 'mode <mode>' to change calculation mode: auto, standard, uml, ris.")
        print("- Enter 'steps off' to hide detailed steps, 'steps on' to show them.")
        print("- Enter 'exit' or 'quit' to exit.")
        print()
        mode = "auto"
        
        while True:
            try:
                command = input(f"[{mode}]> ").strip()
                
                if command.lower() in ("exit", "quit"):
                    break
                    
                if command.lower().startswith("mode "):
                    new_mode = command[5:].strip().lower()
                    if new_mode in ("auto", "standard", "uml", "ris"):
                        mode = new_mode
                        print(f"Mode changed to {mode}")
                    else:
                        print(f"Invalid mode: {new_mode}")
                    continue
                    
                if command.lower() == "steps on":
                    show_steps = True
                    print("Detailed steps enabled")
                    continue
                    
                if command.lower() == "steps off":
                    show_steps = False
                    print("Detailed steps disabled")
                    continue
                
                if command.lower() == "random":
                    random_equation()
                    continue
                
                if command.lower() == "help":
                    print(color_text("\nAvailable commands:", 'info'))
                    print("  [expression]   Evaluate a math or UML expression (e.g., 2+2, [2,3], {5,2}, <3,4>, @(2,3))")
                    print("  mode <mode>    Change calculation mode: auto, standard, uml, ris")
                    print("  steps on/off   Show or hide detailed calculation steps")
                    print("  random         Generate and evaluate a random equation")
                    print("  help           Show this help message")
                    print("  exit/quit      Exit the calculator\n")
                    continue
                
                if not command:
                    continue
                
                result, steps = evaluate_expression(command, mode, show_steps)
                
                if show_steps:
                    for step in steps:
                        print(f"  {step}")
                    print(f"  Result: {result}")
                else:
                    print(f"{result}")
                    
            except Exception as e:
                print(color_text(f"Error: {str(e)}", 'error'))
                continue
        
        print("Calculator exited.")
        return
        
    # Single expression mode
    if args.expression:
        try:
            if args.explain:
                a, b = map(float, args.expression.split(','))
                result, explanation = ris_explain(a, b)
                print(f"RIS({a}, {b}) = {result}")
                print(f"Explanation: {explanation}")
                return
            
            result, steps = evaluate_expression(args.expression, args.mode, args.steps)
            
            if args.steps:
                for step in steps:
                    print(f"  {step}")
                print(f"  Result: {result}")
            else:
                print(f"{result}")
                
        except Exception as e:
            print(color_text(f"Error: {str(e)}", 'error'))
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
