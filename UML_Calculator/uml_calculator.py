"""
Enhanced UML Calculator with Multiple Interfaces
Integrates the enhanced UML core with modern UI options including Tkinter desktop app and enhanced CLI. All built on the conversation-analysis-enhanced
UML core with RIS meta-operator, recursive compression, and T.R.E.E.S. principles.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import datetime
from typing import Any, Dict, List, Tuple, Optional

# Import safe_eval
from safe_eval import safe_eval

# Import the enhanced UML core
from uml_core import (
    parse_uml, eval_uml, eval_recursive_compress, 
    ris_meta_operator
)

# Import convert_standard_to_uml from the correct module
from enhanced_convert_standard_to_uml import convert_standard_to_uml

# Only import what is used from symbolic_extensions
from symbolic_extensions import base52_encode, fibonacci, is_prime, gcd, lcm

class UMLCalculatorGUI:
    """Enhanced Tkinter GUI for UML Calculator with modern styling"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("UML Calculator - Enhanced with T.R.E.E.S. Principles")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Variables
        self.history = []
        self.current_expression = tk.StringVar()
        self.result_var = tk.StringVar(value="0")
        self.mode_var = tk.StringVar(value="standard")
        
        self.setup_styles()
        self.create_widgets()
        self.bind_keyboard()
        
    def setup_styles(self):
        """Configure modern, friendly styling with dynamic scaling"""
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Modern color palette
        primary_bg = '#232946'
        accent = '#eebbc3'
        button_bg = '#393e46'
        button_fg = '#f4f4f4'
        entry_bg = '#f4f4f4'
        entry_fg = '#232946'
        border_radius = 10

        # Title
        self.style.configure('Title.TLabel', 
            background=primary_bg, 
            foreground=accent, 
            padding=10)

        # Display
        self.style.configure('Display.TFrame', 
            background=button_bg, 
            relief='sunken', 
            borderwidth=2)

        # Buttons
        self.style.configure('Calc.TButton',
            padding=15,
            background=button_bg,
            foreground=button_fg,
            borderwidth=0)
        self.style.map('Calc.TButton',
            background=[('active', accent)],
            foreground=[('active', primary_bg)])

        self.style.configure('Button.TButton',
            padding=10,
            background=button_bg,
            foreground=button_fg,
            borderwidth=0)
        self.style.map('Button.TButton',
            background=[('active', accent)],
            foreground=[('active', primary_bg)])

        # Entry
        self.style.configure('TEntry',
            fieldbackground=entry_bg,
            foreground=entry_fg,
            padding=8)

        # LabelFrame
        self.style.configure('TLabelframe', background=primary_bg, foreground=accent)
        self.style.configure('TLabelframe.Label', background=primary_bg, foreground=accent)

        # Make widgets scale with window
        self.root.option_add('*TButton*relief', 'flat')
        self.root.option_add('*TButton*highlightThickness', 0)
        self.root.option_add('*TButton*borderWidth', 0)
        self.root.option_add('*TButton*padding', 10)
        self.root.option_add('*TEntry*padding', 8)
        self.root.option_add('*Font', 'Segoe UI 13')

        # Set minimum window size for usability
        self.root.minsize(600, 400)
        
    def create_widgets(self):
        """Create and layout GUI widgets with dynamic scaling and friendly UI"""
        # Define fonts and colors for direct use
        primary_bg = '#232946'
        accent = '#eebbc3'
        text_color = '#f4f4f4'
          # Title
        title_frame = tk.Frame(self.root, bg=primary_bg)
        title_frame.pack(fill='x', padx=10, pady=5)
        tk.Label(title_frame, text="UML Calculator", font="Arial 20 bold", bg=primary_bg, fg=accent).pack()
        tk.Label(title_frame, text="Universal Mathematical Language • T.R.E.E.S. Ready", font="Arial 12", bg=primary_bg, fg=accent).pack()
        tk.Label(title_frame, text="Welcome! Enter any math or UML expression below", font="Arial 10 italic", bg=primary_bg, fg=text_color).pack(pady=(0, 5))

        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        main_frame.columnconfigure(0, weight=2)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Left panel - Calculator
        calc_frame = ttk.LabelFrame(main_frame, text="Calculator", padding=10)
        calc_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        calc_frame.columnconfigure(0, weight=1)
        calc_frame.rowconfigure(2, weight=1)

        # Display
        display_frame = tk.Frame(calc_frame, bg='#393e46', relief='sunken', bd=2)
        display_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        display_frame.columnconfigure(0, weight=1)

        entry = ttk.Entry(display_frame, textvariable=self.current_expression, font=('Segoe UI', 18),
                         justify='right')
        entry.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        entry.insert(0, "Type an expression (e.g. 2+3*4 or [2,3])")
        entry.bind('<FocusIn>', lambda e: entry.delete(0, 'end') if entry.get().startswith('Type an') else None)

        result_label = tk.Label(display_frame, textvariable=self.result_var, anchor='e',
                                font=('Segoe UI', 16, 'bold'), bg='#393e46', fg='#eebbc3')
        result_label.grid(row=1, column=0, sticky='ew', padx=5, pady=(0, 5))

        # Mode selection
        mode_frame = ttk.Frame(calc_frame)
        mode_frame.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        ttk.Label(mode_frame, text="Mode:", font=('Segoe UI', 12)).pack(side='left', padx=(0, 5))
        for mode, label in [("standard", "Standard"), ("uml", "UML"), ("ris", "RIS")]:
            ttk.Radiobutton(mode_frame, text=label, variable=self.mode_var, value=mode).pack(side='left', padx=2)

        # Calculator buttons
        self.create_button_grid(calc_frame)        # Control buttons
        control_frame = ttk.Frame(calc_frame)
        control_frame.grid(row=3, column=0, sticky='ew', pady=5)
        control_frame.columnconfigure((0,1,2,3,4), weight=1)
        
        # Using tk buttons for consistent styling
        tk.Button(control_frame, text="Calculate", command=self.calculate, 
                  font="Arial 16 bold", bg='#393e46', fg='#f4f4f4',
                  relief='flat', bd=0, padx=10, pady=15,
                  activebackground=accent, activeforeground=primary_bg).grid(row=0, column=0, padx=2, sticky='ew')
        
        tk.Button(control_frame, text="Show Steps", command=self.show_uml_steps,
                  font="Arial 13", bg='#393e46', fg='#f4f4f4',
                  relief='flat', bd=0, padx=10, pady=10,
                  activebackground=accent, activeforeground=primary_bg).grid(row=0, column=1, padx=2, sticky='ew')
          tk.Button(control_frame, text="Clear", command=self.clear,
                  font="Arial 13", bg='#393e46', fg='#f4f4f4',
                  relief='flat', bd=0, padx=10, pady=10,
                  activebackground=accent, activeforeground=primary_bg).grid(row=0, column=2, padx=2, sticky='ew')
        
        tk.Button(control_frame, text="Demo", command=self.show_demo,
                  font="Arial 13", bg='#393e46', fg='#f4f4f4',
                  relief='flat', bd=0, padx=10, pady=10,
                  activebackground=accent, activeforeground=primary_bg).grid(row=0, column=3, padx=2, sticky='ew')
        
        tk.Button(control_frame, text="Tests", command=self.run_tests,
                  font="Arial 13", bg='#393e46', fg='#f4f4f4',
                  relief='flat', bd=0, padx=10, pady=10,
                  activebackground=accent, activeforeground=primary_bg).grid(row=0, column=4, padx=2, sticky='ew')

        # Right panel - History and Advanced
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky='nsew')
        right_frame.rowconfigure(0, weight=2)
        right_frame.rowconfigure(1, weight=1)
        right_frame.columnconfigure(0, weight=1)

        # History
        history_frame = ttk.LabelFrame(right_frame, text="History", padding=5)
        history_frame.grid(row=0, column=0, sticky='nsew', pady=(0, 5))
          self.history_text = scrolledtext.ScrolledText(history_frame, height=15, 
            font="Arial 12", wrap='word', bg='#f4f4f4', fg='#232946', borderwidth=0)
        self.history_text.pack(fill='both', expand=True)
        self.history_text.insert('end', "Your calculation history will appear here.\n")
        self.history_text.config(state='disabled')

        # Advanced/Help
        advanced_frame = ttk.LabelFrame(right_frame, text="Help & Advanced", padding=5)
        advanced_frame.grid(row=1, column=0, sticky='nsew')
        
        help_text = (
            "• Enter any math or UML expression and press Calculate.\n"
            "• Use 'Show Steps' to see how your input is parsed and solved.\n"
            "• Modes: Standard (normal math), UML (symbolic), RIS (meta-operator).\n"
            "• Example: 2+3*4, [2,3], <2,3>, RIS(3,4), etc.\n"
            "• Click Demo or Tests for more examples.\n"
        )
        
        help_label = tk.Label(advanced_frame, text=help_text, font="Arial 11", 
                             anchor='w', justify='left', bg='#f4f4f4', fg='#232946')
        help_label.pack(fill='both', expand=True)
    
    def create_button_grid(self, parent):
        """Create calculator button grid"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=10)
        
        # Basic calculator buttons
        buttons = [
            ['7', '8', '9', '/', 'AC'],
            ['4', '5', '6', '*', '('],
            ['1', '2', '3', '-', ')'],
            ['0', '.', '=', '+', '⌫'],
            ['[', ']', '{', '}', ','],
            ['<', '>', '?', '/', '@'],
            ['A', 'B', 'C', 'z', '!']
        ]
        
        for row_idx, button_row in enumerate(buttons):
            for col_idx, button_text in enumerate(button_row):
                if button_text == '=':
                    btn = ttk.Button(button_frame, text=button_text, 
                                   command=self.calculate, width=3)
                elif button_text == 'AC':
                    btn = ttk.Button(button_frame, text=button_text, 
                                   command=self.clear, width=3)
                elif button_text == '⌫':
                    btn = ttk.Button(button_frame, text=button_text, 
                                   command=self.backspace, width=3)
                else:
                    btn = ttk.Button(button_frame, text=button_text, 
                                   command=lambda t=button_text: self.add_to_expression(t), 
                                   width=3)
                btn.grid(row=row_idx, column=col_idx, padx=1, pady=1)
        
        # Add conversion buttons
        conversion_frame = ttk.LabelFrame(button_frame.master, text="Conversion Tools", padding=5)
        conversion_frame.pack(fill='x', pady=(10, 0))
        
        conversion_buttons = [
            ("Convert to UML", self.convert_to_uml),
            ("Convert to Base52", self.convert_to_base52),
            ("Show UML Steps", self.show_uml_steps),
            ("Arithmetic Test", self.run_arithmetic_tests),
            ("Random Test", self.random_test_suite)
        ]
        
        for i, (text, command) in enumerate(conversion_buttons):
            ttk.Button(conversion_frame, text=text, command=command, 
                      width=15).grid(row=i//3, column=i%3, padx=2, pady=2)
    
    def bind_keyboard(self):
        """Bind keyboard shortcuts"""
        self.root.bind('<Return>', lambda e: self.calculate())
        self.root.bind('<Delete>', lambda e: self.clear())
        self.root.bind('<BackSpace>', lambda e: self.backspace())
        self.expression_entry.focus_set()
    
    def add_to_expression(self, text):
        """Add text to current expression"""
        current = self.current_expression.get()
        self.current_expression.set(current + text)    
    def clear(self):
        """Clear the calculator"""
        self.current_expression.set("")
        self.result_var.set("0")

    def backspace(self):
        """Remove last character"""
        current = self.current_expression.get()
        self.current_expression.set(current[:-1])
        
    def calculate(self):
        """Calculate the current expression"""
        expression = self.current_expression.get().strip()
        if not expression:
            return
            
        try:
            mode = self.mode_var.get()
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            
            # UML Mode
            if mode == "uml":
                # Try direct UML parsing first
                try:
                    parsed = parse_uml(expression)
                    result = eval_uml(parsed)
                    self.result_var.set(f"UML: {result}")
                    history_entry = f"[{timestamp}] UML: {expression} = {result}"
                except Exception:
                    # Try to convert standard arithmetic to UML notation
                    try:
                        converted = convert_standard_to_uml(expression)
                        parsed = parse_uml(converted)
                        result = eval_uml(parsed)
                        self.result_var.set(f"UML: {result}")
                        history_entry = f"[{timestamp}] Converted: {expression} → {converted} = {result}"
                    except (ValueError, ZeroDivisionError, OverflowError):
                        self.result_var.set("Error")
                        history_entry = f"[{timestamp}] Error: {expression}"
            # RIS Mode
            elif mode == "ris":
                # Try RIS notation like @(a,b) first
                if expression.startswith('@(') and expression.endswith(')'):
                    try:
                        # Extract values from @(a,b) notation
                        inner = expression[2:-1]
                        parts = inner.split(',')
                        if len(parts) == 2:
                            a, b = float(parts[0].strip()), float(parts[1].strip())
                            result, operation = ris_meta_operator(a, b)
                            self.result_var.set(f"RIS: {result} via {operation}")
                            history_entry = f"[{timestamp}] {expression} = {result} via {operation}"
                        else:
                            self.result_var.set("RIS Error: Format should be @(a,b)")
                            return
                    except Exception:
                        self.result_var.set(f"RIS Error: Cannot parse {expression}")
                        return
                # Try comma-separated values
                elif ',' in expression:
                    parts = expression.replace('(', '').replace(')', '').split(',')
                    if len(parts) == 2:
                        try:
                            a, b = float(parts[0].strip()), float(parts[1].strip())
                            result, operation = ris_meta_operator(a, b)
                            self.result_var.set(f"RIS: {result} via {operation}")
                            history_entry = f"[{timestamp}] RIS({a},{b}) = {result} via {operation}"
                        except Exception:
                            self.result_var.set("RIS Error: Invalid numbers")
                            return
                    else:
                        self.result_var.set("RIS Error: Format should be a,b")
                        return
                else:
                    # Try to intelligently parse arithmetic expressions
                    import re
                    arithmetic_pattern = r'^(\d+(?:\.\d+)?)([+\-*/])(\d+(?:\.\d+)?)$'
                    match = re.match(arithmetic_pattern, expression.replace(' ', ''))
                    if match:
                        a, op, b = match.groups()
                        a, b = float(a), float(b)
                        result, operation = ris_meta_operator(a, b)
                        self.result_var.set(f"RIS: {result} via {operation} (parsed {a}{op}{b})")
                        history_entry = f"[{timestamp}] RIS({a},{b}) = {result} via {operation}"
                    else:
                        self.result_var.set("RIS Error: Use format a,b or simple arithmetic")
                        return
            else:
                # Standard mode with extended operators
                try:
                    # Check for special function patterns
                    if expression.startswith('F[') and expression.endswith(']'):
                        # Fibonacci: F[n]
                        n = int(expression[2:-1])
                        result = fibonacci(n)
                        self.result_var.set(f"F({n}) = {result}")
                        history_entry = f"[{timestamp}] Fibonacci {expression} = {result}"
                    elif expression.startswith('P[') and expression.endswith(']'):
                        # Prime check: P[n]
                        n = int(expression[2:-1])
                        result = 1 if is_prime(n) else 0
                        status = "prime" if result else "composite"
                        self.result_var.set(f"{n} is {status}")
                        history_entry = f"[{timestamp}] Prime check {expression} = {status}"
                    elif expression.startswith('&[') and expression.endswith(']'):
                        # GCD: &[a,b]
                        parts = expression[2:-1].split(',')
                        if len(parts) == 2:
                            a, b = int(parts[0]), int(parts[1])
                            result = gcd(a, b)
                            self.result_var.set(f"GCD({a},{b}) = {result}")
                            history_entry = f"[{timestamp}] {expression} = {result}"
                        else:
                            self.result_var.set("GCD Error: Use &[a,b]")
                            return
                    elif expression.startswith('|[') and expression.endswith(']'):
                        # LCM: |[a,b]
                        parts = expression[2:-1].split(',')
                        if len(parts) == 2:
                            a, b = int(parts[0]), int(parts[1])
                            result = lcm(a, b)
                            self.result_var.set(f"LCM({a},{b}) = {result}")
                            history_entry = f"[{timestamp}] {expression} = {result}"
                        else:
                            self.result_var.set("LCM Error: Use |[a,b]")
                            return
                    elif expression.startswith('%[') and expression.endswith(']'):
                        # Modulo: %[a,b]
                        parts = expression[2:-1].split(',')
                        if len(parts) == 2:
                            a, b = float(parts[0]), float(parts[1])
                            if b == 0:
                                self.result_var.set("Modulo Error: Division by zero")
                                return
                            else:
                                result = a % b
                                self.result_var.set(f"{a} mod {b} = {result}")
                                history_entry = f"[{timestamp}] {expression} = {result}"
                        else:
                            self.result_var.set("Modulo Error: Use %[a,b]")
                            return
                    else:
                        # Try standard evaluation first
                        try:
                            result = safe_eval(expression)
                            self.result_var.set(str(result))
                            history_entry = f"[{timestamp}] {expression} = {result}"
                        except:
                            # Fall back to UML parsing
                            parsed = parse_uml(expression)
                            result = eval_uml(parsed)
                            self.result_var.set(str(result))
                            history_entry = f"[{timestamp}] {expression} = {result}"
                except (ValueError, ZeroDivisionError, OverflowError) as e:
                    self.result_var.set(f"Error: {str(e)}")
                    return
            # Add to history
            self.history.append(history_entry)
            self.update_history_display()
        except Exception as e:
            self.result_var.set(f"Error: {str(e)}")
            
    def update_history_display(self):
        """Update the history text widget"""
        self.history_text.delete(1.0, tk.END)
        for entry in self.history[-20:]:  # Show last 20 entries
            self.history_text.insert(tk.END, entry + "\n")
        self.history_text.see(tk.END)
    
    # === CONVERSION METHODS ===
    
    def convert_to_uml(self):
        """Convert current expression to UML format"""
        expression = self.current_expression.get().strip()
        if not expression:
            return
        
        try:
            # Parse and evaluate the expression first
            result = safe_eval(expression)
            
            # Convert numbers in expression to UML format
            import re
            
            # Find all numbers in the expression
            numbers = re.findall(r'\d+(?:\.\d+)?', expression)
            
            if len(numbers) >= 2:
                # Create UML representation
                uml_parts = [f"[{num}]" for num in numbers]
                operators = re.findall(r'[+\-*/]', expression)
                
                if operators:
                    # Build UML expression
                    uml_expr = f"[{','.join(numbers)}]"
                    self.current_expression.set(uml_expr)
                    self.result_var.set(f"UML: {result}")
                    
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    history_entry = f"[{timestamp}] Converted {expression} → {uml_expr} = {result}"
                    self.history.append(history_entry)
                    self.update_history_display()
                else:
                    self.result_var.set("No operators found to convert")
            else:
                self.result_var.set("Need at least 2 numbers to convert to UML")
                
        except Exception as e:
            self.result_var.set(f"Conversion Error: {str(e)}")
    
    def convert_to_base52(self):
        """Convert current expression to Base52 format"""
        expression = self.current_expression.get().strip()
        if not expression:
            return
        
        try:
            # Parse and evaluate the expression first
            result = safe_eval(expression)
            
            # Convert numbers in expression to Base52
            import re
            
            # Find all numbers in the expression
            numbers = re.findall(r'\d+(?:\.\d+)?', expression)
            
            if numbers:
                # Convert each number to Base52
                base52_numbers = []
                for num_str in numbers:
                    num = int(float(num_str))  # Convert to int for Base52
                    if num > 0:
                        base52_num = base52_encode(num)
                        base52_numbers.append(base52_num)
                    else:
                        base52_numbers.append(str(num))
                
                # Convert result to Base52 too
                result_int = int(result) if isinstance(result, (int, float)) and result > 0 else result
                result_base52 = base52_encode(result_int) if isinstance(result_int, int) and result_int > 0 else str(result)
                
                # Create Base52 UML expression
                if len(base52_numbers) >= 2:
                    base52_expr = f"[{','.join(base52_numbers)}]"
                    self.current_expression.set(base52_expr)
                    self.result_var.set(f"Base52: {result_base52}")
                    
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    history_entry = f"[{timestamp}] Base52: {expression} → {base52_expr} = {result_base52}"
                    self.history.append(history_entry)
                    self.update_history_display()
                else:
                    self.result_var.set("Need at least 2 numbers for Base52 conversion")
            else:
                self.result_var.set("No numbers found to convert to Base52")
                
        except Exception as e:
            self.result_var.set(f"Base52 Error: {str(e)}")
    
    def show_uml_steps(self):
        """Show step-by-step UML parsing and evaluation"""
        expression = self.current_expression.get().strip()
        if not expression:
            return
        
        try:
            steps = []
            steps.append(f"Original expression: {expression}")
            
            # Try standard evaluation first
            try:
                result = safe_eval(expression)
                steps.append(f"Standard evaluation: {result}")
            except:
                steps.append("Standard evaluation failed")
            
            # Try UML parsing
            try:
                parsed = parse_uml(expression)
                steps.append(f"UML parsed: {parsed}")
                
                uml_result = eval_uml(parsed)
                steps.append(f"UML evaluation: {uml_result}")
            except Exception as e:
                steps.append(f"UML parsing failed: {e}")
            
            # Try recursive compression
            try:
                compressed = eval_recursive_compress(expression)
                steps.append(f"Recursive compression: {compressed}")
            except Exception as e:
                steps.append(f"Recursive compression failed: {e}")
            
            # Show steps in a new window
            steps_text = "\n".join(steps)
            self.show_text_window("UML Processing Steps", steps_text)
            
        except Exception as e:
            self.result_var.set(f"Steps Error: {str(e)}")
    
    def run_arithmetic_tests(self):
        """Run comprehensive arithmetic tests across all modes"""
        test_cases = [
            "7+7", "1+1", "2*3", "10-4", "15/3",
            "2+3*4", "(5+3)*2", "100/10+5",
            "7*7", "9-5", "20/4", "3*3*3"
        ]
        
        results = []
        results.append("=== ARITHMETIC TEST SUITE ===\n")
        
        for expr in test_cases:
            results.append(f"Testing: {expr}")
            
            # Standard mode
            try:
                std_result = safe_eval(expr)
                results.append(f"  Standard: {std_result}")
            except Exception as e:
                results.append(f"  Standard: Error - {e}")
            
            # UML mode
            try:
                uml_result = eval_recursive_compress(expr)
                results.append(f"  UML: {uml_result}")
            except Exception as e:
                results.append(f"  UML: Error - {e}")
            
            # RIS mode (for 2-number expressions)
            import re
            match = re.match(r'^(\d+(?:\.\d+)?)\s*([+\-*/])\s*(\d+(?:\.\d+)?)$', expr)
            if match:
                try:
                    a, op, b = match.groups()
                    a, b = float(a), float(b)
                    ris_result, operation = ris_meta_operator(a, b)
                    results.append(f"  RIS: {ris_result} via {operation}")
                except Exception as e:
                    results.append(f"  RIS: Error - {e}")
            else:
                results.append(f"  RIS: Not applicable")
            
            results.append("")  # Empty line
        
        # Show results
        self.show_text_window("Arithmetic Test Results", "\n".join(results))
    
    def random_test_suite(self):
        """Run randomized test cases"""
        import random
        
        results = []
        results.append("=== RANDOM TEST SUITE ===\n")
        
        # Generate random test cases
        for i in range(10):
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            op = random.choice(['+', '-', '*', '/'])
            
            if op == '/' and b == 0:
                b = 1  # Avoid division by zero
            
            expr = f"{a}{op}{b}"
            results.append(f"Test {i+1}: {expr}")
            
            # Test all modes
            try:
                std_result = safe_eval(expr)
                results.append(f"  Standard: {std_result}")
                
                uml_result = eval_recursive_compress(expr)
                results.append(f"  UML: {uml_result}")
                
                ris_result, operation = ris_meta_operator(float(a), float(b))
                results.append(f"  RIS: {ris_result} via {operation}")
                
                # Base52 conversion
                base52_a = base52_encode(a)
                base52_b = base52_encode(b)
                base52_result = base52_encode(int(std_result)) if isinstance(std_result, (int, float)) and std_result > 0 else str(std_result)
                results.append(f"  Base52: [{base52_a},{base52_b}] = {base52_result}")
                
            except Exception as e:
                results.append(f"  Error: {e}")
            
            results.append("")  # Empty line        # Show results
        self.show_text_window("Random Test Results", "\n".join(results))
    
    def show_demo(self):
        """Show demo information"""
        messagebox.showinfo("Demo", "Demo feature coming soon!")
    
    def run_tests(self):
        """Run the test suite"""
        messagebox.showinfo("Tests", "Test suite coming soon!")
    
    def show_vector_demo(self):
        messagebox.showinfo("Vector Ops", "Vector operations demo coming soon!")
    def show_matrix_demo(self):
        messagebox.showinfo("Matrix Ops", "Matrix operations demo coming soon!")
    def show_stats_demo(self):
        messagebox.showinfo("Statistics", "Statistics demo coming soon!")
    def show_number_theory_demo(self):
        messagebox.showinfo("Number Theory", "Number theory demo coming soon!")
    def show_base52_demo(self):
        messagebox.showinfo("Base52", "Base52 demo coming soon!")
    def show_si_demo(self):
        messagebox.showinfo("SI Prefixes", "SI prefixes demo coming soon!")
    def ris_demo(self):
        messagebox.showinfo("RIS Meta-Op", "RIS meta-operator demo coming soon!")
    def magic_square_demo(self):
        messagebox.showinfo("Magic Square", "Magic square demo coming soon!")
    def show_fibonacci_demo(self):
        messagebox.showinfo("Fibonacci", "Fibonacci demo coming soon!")
    def show_prime_demo(self):
        messagebox.showinfo("Prime Check", "Prime check demo coming soon!")
    def compression_demo(self):
        messagebox.showinfo("Recursive Compress", "Recursive compression demo coming soon!")
    def show_help(self):
        messagebox.showinfo("Help", "Help coming soon!")
    
    def show_text_window(self, title, text):
        """Show a text in a new window"""
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("600x400")
        txt = scrolledtext.ScrolledText(win, wrap=tk.WORD, font=("Consolas", 10))
        txt.pack(fill=tk.BOTH, expand=True)
        txt.insert(tk.END, text)
        txt.config(state=tk.DISABLED)
    
def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python uml_calculator.py [gui|test <expr>]")
        print("  gui  - Launch desktop calculator GUI")
        print("  test <expr> - Evaluate an expression in all modes")
        return
    mode = sys.argv[1].lower()
    if mode == "gui":
        app = UMLCalculatorGUI()
        app.root.mainloop()
    elif mode == "test":
        if len(sys.argv) < 3:
            print("Usage: python uml_calculator.py test <expr>")
            return
        expr = sys.argv[2]
        print(f"Standard: {expr} = {safe_eval(expr)}")
        try:
            parsed = parse_uml(expr)
            print(f"UML: {expr} = {eval_uml(parsed)}")
        except Exception as e:
            print(f"UML: {expr} = Error: {e}")
        try:
            import re
            match = re.match(r'^(\d+(?:\.\d+)?)\s*([+\-*/])\s*(\d+(?:\.\d+)?)$', expr)
            if match:
                a, op, b = match.groups()
                a, b = float(a), float(b)
                ris_result, operation = ris_meta_operator(a, b)
                print(f"RIS: {expr} = {ris_result} via {operation}")
            else:
                print("RIS: Not applicable")
        except Exception as e:
            print(f"RIS: {expr} = Error: {e}")
    else:
        print(f"Unknown mode: {mode}")
        print("Usage: python uml_calculator.py [gui|test <expr>]")

if __name__ == "__main__":
    main()
