"""
UML Calculator GUI - Modern, User-Friendly Interface
This module provides a clean, responsive Tkinter GUI for the UML Calculator.
"""

import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
import datetime
from typing import Any, Dict, List, Optional

# Import safe evaluation
from utils.safe_eval import safe_eval

# Import UML core functionality
from core.uml_core import parse_uml, eval_uml, ris_meta_operator

# Import standard-to-UML conversion
from core.converters import convert_standard_to_uml

# Import symbolic extensions
from utils.symbolic_extensions import fibonacci, is_prime, gcd, lcm

SETTINGS_FILE = os.path.join(os.path.expanduser("~"), ".uml_calculator_settings.json")


class UMLCalculatorGUI:
    """Modern Tkinter GUI for UML Calculator with responsive design"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("UML Calculator")
        self.root.geometry("900x650")

        # Set icon if available
        try:
            self.root.iconbitmap("resources/uml_icon.ico")
        except:
            pass  # Icon not available, use default

        # Variables
        self.history = []
        self.current_expression = tk.StringVar()
        self.result_var = tk.StringVar(value="0")
        self.mode_var = tk.StringVar(value="standard")

        # Configure styles and colors
        self.configure_styles()

        # Create the UI
        self.create_widgets()

        # Bind keyboard shortcuts
        self.bind_keyboard()

        # Load user settings
        self.load_user_settings()

    def configure_styles(self):
        """Set up modern UI styles and colors"""
        # Colors
        self.colors = {
            "primary": "#232946",  # Dark blue
            "secondary": "#eebbc3",  # Soft pink
            "text": "#fffffe",  # Bright white
            "accent": "#b8c1ec",  # Light lavender
            "background": "#121629",  # Deeper blue
            "highlight": "#ff8906",  # Orange highlight
        }

        # Configure root window
        self.root.configure(bg=self.colors["background"])

        # Check if system supports custom fonts
        available_fonts = font.families()

        # Use a nice font if available, fall back to system default
        if "Segoe UI" in available_fonts:
            self.main_font = "Segoe UI"
        elif "Helvetica" in available_fonts:
            self.main_font = "Helvetica"
        else:
            self.main_font = "TkDefaultFont"

        # Configure ttk styles
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use a modern theme

        # Frame styles
        self.style.configure("TFrame", background=self.colors["background"])
        self.style.configure(
            "Content.TFrame",
            background=self.colors["primary"],
            borderwidth=1,
            relief="raised",
        )

        # Label styles
        self.style.configure(
            "TLabel", background=self.colors["primary"], foreground=self.colors["text"]
        )
        self.style.configure(
            "Header.TLabel",
            background=self.colors["background"],
            foreground=self.colors["secondary"],
        )

        # Button styles
        self.style.configure(
            "TButton", background=self.colors["primary"], foreground=self.colors["text"]
        )
        self.style.map(
            "TButton",
            background=[("active", self.colors["secondary"])],
            foreground=[("active", self.colors["primary"])],
        )

        # Entry styles
        self.style.configure(
            "TEntry",
            fieldbackground=self.colors["accent"],
            foreground=self.colors["primary"],
        )

        # Make window resizable
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

    def create_widgets(self):
        """Create and arrange all UI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=2)

        # Header with title and welcome
        header_frame = tk.Frame(main_frame, bg=self.colors["background"])
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        title_label = tk.Label(
            header_frame,
            text="UML Calculator",
            font=(self.main_font, 24, "bold"),
            bg=self.colors["background"],
            fg=self.colors["secondary"],
        )
        title_label.pack(anchor="w")

        subtitle_label = tk.Label(
            header_frame,
            text="Universal Mathematical Language • T.R.E.E.S. Ready",
            font=(self.main_font, 12),
            bg=self.colors["background"],
            fg=self.colors["text"],
        )
        subtitle_label.pack(anchor="w")

        # Add theme toggle button to header
        theme_btn = tk.Button(
            header_frame,
            text="Toggle Theme",
            font=(self.main_font, 10),
            bg=self.colors["accent"],
            fg=self.colors["primary"],
            relief="flat",
            command=self.toggle_theme
        )
        theme_btn.pack(side="right", padx=10)

        # Add settings button to header
        settings_btn = tk.Button(
            header_frame,
            text="Settings",
            font=(self.main_font, 10),
            bg=self.colors["accent"],
            fg=self.colors["primary"],
            relief="flat",
            command=self.open_settings
        )
        settings_btn.pack(side="right", padx=10)

        # Add About button to header
        about_btn = tk.Button(
            header_frame,
            text="About",
            font=(self.main_font, 10),
            bg=self.colors["accent"],
            fg=self.colors["primary"],
            relief="flat",
            command=self.open_about
        )
        about_btn.pack(side="right", padx=10)

        # Left panel (Calculator)
        calculator_frame = ttk.Frame(main_frame, style="Content.TFrame")
        calculator_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        calculator_frame.columnconfigure(0, weight=1)
        calculator_frame.rowconfigure(2, weight=1)

        # Input and result area
        input_frame = tk.Frame(
            calculator_frame, bg=self.colors["primary"], padx=10, pady=10
        )
        input_frame.grid(row=0, column=0, sticky="ew")
        input_frame.columnconfigure(0, weight=1)

        # Expression entry
        entry = tk.Entry(
            input_frame,
            textvariable=self.current_expression,
            font=(self.main_font, 16),
            bg=self.colors["accent"],
            fg=self.colors["primary"],
            insertbackground=self.colors["primary"],
            relief="flat",
            borderwidth=0,
        )
        entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5, ipady=8)
        entry.insert(0, "Enter an expression")
        entry.bind("<FocusIn>", self.on_entry_focus)

        # Save entry as self.input_entry for error highlighting
        self.input_entry = entry

        # Result display
        result_display = tk.Label(
            input_frame,
            textvariable=self.result_var,
            font=(self.main_font, 20, "bold"),
            bg=self.colors["primary"],
            fg=self.colors["secondary"],
            anchor="e",
            padx=5,
        )
        result_display.grid(row=1, column=0, sticky="ew", pady=5)

        # Copy Result Button
        copy_btn = tk.Button(
            input_frame,
            text="Copy Result",
            font=(self.main_font, 10),
            bg=self.colors["accent"],
            fg=self.colors["primary"],
            relief="flat",
            command=self.copy_result_to_clipboard,
        )
        copy_btn.grid(row=1, column=1, padx=5, pady=5, sticky="e")

        # Mode selection
        mode_frame = tk.Frame(
            calculator_frame, bg=self.colors["primary"], padx=10, pady=5
        )
        mode_frame.grid(row=1, column=0, sticky="ew")

        mode_label = tk.Label(
            mode_frame,
            text="Mode:",
            font=(self.main_font, 12),
            bg=self.colors["primary"],
            fg=self.colors["text"],
        )
        mode_label.pack(side="left", padx=(0, 10))

        # Create radio buttons for mode selection
        modes = [("Standard", "standard"), ("UML", "uml"), ("RIS", "ris")]
        for text, mode in modes:
            rb = tk.Radiobutton(
                mode_frame,
                text=text,
                variable=self.mode_var,
                value=mode,
                font=(self.main_font, 12),
                bg=self.colors["primary"],
                fg=self.colors["text"],
                selectcolor=self.colors["accent"],
                activebackground=self.colors["primary"],
                activeforeground=self.colors["secondary"],
            )
            rb.pack(side="left", padx=5)

        # Calculator buttons
        button_frame = tk.Frame(
            calculator_frame, bg=self.colors["primary"], padx=10, pady=10
        )
        button_frame.grid(row=2, column=0, sticky="nsew")
        self.create_button_grid(button_frame)

        # Control buttons
        control_frame = tk.Frame(
            calculator_frame, bg=self.colors["primary"], padx=10, pady=10
        )
        control_frame.grid(row=3, column=0, sticky="ew")
        control_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)

        # Main action buttons
        self.create_button(
            control_frame, "Calculate", self.calculate, 0, 0, is_primary=True
        )
        self.create_button(control_frame, "Show Steps", self.show_uml_steps, 0, 1)
        self.create_button(control_frame, "Clear", self.clear, 0, 2)
        self.create_button(control_frame, "Demo", self.show_demo, 0, 3)
        self.create_button(control_frame, "Tests", self.run_tests, 0, 4)

        # Right panel (History and Help)
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=1, column=1, sticky="nsew")
        right_panel.rowconfigure(0, weight=2)
        right_panel.rowconfigure(1, weight=1)
        right_panel.columnconfigure(0, weight=1)

        # History panel
        history_frame = ttk.Frame(right_panel, style="Content.TFrame")
        history_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 5))

        history_header = tk.Label(
            history_frame,
            text="Calculation History",
            font=(self.main_font, 14, "bold"),
            bg=self.colors["primary"],
            fg=self.colors["secondary"],
            anchor="w",
            padx=10,
            pady=5,
        )
        history_header.pack(fill="x")

        self.history_text = scrolledtext.ScrolledText(
            history_frame,
            font=(self.main_font, 12),
            bg=self.colors["accent"],
            fg=self.colors["primary"],
            wrap="word",
            borderwidth=0,
            state="disabled",
        )
        self.history_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.history_text.tag_configure('even', background=self.colors["accent"])
        self.history_text.tag_configure('odd', background=self.colors["background"])
        self.history_text.insert("end", "Your calculation history will appear here.\n", 'even')
        self.history_text.config(state="disabled")

        # Help panel
        help_frame = ttk.Frame(right_panel, style="Content.TFrame")
        help_frame.grid(row=1, column=0, sticky="nsew")

        help_header = tk.Label(
            help_frame,
            text="Quick Guide",
            font=(self.main_font, 14, "bold"),
            bg=self.colors["primary"],
            fg=self.colors["secondary"],
            anchor="w",
            padx=10,
            pady=5,
        )
        help_header.pack(fill="x")

        help_text = "\n".join(
            [
                "• Enter expressions and press Calculate or Enter",
                "• UML Notation:",
                "  - Addition: [a,b]",
                "  - Subtraction: {a,b}",
                "  - Multiplication: <a,b>",
                "  - Division: <>a,b<>",
                "  - Power: @(a,b)",
                "• Standard notation (2+3*4) also works",
                "• Use Show Steps to see the calculation process",
            ]
        )

        help_content = tk.Label(
            help_frame,
            text=help_text,
            font=(self.main_font, 12),
            bg=self.colors["accent"],
            fg=self.colors["primary"],
            justify="left",
            anchor="w",
            padx=10,
            pady=10,
        )
        help_content.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Bind history click
        self.history_text.bind("<Button-1>", self.on_history_click)

    def on_history_click(self, event):
        index = self.history_text.index(f"@{event.x},{event.y}")
        line = int(index.split('.')[0]) - 1
        if 0 <= line < len(self.history):
            expr = self.history[line].split('=')[0].strip()
            self.current_expression.set(expr)

    def create_button_grid(self, parent):
        """Create the calculator buttons grid"""
        # Button definitions: (text, row, column, colspan, function)
        buttons = [
            ("7", 0, 0, 1, lambda: self.add_to_expression("7")),
            ("8", 0, 1, 1, lambda: self.add_to_expression("8")),
            ("9", 0, 2, 1, lambda: self.add_to_expression("9")),
            ("/", 0, 3, 1, lambda: self.add_to_expression("/")),
            ("(", 0, 4, 1, lambda: self.add_to_expression("(")),
            ("4", 1, 0, 1, lambda: self.add_to_expression("4")),
            ("5", 1, 1, 1, lambda: self.add_to_expression("5")),
            ("6", 1, 2, 1, lambda: self.add_to_expression("6")),
            ("*", 1, 3, 1, lambda: self.add_to_expression("*")),
            (")", 1, 4, 1, lambda: self.add_to_expression(")")),
            ("1", 2, 0, 1, lambda: self.add_to_expression("1")),
            ("2", 2, 1, 1, lambda: self.add_to_expression("2")),
            ("3", 2, 2, 1, lambda: self.add_to_expression("3")),
            ("-", 2, 3, 1, lambda: self.add_to_expression("-")),
            ("^", 2, 4, 1, lambda: self.add_to_expression("^")),
            ("0", 3, 0, 1, lambda: self.add_to_expression("0")),
            (".", 3, 1, 1, lambda: self.add_to_expression(".")),
            ("←", 3, 2, 1, self.backspace),
            ("+", 3, 3, 1, lambda: self.add_to_expression("+")),
            ("RIS", 3, 4, 1, lambda: self.add_to_expression("RIS(,)")),
        ]

        # UML notation buttons row
        uml_buttons = [
            ("[,]", 4, 0, 1, lambda: self.add_to_expression("[,]")),
            ("{,}", 4, 1, 1, lambda: self.add_to_expression("{,}")),
            ("<,>", 4, 2, 1, lambda: self.add_to_expression("<,>")),
            ("<>,,<>", 4, 3, 1, lambda: self.add_to_expression("<>,,<>")),
            ("@(,)", 4, 4, 1, lambda: self.add_to_expression("@(,)")),
        ]

        # Configure grid
        for i in range(5):
            parent.columnconfigure(i, weight=1)
        for i in range(5):
            parent.rowconfigure(i, weight=1)

        # Create all buttons
        for text, row, col, colspan, command in buttons:
            button = tk.Button(
                parent,
                text=text,
                font=(self.main_font, 14),
                bg=self.colors["accent"],
                fg=self.colors["primary"],
                activebackground=self.colors["secondary"],
                activeforeground=self.colors["primary"],
                relief="flat",
                borderwidth=0,
                command=command,
            )
            button.grid(
                row=row, column=col, columnspan=colspan, sticky="nsew", padx=2, pady=2
            )

        # Create UML notation buttons (with different style)
        for text, row, col, colspan, command in uml_buttons:
            button = tk.Button(
                parent,
                text=text,
                font=(self.main_font, 14),
                bg=self.colors["secondary"],
                fg=self.colors["primary"],
                activebackground=self.colors["highlight"],
                activeforeground=self.colors["primary"],
                relief="flat",
                borderwidth=0,
                command=command,
            )
            button.grid(
                row=row, column=col, columnspan=colspan, sticky="nsew", padx=2, pady=2
            )

    def create_button(self, parent, text, command, row, col, is_primary=False):
        """Create a styled button"""
        if is_primary:
            bg_color = self.colors["highlight"]
        else:
            bg_color = self.colors["accent"]

        button = tk.Button(
            parent,
            text=text,
            font=(self.main_font, 12, "bold" if is_primary else ""),
            bg=bg_color,
            fg=self.colors["primary"],
            activebackground=self.colors["secondary"],
            activeforeground=self.colors["primary"],
            relief="flat",
            borderwidth=0,
            padx=10,
            pady=10,
            command=command,
        )
        button.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

    def bind_keyboard(self):
        """Bind keyboard shortcuts"""
        self.root.bind("<Return>", lambda e: self.calculate())
        self.root.bind("<KP_Enter>", lambda e: self.calculate())
        self.root.bind("<BackSpace>", lambda e: self.backspace())
        self.root.bind("<Escape>", lambda e: self.clear())

    def on_entry_focus(self, event):
        """Clear placeholder text when entry is focused"""
        if self.current_expression.get() == "Enter an expression":
            self.current_expression.set("")

    def add_to_expression(self, text):
        """Add text to the current expression"""
        current = self.current_expression.get()
        if current == "Enter an expression" or current == "0":
            self.current_expression.set(text)
        else:
            self.current_expression.set(current + text)

    def backspace(self):
        """Remove the last character from the expression"""
        current = self.current_expression.get()
        if current and current != "Enter an expression":
            self.current_expression.set(current[:-1])

    def clear(self):
        """Clear the current expression"""
        self.current_expression.set("")
        self.result_var.set("0")

    def show_error(self, message):
        """Show an error message and highlight the input box"""
        self.result_var.set(f"Error: {message}")
        self.input_entry.config(bg="#ffcccc")
        self.root.after(2000, lambda: self.input_entry.config(bg=self.colors["accent"]))

    def calculate(self):
        """Calculate the current expression (UML is primary, standard is comparison)"""
        expression = self.current_expression.get().strip()
        if not expression or expression == "Enter an expression":
            return
        try:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            # Always try UML first
            try:
                parsed = parse_uml(expression)
                uml_result = eval_uml(parsed)
                uml_str = f"UML: {expression} = {uml_result}"
            except Exception as e:
                uml_result = None
                uml_str = f"UML Error: {str(e)}"
            # Try standard evaluation for comparison
            try:
                std_result = safe_eval(expression)
                std_str = f"Standard: {expression} = {std_result}"
            except Exception as e:
                std_result = None
                std_str = f"Standard Error: {str(e)}"
            # Display UML as primary, standard as comparison
            if uml_result is not None:
                self.result_var.set(f"{uml_result}")
            elif std_result is not None:
                self.result_var.set(f"{std_result}")
            else:
                self.result_var.set("Error")
            # Add both to history
            history_entry = f"[{timestamp}] {uml_str}\n[{timestamp}] {std_str}"
            self.history.append(history_entry)
            self.update_history_display()
        except Exception as e:
            self.show_error(str(e))

    def update_history_display(self):
        """Update the history text display"""
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", "end")
        for idx, entry in enumerate(self.history):
            tag = 'even' if idx % 2 == 0 else 'odd'
            self.history_text.insert("end", entry + "\n", tag)
        self.history_text.config(state="disabled")

    def show_uml_steps(self):
        """Show step-by-step UML parsing and evaluation"""
        expression = self.current_expression.get().strip()
        if not expression or expression == "Enter an expression":
            return

        try:
            steps = []
            steps.append(f"Original expression: {expression}")

            # Try standard evaluation first
            try:
                result = safe_eval(expression)
                steps.append(f"Standard evaluation: {result}")
            except Exception:
                steps.append("Standard evaluation not applicable")

            # Try converting to UML
            try:
                uml = convert_standard_to_uml(expression)
                if uml != expression:
                    steps.append(f"Converted to UML: {uml}")

                # Parse UML
                try:
                    parsed = parse_uml(uml)
                    steps.append(f"UML parsed structure: {str(parsed)}")

                    # Evaluate UML
                    result = eval_uml(parsed)
                    steps.append(f"UML evaluation result: {result}")
                except Exception as e:
                    steps.append(f"UML parsing/evaluation error: {str(e)}")
            except Exception:
                # Try direct UML parsing if conversion failed
                try:
                    parsed = parse_uml(expression)
                    steps.append(f"Direct UML parsed structure: {str(parsed)}")

                    result = eval_uml(parsed)
                    steps.append(f"UML evaluation result: {result}")
                except Exception as e:
                    steps.append(f"Direct UML error: {str(e)}")

            # Try RIS interpretation
            try:
                if "," in expression:
                    parts = expression.replace("(", "").replace(")", "").split(",")
                    if len(parts) == 2:
                        a, b = float(parts[0].strip()), float(parts[1].strip())
                        result, operation = ris_meta_operator(a, b)
                        steps.append(
                            f"RIS interpretation: {a},{b} = {result} via {operation}"
                        )
            except Exception:
                pass  # RIS not applicable

            # Show steps in a pop-up window
            self.show_step_window("Calculation Steps", steps)

        except Exception as e:
            messagebox.showerror("Error", f"Could not show steps: {str(e)}")

    def show_step_window(self, title, steps):
        """Show a window with calculation steps"""
        step_window = tk.Toplevel(self.root)
        step_window.title(title)
        step_window.geometry("600x400")
        step_window.configure(bg=self.colors["background"])

        # Make window modal
        step_window.transient(self.root)
        step_window.grab_set()

        # Add a title
        title_label = tk.Label(
            step_window,
            text=title,
            font=(self.main_font, 16, "bold"),
            bg=self.colors["background"],
            fg=self.colors["secondary"],
        )
        title_label.pack(fill="x", pady=10, padx=10)

        # Create scrolled text for steps
        steps_text = scrolledtext.ScrolledText(
            step_window,
            font=(self.main_font, 12),
            bg=self.colors["accent"],
            fg=self.colors["primary"],
            wrap="word",
            padx=10,
            pady=10,
            borderwidth=0,
        )
        steps_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Insert steps
        for step in steps:
            steps_text.insert("end", step + "\n\n")

        # Add close button
        close_button = tk.Button(
            step_window,
            text="Close",
            font=(self.main_font, 12),
            bg=self.colors["secondary"],
            fg=self.colors["primary"],
            activebackground=self.colors["highlight"],
            activeforeground=self.colors["primary"],
            relief="flat",
            borderwidth=0,
            padx=20,
            pady=10,
            command=step_window.destroy,
        )
        close_button.pack(pady=(0, 10))

        # Focus the window
        step_window.focus_set()

    def show_demo(self):
        """Show a demonstration of UML Calculator capabilities"""
        demo_expressions = [
            "2+3*4",
            "[2,<3,4>]",
            "RIS(3,4)",
            "<>10,2<>",
            "@(2,3)",
            "!(3,4)",
        ]

        steps = ["UML Calculator Demonstration:"]

        for expr in demo_expressions:
            steps.append(f"\nExpression: {expr}")

            try:
                if expr.startswith("RIS("):
                    # RIS demo
                    inner = expr[4:-1]
                    parts = inner.split(",")
                    if len(parts) == 2:
                        a, b = float(parts[0].strip()), float(parts[1].strip())
                        result, operation = ris_meta_operator(a, b)
                        steps.append(f"RIS Result: {result} via {operation}")
                else:
                    # Try direct UML parsing first
                    try:
                        parsed = parse_uml(expr)
                        steps.append(f"UML Structure: {str(parsed)}")

                        result = eval_uml(parsed)
                        steps.append(f"Result: {result}")
                    except (ValueError, TypeError, SyntaxError):
                        # Try standard evaluation
                        try:
                            uml = convert_standard_to_uml(expr)
                            steps.append(f"Converted to UML: {uml}")

                            parsed = parse_uml(uml)
                            result = eval_uml(parsed)
                            steps.append(f"Result: {result}")
                        except (ValueError, TypeError, SyntaxError) as e:
                            steps.append(f"Error: {str(e)}")
            except Exception as e:
                steps.append(f"Error: {str(e)}")

        self.show_step_window("UML Calculator Demo", steps)

    def run_tests(self):
        """Run a test suite of common operations"""
        test_expressions = [
            # Standard arithmetic
            "2+3",
            "10-5",
            "4*8",
            "20/4",
            "2^5",
            "10%3",
            # Order of operations
            "2+3*4",
            "(2+3)*4",
            # UML notation
            "[2,3]",
            "{10,3}",
            "<4,5>",
            "<>20,5<>",
            "@(3,2)",
            # Complex
            "RIS(3,4)",
            "RIS(25,5)",
        ]

        steps = ["UML Calculator Test Suite:"]

        for expr in test_expressions:
            steps.append(f"\nTest: {expr}")

            try:
                # Try UML parsing first
                try:
                    parsed = parse_uml(expr)
                    result = eval_uml(parsed)
                    steps.append(f"UML Result: {result}")
                except (ValueError, TypeError, SyntaxError):
                    # Try standard evaluation
                    try:
                        if expr.startswith("RIS("):
                            # RIS test
                            inner = expr[4:-1]
                            parts = inner.split(",")
                            if len(parts) == 2:
                                a, b = float(parts[0].strip()), float(parts[1].strip())
                                result, operation = ris_meta_operator(a, b)
                                steps.append(f"RIS Result: {result} via {operation}")
                        else:
                            # Standard eval
                            result = safe_eval(expr)
                            steps.append(f"Standard Result: {result}")

                            # Also try UML conversion
                            uml = convert_standard_to_uml(expr)
                            steps.append(f"Converted to UML: {uml}")

                            parsed = parse_uml(uml)
                            uml_result = eval_uml(parsed)
                            steps.append(f"UML Result: {uml_result}")

                            if abs(result - uml_result) < 1e-10:
                                steps.append("PASS: Results match")
                            else:
                                steps.append(
                                    f"WARN: Results differ ({result} vs {uml_result})"
                                )
                    except (ValueError, TypeError, SyntaxError) as e:
                        steps.append(f"Error: {str(e)}")
            except Exception as e:
                steps.append(f"Error: {str(e)}")

        self.show_step_window("Test Results", steps)

    def copy_result_to_clipboard(self):
        """Copy the result to the clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.result_var.get())
        self.root.update()  # Keeps clipboard after window closes

    def toggle_theme(self):
        if self.colors["background"] == "#121629":
            # Switch to light theme
            self.colors.update({
                "primary": "#f5f5f5",
                "secondary": "#232946",
                "text": "#232946",
                "accent": "#eebbc3",
                "background": "#ffffff",
                "highlight": "#ff8906",
            })
        else:
            # Switch to dark theme
            self.colors.update({
                "primary": "#232946",
                "secondary": "#eebbc3",
                "text": "#fffffe",
                "accent": "#b8c1ec",
                "background": "#121629",
                "highlight": "#ff8906",
            })
        self.configure_styles()
        self.create_widgets()

    def create_symbol_buttons(self, parent):
        """Create quick-insert buttons for math/UML symbols"""
        symbols = [
            ('+', '-'), ('*', '/'), ('[', ']'), ('{', '}'), ('<', '>'), ('@', '('), (')', ',')
        ]
        for row, pair in enumerate(symbols):
            for col, symbol in enumerate(pair):
                btn = tk.Button(
                    parent,
                    text=symbol,
                    font=(self.main_font, 12),
                    width=3,
                    bg=self.colors["accent"],
                    fg=self.colors["primary"],
                    relief="flat",
                    command=lambda s=symbol: self.insert_symbol(s)
                )
                btn.grid(row=row, column=col, padx=2, pady=2)

    def insert_symbol(self, symbol):
        """Insert a symbol into the current expression"""
        self.input_entry.insert(tk.INSERT, symbol)

    def open_settings(self):
        """Open the settings/preferences dialog"""
        settings = tk.Toplevel(self.root)
        settings.title("Settings & Preferences")
        settings.geometry("400x400")
        settings.configure(bg=self.colors["background"])

        # Default Mode
        tk.Label(settings, text="Default Mode:", bg=self.colors["background"], fg=self.colors["text"], font=(self.main_font, 12)).pack(pady=5)
        mode_var = tk.StringVar(value=self.mode_var.get())
        for text, mode in [("UML", "uml"), ("Standard", "standard"), ("RIS", "ris")]:
            tk.Radiobutton(settings, text=text, variable=mode_var, value=mode, bg=self.colors["background"], fg=self.colors["text"], selectcolor=self.colors["accent"], font=(self.main_font, 11)).pack(anchor="w", padx=20)

        # Font Family
        tk.Label(settings, text="Font Family:", bg=self.colors["background"], fg=self.colors["text"], font=(self.main_font, 12)).pack(pady=5)
        font_families = sorted(font.families())
        font_family_var = tk.StringVar(value=self.main_font if isinstance(self.main_font, str) else self.main_font[0])
        font_menu = tk.OptionMenu(settings, font_family_var, *font_families)
        font_menu.config(bg=self.colors["accent"], fg=self.colors["primary"])
        font_menu.pack(fill="x", padx=20)

        # Font Size
        tk.Label(settings, text="Font Size:", bg=self.colors["background"], fg=self.colors["text"], font=(self.main_font, 12)).pack(pady=5)
        font_size_var = tk.IntVar(value=16)
        tk.Scale(settings, from_=10, to=32, orient="horizontal", variable=font_size_var, bg=self.colors["background"], fg=self.colors["text"], troughcolor=self.colors["accent"]).pack(fill="x", padx=20)

        # Theme
        tk.Label(settings, text="Theme:", bg=self.colors["background"], fg=self.colors["text"], font=(self.main_font, 12)).pack(pady=5)
        theme_var = tk.StringVar(value="dark" if self.colors["background"] == "#121629" else "light")
        for text, val in [("Dark", "dark"), ("Light", "light")]:
            tk.Radiobutton(settings, text=text, variable=theme_var, value=val, bg=self.colors["background"], fg=self.colors["text"], selectcolor=self.colors["accent"], font=(self.main_font, 11)).pack(anchor="w", padx=20)

        # Show Steps by Default
        show_steps_var = tk.BooleanVar(value=getattr(self, 'show_steps_default', True))
        tk.Checkbutton(settings, text="Show Steps by Default", variable=show_steps_var, bg=self.colors["background"], fg=self.colors["text"], selectcolor=self.colors["accent"], font=(self.main_font, 11)).pack(anchor="w", padx=20, pady=5)

        # History Length
        tk.Label(settings, text="History Length:", bg=self.colors["background"], fg=self.colors["text"], font=(self.main_font, 12)).pack(pady=5)
        history_length_var = tk.IntVar(value=getattr(self, 'history_length', 50))
        tk.Scale(settings, from_=10, to=200, orient="horizontal", variable=history_length_var, bg=self.colors["background"], fg=self.colors["text"], troughcolor=self.colors["accent"]).pack(fill="x", padx=20)

        # Sound/Notification Toggle
        sound_var = tk.BooleanVar(value=getattr(self, 'sound_enabled', False))
        tk.Checkbutton(settings, text="Enable Sound/Notifications", variable=sound_var, bg=self.colors["background"], fg=self.colors["text"], selectcolor=self.colors["accent"], font=(self.main_font, 11)).pack(anchor="w", padx=20, pady=5)

        def save_settings():
            self.mode_var.set(mode_var.get())
            self.main_font = font_family_var.get()
            self.font_size = font_size_var.get()
            self.show_steps_default = show_steps_var.get()
            self.history_length = history_length_var.get()
            self.sound_enabled = sound_var.get()
            if theme_var.get() == "dark":
                self.colors.update({
                    "primary": "#232946",
                    "secondary": "#eebbc3",
                    "text": "#fffffe",
                    "accent": "#b8c1ec",
                    "background": "#121629",
                    "highlight": "#ff8906",
                })
            else:
                self.colors.update({
                    "primary": "#f5f5f5",
                    "secondary": "#232946",
                    "text": "#232946",
                    "accent": "#eebbc3",
                    "background": "#ffffff",
                    "highlight": "#ff8906",
                })
            self.configure_styles()
            self.create_widgets()
            self.save_user_settings()
            settings.destroy()

        tk.Button(settings, text="Save", command=save_settings, bg=self.colors["accent"], fg=self.colors["primary"], font=(self.main_font, 11)).pack(pady=20)

    def open_about(self):
        """Open the About dialog"""
        about = tk.Toplevel(self.root)
        about.title("About UML Calculator")
        about.geometry("400x250")
        about.configure(bg=self.colors["background"])

        tk.Label(
            about,
            text="UML Calculator V1",
            font=(self.main_font, 16, "bold"),
            bg=self.colors["background"],
            fg=self.colors["secondary"],
        ).pack(pady=10)

        tk.Label(
            about,
            text="Universal Mathematical Language Calculator\nT.R.E.E.S. Ready\n\nCreated by Travis Miner & Team\n2023-2025\n\nFor help, see the Quick Guide panel.",
            font=(self.main_font, 12),
            bg=self.colors["background"],
            fg=self.colors["text"],
            justify="left",
        ).pack(pady=10)

        tk.Button(
            about,
            text="Close",
            command=about.destroy,
            bg=self.colors["accent"],
            fg=self.colors["primary"],
            font=(self.main_font, 11),
        ).pack(pady=10)

    def save_user_settings(self):
        settings = {
            "mode": self.mode_var.get(),
            "main_font": self.main_font if isinstance(self.main_font, str) else self.main_font[0],
            "font_size": getattr(self, 'font_size', 16),
            "theme": "dark" if self.colors["background"] == "#121629" else "light",
            "show_steps_default": getattr(self, 'show_steps_default', True),
            "history_length": getattr(self, 'history_length', 50),
            "sound_enabled": getattr(self, 'sound_enabled', False),
            "history": self.history[-getattr(self, 'history_length', 50):],
        }
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f)

    def load_user_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                settings = json.load(f)
            self.mode_var.set(settings.get("mode", "uml"))
            self.main_font = settings.get("main_font", self.main_font)
            self.font_size = settings.get("font_size", 16)
            if settings.get("theme", "dark") == "dark":
                self.colors.update({
                    "primary": "#232946",
                    "secondary": "#eebbc3",
                    "text": "#fffffe",
                    "accent": "#b8c1ec",
                    "background": "#121629",
                    "highlight": "#ff8906",
                })
            else:
                self.colors.update({
                    "primary": "#f5f5f5",
                    "secondary": "#232946",
                    "text": "#232946",
                    "accent": "#eebbc3",
                    "background": "#ffffff",
                    "highlight": "#ff8906",
                })
            self.show_steps_default = settings.get("show_steps_default", True)
            self.history_length = settings.get("history_length", 50)
            self.sound_enabled = settings.get("sound_enabled", False)
            self.history = settings.get("history", [])
            self.update_history_display()

def save_settings(settings: dict):
    SETTINGS_FILE = os.path.join(os.path.expanduser("~"), ".uml_calculator_settings.json")
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

def load_settings() -> dict:
    SETTINGS_FILE = os.path.join(os.path.expanduser("~"), ".uml_calculator_settings.json")
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_history(history: list):
    HISTORY_FILE = os.path.join(os.path.expanduser("~"), ".uml_calculator_history.json")
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

def load_history() -> list:
    HISTORY_FILE = os.path.join(os.path.expanduser("~"), ".uml_calculator_history.json")
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def main():
    """Main entry point for the UML Calculator GUI"""
    app = UMLCalculatorGUI()
    app.root.mainloop()


if __name__ == "__main__":
    main()
