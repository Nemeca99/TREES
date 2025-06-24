"""
Modern CLI for UML Calculator using Rich and Typer
Provides beautiful formatting, easy command handling, and UML diagram generation
"""
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.theme import Theme
import json
import csv
import datetime
import sys
import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
from pathlib import Path

# Add path to core modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.ris import ris, ris_explain
from core.symbolic import evaluate_expression, generate_plot_data, solve_equation
from core.visualization import create_plot
try:
    from core.uml_generator import UMLGenerator
    UML_GENERATOR = UMLGenerator()
    UML_AVAILABLE = True
except ImportError:
    UML_AVAILABLE = False

# Define UML Calculator theme
UML_THEMES = {
    "default": {
        "info": "blue",
        "warning": "yellow",
        "danger": "red bold",
        "success": "green",
        "title": "blue bold",
        "heading": "cyan bold",
        "key": "magenta",
        "value": "green",
        "ris_op": "bright_green",
        "ris_result": "bright_cyan"
    },
    "dark": {
        "info": "cyan",
        "warning": "yellow",
        "danger": "red bold",
        "success": "green",
        "title": "cyan bold",
        "heading": "bright_blue bold",
        "key": "bright_magenta",
        "value": "bright_green",
        "ris_op": "bright_green",
        "ris_result": "bright_cyan"
    },
    "light": {
        "info": "dark_blue",
        "warning": "dark_orange",
        "danger": "dark_red bold",
        "success": "dark_green",
        "title": "dark_blue bold",
        "heading": "dark_cyan bold",
        "key": "purple",
        "value": "dark_green",
        "ris_op": "green",
        "ris_result": "blue"
    }
}

# Initialize rich console with theme
console = Console(theme=Theme(UML_THEMES["default"]))
app = typer.Typer(help="UML Calculator: Math and RIS Operations")

# Global settings
SETTINGS_FILE = Path(os.path.expanduser("~")) / ".uml_calculator_settings.json"
SETTINGS = {
    "theme": "default",
    "history_size": 100,
    "precision": 4,
    "plot_points": 100,
    "show_welcome": True,
    "default_mode": "standard",  # standard or ris
}

# Setup history tracking
HISTORY_FILE = Path(os.path.expanduser("~")) / ".uml_calculator_history.json"
calculation_history = []

def load_settings():
    """Load user settings"""
    global SETTINGS
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r") as f:
                loaded = json.load(f)
                # Update settings with loaded values
                SETTINGS.update(loaded)
        except Exception as e:
            console.print(f"[warning]Warning: Could not load settings: {e}[/warning]")
    
    # Apply theme
    console.theme = Theme(UML_THEMES.get(SETTINGS["theme"], UML_THEMES["default"]))

def save_settings():
    """Save user settings"""
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(SETTINGS, f, indent=2)
    except Exception as e:
        console.print(f"[warning]Warning: Could not save settings: {e}[/warning]")

def load_history():
    """Load calculation history from file"""
    global calculation_history
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r") as f:
                calculation_history = json.load(f)
        except Exception as e:
            console.print(f"[warning]Warning: Could not load history: {e}[/warning]")

def save_history():
    """Save calculation history to file"""
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(calculation_history, f, indent=2)
    except Exception as e:
        console.print(f"[warning]Warning: Could not save history: {e}[/warning]")

def add_to_history(entry_type, data):
    """Add calculation to history"""
    history_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "type": entry_type,
        "data": data
    }
    calculation_history.append(history_entry)
    if len(calculation_history) > SETTINGS["history_size"]:
        calculation_history.pop(0)
    save_history()

@app.command("calc")
def calculate(
    expression: str = typer.Argument(..., help="Math expression (e.g. '2+2' or 'RIS(6,3)')"),
    x: float = typer.Option(None, help="Value for x in expressions like '3*x^2'"),
    mode: str = typer.Option(None, help="Mode: standard (normal math) or ris (RIS logic)"),
    explain: bool = typer.Option(False, "--explain", "-e", help="Show detailed explanation for RIS"),
):
    """Calculate any mathematical expression, with RIS support"""
    try:
        # Determine mode
        calc_mode = mode if mode else SETTINGS["default_mode"]
        standard_mode = calc_mode.lower() != "ris"
            
        # Check if it's a simple RIS call
        if expression.upper().startswith("RIS(") and ")" in expression and len(expression.split(")")) == 2:
            # Parse the RIS arguments
            args = expression.upper().replace("RIS(", "").split(")")[0].split(",")
            if len(args) >= 2:
                try:
                    a = float(args[0].strip())
                    b = float(args[1].strip())
                    ris_mode = args[2].strip() if len(args) > 2 else "default"
                    
                    context = {"ris_mode": ris_mode} if ris_mode != "default" else {}
                    
                    if explain:
                        result, explanation = ris_explain(a, b, context)
                        console.print(Panel.fit(
                            f"[ris_op]RIS({a}, {b})[/ris_op] = [ris_result]{result}[/ris_result]\n\n[value]{explanation}[/value]",
                            title="RIS Result",
                            border_style="info"
                        ))
                        add_to_history("ris", {
                            "a": a,
                            "b": b,
                            "result": result,
                            "mode": ris_mode,
                            "explanation": explanation
                        })
                        return result
                    else:
                        result = ris(a, b, context)
                        console.print(Panel.fit(
                            f"[ris_op]RIS({a}, {b})[/ris_op] = [ris_result]{result}[/ris_result]",
                            title="RIS Result", 
                            border_style="info"
                        ))
                        add_to_history("ris", {
                            "a": a,
                            "b": b,
                            "result": result,
                            "mode": ris_mode
                        })
                        return result
                except:
                    # If any issues parsing as direct RIS call, fall back to expression evaluation
                    pass
        
        # Evaluate as a general expression
        try:
            if "=" in expression:
                result = solve_equation(
                    expression.split("=")[0].strip(), 
                    expression.split("=")[1].strip() if len(expression.split("=")) > 1 and expression.split("=")[1].strip() else "0",
                    x
                )
                
                if x is not None:
                    # Evaluating with specific x
                    console.print(Panel.fit(
                        f"Expression: [ris_op]{expression}[/ris_op] with x={x}\n" 
                        f"Left side: [ris_result]{result['left_value']}[/ris_result]\n"
                        f"Right side: [ris_result]{result['right_value']}[/ris_result]\n"
                        f"Equal: [ris_result]{result['equal']}[/ris_result]",
                        title="Equation Evaluation",
                        border_style="info"
                    ))
                else:
                    # Solving for x
                    solutions = result['solutions']
                    if not solutions:
                        console.print(Panel.fit(
                            f"Equation: [ris_op]{result['equation']}[/ris_op]\n"
                            f"No solutions found.",
                            title="Equation Solution",
                            border_style="info"
                        ))
                    else:
                        solution_text = "\n".join([f"x = [ris_result]{sol}[/ris_result]" for sol in solutions])
                        console.print(Panel.fit(
                            f"Equation: [ris_op]{result['equation']}[/ris_op]\n\n"
                            f"{solution_text}",
                            title="Equation Solution",
                            border_style="info"
                        ))
            else:
                # Simple expression
                result = evaluate_expression(expression, x_value=x, standard_mode=standard_mode)
                
                if x is not None:
                    console.print(Panel.fit(
                        f"Expression: [ris_op]{expression}[/ris_op] with x={x}\n"
                        f"Result: [ris_result]{result}[/ris_result]",
                        title="Expression Evaluation",
                        border_style="info"
                    ))
                else:
                    console.print(Panel.fit(
                        f"[ris_op]{expression}[/ris_op] = [ris_result]{result}[/ris_result]",
                        title="Calculation Result",
                        border_style="info"
                    ))
            
            # Add to history
            add_to_history("expression", {
                "expression": expression,
                "x_value": x,
                "mode": calc_mode,
                "result": str(result)
            })
                
            return result
        except Exception as e:
            console.print(f"[danger]Error evaluating expression:[/danger] {str(e)}")
            return None
            
    except Exception as e:
        console.print(f"[danger]Error:[/danger] {str(e)}")
        return None

@app.command("plot")
def plot_expression(
    expression: str = typer.Argument(..., help="Expression to plot (e.g., '3*x^2' or 'RIS(x,2)')"),
    x_min: float = typer.Option(-10.0, "--min", help="Minimum x value"),
    x_max: float = typer.Option(10.0, "--max", help="Maximum x value"),
    points: int = typer.Option(100, "--points", "-p", help="Number of points to calculate"),
    mode: str = typer.Option(None, help="Mode: standard (normal math) or ris (RIS logic)"),
    save: str = typer.Option(None, "--save", help="Save plot to file"),
    no_history: bool = typer.Option(False, "--no-history", help="Don't add to calculation history"),
):
    """Plot a mathematical expression or function"""
    try:
        # Determine mode
        calc_mode = mode if mode else SETTINGS["default_mode"]
        standard_mode = calc_mode.lower() != "ris"
        
        # Generate plot data
        x_values, y_values = generate_plot_data(expression, x_min, x_max, points, standard_mode=standard_mode)
        
        # Create plot
        title = f"Plot of {expression}"
        
        if save:
            plot_file = create_plot(x_values, y_values, title=title, terminal_mode=False)
            import shutil
            shutil.move(plot_file, save)
            console.print(f"[success]Plot saved to {save}[/success]")
        else:
            plot_output = create_plot(x_values, y_values, title=title, terminal_mode=True)
            console.print(plot_output)
        
        if not no_history:
            add_to_history("plot", {
                "expression": expression,
                "x_min": x_min,
                "x_max": x_max,
                "mode": calc_mode,
                "save_path": save
            })
            
        return True
    except Exception as e:
        console.print(f"[danger]Error plotting expression:[/danger] {str(e)}")
        return False

@app.command("ris")
def ris_calc(
    a: float = typer.Argument(..., help="First operand"),
    b: float = typer.Argument(..., help="Second operand"),
    mode: str = typer.Option("default", help="RIS mode: default, always_multiply, always_divide"),
    explain: bool = typer.Option(False, "--explain", "-e", help="Show detailed explanation"),
    no_history: bool = typer.Option(False, "--no-history", help="Don't add to calculation history"),
):
    """Perform a direct RIS calculation with detailed options"""
    try:
        context = {"ris_mode": mode} if mode != "default" else {}
        
        if explain:
            result, explanation = ris_explain(a, b, context)
            console.print(Panel.fit(
                f"[ris_op]RIS({a}, {b})[/ris_op] = [ris_result]{result}[/ris_result]\n\n[value]{explanation}[/value]",
                title="UML Calculator RIS Result",
                border_style="info"
            ))
            if not no_history:
                add_to_history("ris", {
                    "a": a,
                    "b": b,
                    "result": result,
                    "mode": mode,
                    "explanation": explanation
                })
        else:
            result = ris(a, b, context)
            console.print(Panel.fit(
                f"[ris_op]RIS({a}, {b})[/ris_op] = [ris_result]{result}[/ris_result]",
                title="UML Calculator RIS Result", 
                border_style="info"
            ))
            if not no_history:
                add_to_history("ris", {
                    "a": a,
                    "b": b,
                    "result": result,
                    "mode": mode
                })
        
        return result
    except Exception as e:
        console.print(f"[danger]Error:[/danger] {str(e)}")
        return None

@app.command("history")
def show_history(
    limit: int = typer.Option(10, help="Limit number of history items shown"),
    clear: bool = typer.Option(False, help="Clear history")
):
    """Show calculation history"""
    global calculation_history
    
    if clear:
        if Confirm.ask("Are you sure you want to clear calculation history?"):
            calculation_history = []
            save_history()
            console.print("[success]History cleared.[/success]")
        return

    if not calculation_history:
        console.print("[warning]No calculation history found.[/warning]")
        return

    table = Table(title=f"Calculation History (Last {min(limit, len(calculation_history))} entries)")
    table.add_column("Time", style="key")
    table.add_column("Type", style="info")
    table.add_column("Input", style="ris_op")
    table.add_column("Result", style="ris_result")
    
    for entry in calculation_history[-limit:]:
        timestamp = datetime.datetime.fromisoformat(entry["timestamp"]).strftime("%Y-%m-%d %H:%M")
        entry_type = entry["type"]
        data = entry["data"]
        
        if entry_type == "ris":
            input_str = f"RIS({data['a']}, {data['b']})"
            result_str = str(data["result"])
        elif entry_type == "expression":
            input_str = data["expression"]
            result_str = data["result"]
        elif entry_type == "plot":
            input_str = data["expression"]
            result_str = f"Plot [{data['x_min']} to {data['x_max']}]"
        else:
            input_str = str(data)
            result_str = "N/A"
            
        table.add_row(timestamp, entry_type, input_str, result_str)
    
    console.print(table)

@app.command("batch")
def batch_process(
    input_file: str = typer.Argument(..., help="CSV file with operations"),
    output_file: str = typer.Option(None, help="Output file for results (CSV)"),
    explain: bool = typer.Option(False, help="Include explanations in output")
):
    """Process batch calculations from a file"""
    try:
        results = []
        
        with open(input_file, 'r') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                try:
                    if len(row) < 2:
                        console.print(f"[warning]Warning: Row {i+1} has insufficient values, skipping.[/warning]")
                        continue
                        
                    a = float(row[0])
                    b = float(row[1])
                    mode = row[2] if len(row) > 2 else "default"
                    
                    context = {"ris_mode": mode} if mode != "default" else {}
                    
                    if explain:
                        result, explanation = ris_explain(a, b, context)
                        results.append([a, b, result, mode, explanation])
                    else:
                        result = ris(a, b, context)
                        results.append([a, b, result, mode])
                    
                    console.print(f"[success]Processed:[/success] RIS({a}, {b}) = {result} [{mode}]")
                except Exception as e:
                    console.print(f"[danger]Error in row {i+1}:[/danger] {str(e)}")
        
        if output_file:
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                if explain:
                    writer.writerow(["a", "b", "result", "mode", "explanation"])
                else:
                    writer.writerow(["a", "b", "result", "mode"])
                writer.writerows(results)
            console.print(f"[success]Results saved to {output_file}[/success]")
        
        # Show summary
        console.print(f"[heading]Batch processing complete.[/heading] Processed {len(results)} calculations.")
    except Exception as e:
        console.print(f"[danger]Batch processing failed:[/danger] {str(e)}")

@app.command("export")
def export_history(
    output_file: str = typer.Argument(..., help="Export file path (JSON or CSV)"),
    format: str = typer.Option("csv", help="Export format (csv or json)")
):
    """Export calculation history to a file"""
    if not calculation_history:
        console.print("[warning]No calculation history to export.[/warning]")
        return
    
    try:
        if format.lower() == 'json':
            with open(output_file, 'w') as f:
                json.dump(calculation_history, f, indent=2)
        elif format.lower() == 'csv':
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "type", "input", "result"])
                for entry in calculation_history:
                    timestamp = entry["timestamp"]
                    entry_type = entry["type"]
                    data = entry["data"]
                    
                    if entry_type == "ris":
                        input_str = f"RIS({data['a']}, {data['b']})"
                        result_str = str(data["result"])
                    elif entry_type == "expression":
                        input_str = data["expression"]
                        result_str = data["result"]
                    elif entry_type == "plot":
                        input_str = data["expression"]
                        result_str = f"Plot [{data['x_min']} to {data['x_max']}]"
                    else:
                        input_str = str(data)
                        result_str = "N/A"
                        
                    writer.writerow([timestamp, entry_type, input_str, result_str])
        else:
            console.print("[danger]Unsupported format. Use 'csv' or 'json'.[/danger]")
            return
        
        console.print(f"[success]History exported to {output_file}[/success]")
    except Exception as e:
        console.print(f"[danger]Export failed:[/danger] {str(e)}")

@app.command("settings")
def configure_settings(
    theme: str = typer.Option(None, help="UI theme (default, dark, light)"),
    history_size: int = typer.Option(None, help="Maximum history entries to keep"),
    precision: int = typer.Option(None, help="Decimal precision for results"),
    plot_points: int = typer.Option(None, help="Default number of points for plots"),
    show_welcome: bool = typer.Option(None, help="Show welcome message on startup"),
    default_mode: str = typer.Option(None, help="Default calculation mode (standard or ris)"),
    reset: bool = typer.Option(False, help="Reset all settings to defaults"),
):
    """Configure calculator settings"""
    global SETTINGS
    
    # Load current settings
    load_settings()
    
    if reset:
        if Confirm.ask("Are you sure you want to reset all settings to defaults?"):
            SETTINGS = {
                "theme": "default",
                "history_size": 100,
                "precision": 4,
                "plot_points": 100,
                "show_welcome": True,
                "default_mode": "standard"
            }
            save_settings()
            console.print("[success]Settings reset to defaults.[/success]")
            # Apply theme
            console.theme = Theme(UML_THEMES.get(SETTINGS["theme"], UML_THEMES["default"]))
            return
    
    # Update settings with provided values
    updated = False
    if theme is not None:
        if theme in UML_THEMES:
            SETTINGS["theme"] = theme
            console.theme = Theme(UML_THEMES.get(theme, UML_THEMES["default"]))
            updated = True
        else:
            console.print(f"[danger]Invalid theme: {theme}. Available themes: {', '.join(UML_THEMES.keys())}[/danger]")
    
    if history_size is not None and history_size > 0:
        SETTINGS["history_size"] = history_size
        updated = True
    
    if precision is not None and precision >= 0:
        SETTINGS["precision"] = precision
        updated = True
    
    if plot_points is not None and plot_points > 10:
        SETTINGS["plot_points"] = plot_points
        updated = True
    
    if show_welcome is not None:
        SETTINGS["show_welcome"] = show_welcome
        updated = True
        
    if default_mode is not None:
        if default_mode.lower() in ["standard", "ris"]:
            SETTINGS["default_mode"] = default_mode.lower()
            updated = True
        else:
            console.print(f"[danger]Invalid mode: {default_mode}. Available modes: standard, ris[/danger]")
    
    if updated:
        save_settings()
        console.print("[success]Settings updated.[/success]")
    
    # Display current settings
    table = Table(title="Current Settings")
    table.add_column("Setting", style="key")
    table.add_column("Value", style="value")
    
    for key, value in SETTINGS.items():
        table.add_row(key, str(value))
    
    console.print(table)

@app.command("table")
def truth_table():
    """Display the RIS truth table"""
    table = Table(title="RIS Truth Table")
    table.add_column("a", style="key")
    table.add_column("b", style="key")
    table.add_column("Condition", style="info")
    table.add_column("Result", style="ris_result")
    table.add_column("Rule", style="ris_op")
    
    # Add rows based on the RIS truth table
    table.add_row("6", "3", "a > b, special case", "18 (×)", "Multiplication (Special)")
    table.add_row("8", "2", "a % b = 0, a/b < a, b", "4 (÷)", "Division (Compact)")
    table.add_row("0", "5", "a or b = 0", "5 (+)", "Addition (Zero)")
    table.add_row("5", "5", "Equal", "25 (×)", "Multiplication (Equal)")
    table.add_row("9", "3", "a % b = 0, a/b < a, b", "3 (÷)", "Division (Compact)")
    
    console.print(table)

@app.command("uml")
def generate_uml(
    type: str = typer.Argument(..., help="Type of UML: ris, function, equation, rules"),
    expression: str = typer.Option(None, help="Expression for function or equation UML"),
    a: float = typer.Option(None, help="First operand for RIS UML"),
    b: float = typer.Option(None, help="Second operand for RIS UML"),
    output: str = typer.Option(None, help="Output file path (SVG or PNG)"),
    format: str = typer.Option("png", help="Output format (svg or png)"),
):
    """Generate UML diagrams for math operations and RIS logic"""
    if not UML_AVAILABLE:
        console.print("[danger]UML generation requires pydot, graphviz and plantuml packages.[/danger]")
        console.print("[info]Install them with: pip install pydot graphviz plantuml[/info]")
        return False
        
    try:
        type = type.lower()
        
        # Determine output file if not specified
        if not output:
            output = f"uml_{type}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
            
        # Generate appropriate UML based on type
        if type == "ris":
            if a is None or b is None:
                console.print("[danger]Please provide a and b values for RIS UML diagram.[/danger]")
                return False
                
            context = {}
            result = ris(a, b, context)
            _, explanation = ris_explain(a, b, context)
            
            # Determine operation symbol
            operation = "×"
            if "Addition" in explanation:
                operation = "+"
            elif "Division" in explanation:
                operation = "÷"
                
            puml = UML_GENERATOR.generate_ris_diagram(a, b, result, operation, explanation)
            diagram_file = UML_GENERATOR.render_plantuml(puml, output_file=output, format=format)
            
            console.print(f"[success]Generated RIS UML diagram for RIS({a}, {b})[/success]")
            console.print(f"[info]Saved to: {diagram_file}[/info]")
            
            # Add to history
            add_to_history("uml", {
                "type": "ris",
                "a": a,
                "b": b,
                "result": result,
                "file": diagram_file
            })
            
        elif type == "function":
            if not expression:
                console.print("[danger]Please provide an expression for function UML diagram.[/danger]")
                return False
                
            # Parse variables if present
            variables = {}
            if "=" in expression and "," in expression.split("=")[0]:
                # Format like "f(x,y) = x^2 + y"
                parts = expression.split("=", 1)
                func_decl = parts[0].strip()
                expr = parts[1].strip()
                
                # Extract variables from function declaration
                var_part = func_decl[func_decl.find("(")+1:func_decl.find(")")]
                var_list = [v.strip() for v in var_part.split(",")]
                for v in var_list:
                    variables[v] = 'x'  # Symbolic variable
            else:
                # Just the expression
                expr = expression
                variables = {'x': 'x'}  # Default to x
                
            puml = UML_GENERATOR.generate_function_diagram(expr, variables)
            diagram_file = UML_GENERATOR.render_plantuml(puml, output_file=output, format=format)
            
            console.print(f"[success]Generated function UML diagram for: {expression}[/success]")
            console.print(f"[info]Saved to: {diagram_file}[/info]")
            
            # Add to history
            add_to_history("uml", {
                "type": "function",
                "expression": expression,
                "file": diagram_file
            })
            
        elif type == "equation":
            if not expression:
                console.print("[danger]Please provide an equation for equation UML diagram.[/danger]")
                return False
                
            # Split into left and right side
            if "=" in expression:
                left, right = expression.split("=", 1)
                left = left.strip()
                right = right.strip()
            else:
                left = expression
                right = "0"
                
            # Try to solve
            try:
                solution = solve_equation(left, right, None)
                solutions = solution.get("solutions", None)
            except:
                solutions = None
                
            puml = UML_GENERATOR.generate_equation_diagram(left, right, solutions)
            diagram_file = UML_GENERATOR.render_plantuml(puml, output_file=output, format=format)
            
            console.print(f"[success]Generated equation UML diagram for: {expression}[/success]")
            console.print(f"[info]Saved to: {diagram_file}[/info]")
            
            # Add to history
            add_to_history("uml", {
                "type": "equation",
                "expression": expression,
                "solutions": solutions,
                "file": diagram_file
            })
            
        elif type == "rules":
            puml = UML_GENERATOR.generate_ris_rules_diagram()
            diagram_file = UML_GENERATOR.render_plantuml(puml, output_file=output, format=format)
            
            console.print(f"[success]Generated RIS rules UML diagram[/success]")
            console.print(f"[info]Saved to: {diagram_file}[/info]")
            
            # Add to history
            add_to_history("uml", {
                "type": "rules",
                "file": diagram_file
            })
            
        else:
            console.print(f"[danger]Unknown UML type: {type}[/danger]")
            console.print("[info]Valid types: ris, function, equation, rules[/info]")
            return False
            
        return True
    except Exception as e:
        console.print(f"[danger]Error generating UML diagram:[/danger] {str(e)}")
        return False

@app.command("help")
def show_help():
    """Display help information about UML Calculator"""
    console.print(Panel.fit(
        "[heading]UML Calculator[/heading]\n\n"
        "A unified calculator with standard math, RIS operations, and UML generation.\n\n"
        "[title]Commands:[/title]\n"
        "  [key]calc[/key] - Calculate any expression (e.g., 'calc 2+2' or 'calc RIS(6,3)')\n"
        "  [key]plot[/key] - Plot mathematical expressions (e.g., 'plot 3*x^2')\n"
        "  [key]ris[/key] - Direct RIS calculation (e.g., 'ris 6 3')\n"
        "  [key]uml[/key] - Generate UML diagrams (e.g., 'uml ris --a 6 --b 3')\n"
        "  [key]examples[/key] - Show example calculations\n"
        "  [key]history[/key] - Show calculation history\n"
        "  [key]settings[/key] - Configure calculator settings\n"
        "  [key]help[/key] - Show this help information\n\n"
        "[title]Standard Math Examples:[/title]\n"
        "  calc '2 + 3*5'\n"
        "  calc '3*x^2 - 5*x + 2' --x 3\n"
        "  calc '3*x^2 - 5*x + 2 = 0'\n\n"
        "[title]UML Examples:[/title]\n"
        "  uml ris --a 6 --b 3\n"
        "  uml function --expression 'x^2 + 3*x'\n"
        "  uml equation --expression 'x^2 - 9 = 0'\n"
        "  uml rules",
        title="UML Calculator Help",
        border_style="success"
    ))

@app.command("examples")
def show_examples():
    """Show example calculations and RIS operations"""
    examples = [
        ("Standard Math", [
            "2 + 3*5", 
            "(10 - 5) / 2.5",
            "3^2 + 4^2",
            "2*x + 5 with x=3",
            "3*x^2 - 5*x + 2 = 0"
        ]),
        ("RIS Operations", [
            "RIS(6, 3)",
            "RIS(8, 2)",
            "RIS(5, 5)",
            "RIS(10, 5, always_multiply)",
            "RIS(10, 5, always_divide)"
        ]),
        ("UML Diagrams", [
            "RIS diagram for 6 and 3",
            "Function diagram for x^2 + 2*x",
            "Equation diagram for x^2 - 4 = 0",
            "RIS rules diagram"
        ]),
        ("Plotting", [
            "plot 3*x^2 - 5*x + 2",
            "plot RIS(x, 3)",
            "plot 'sin(x) + RIS(x, 2)'"
        ])
    ]
    
    for category, items in examples:
        table = Table(title=f"{category} Examples")
        table.add_column("Expression", style="ris_op")
        table.add_column("How to Run", style="value")
        
        for item in items:
            if category == "UML Diagrams":
                if "RIS diagram for" in item:
                    a, b = item.split("for ")[1].split(" and ")
                    table.add_row(item, f"uml ris --a {a} --b {b}")
                elif "Function diagram" in item:
                    expr = item.split("for ")[1]
                    table.add_row(item, f"uml function --expression '{expr}'")
                elif "Equation diagram" in item:
                    expr = item.split("for ")[1]
                    table.add_row(item, f"uml equation --expression '{expr}'")
                else:
                    table.add_row(item, "uml rules")
            elif "with" in item:
                expr, x_val = item.split("with")
                table.add_row(item, f"calc '{expr.strip()}' --x {x_val.strip()}")
            elif "=" in item and not item.startswith("plot"):
                table.add_row(item, f"calc '{item}'")
            elif item.startswith("plot"):
                # For plot examples
                _, expr = item.split(" ", 1)
                if "'" in expr:
                    expr = expr.strip("'")
                table.add_row(item, f"plot '{expr}'")
            else:
                table.add_row(item, f"calc '{item}'")
        
        console.print(table)
        console.print()

def show_welcome_message():
    """Show a welcome message with calculator logo"""
    try:
        from art import text2art
        logo = text2art("UML CALCULATOR", font="small")
    except:
        logo = """
  _   _ __  __ _       ____    _    _     ____ _   _ _        _  _____ ___  ____  
 | | | |  \/  | |     / ___|  / \  | |   / ___| | | | |      / \|_   _/ _ \|  _ \ 
 | | | | |\/| | |    | |     / _ \ | |  | |   | | | | |     / _ \ | || | | | |_) |
 | |_| | |  | | |___ | |___ / ___ \| |__| |___| |_| | |___ / ___ \| || |_| |  _ < 
  \___/|_|  |_|_____(_)____/_/   \_\_____\____|\___/|_____/_/   \_\_| \___/|_| \_\\
        """
    
    console.print(Panel.fit(
        f"[title]{logo}[/title]\n\n"
        "[info]All-in-One Calculator: Math + RIS + UML Diagrams[/info]\n"
        "Type a command or 'help' for assistance.\n\n"
        "[key]Quick Examples:[/key]\n"
        "• Standard Math: [ris_op]calc '2 + 3*5'[/ris_op]\n"
        "• Equations: [ris_op]calc '3*x^2 - 5*x + 2 = 0'[/ris_op]\n"
        "• RIS Operation: [ris_op]calc 'RIS(6,3)'[/ris_op]\n"
        "• UML Diagram: [ris_op]uml ris --a 6 --b 3[/ris_op]\n\n"
        "Type [ris_op]examples[/ris_op] to see more usage examples.",
        title="UML Calculator",
        border_style="info"
    ))

def show_interactive_menu():
    """Show interactive menu for CLI mode"""
    options = [
        ("calc", "Calculate any math expression"),
        ("plot", "Plot a function or expression"),
        ("ris", "Perform direct RIS calculation"),
        ("uml", "Generate UML diagrams"),
        ("examples", "Show usage examples"),
        ("history", "Show calculation history"),
        ("settings", "Configure calculator settings"),
        ("help", "Show help information"),
        ("exit", "Exit the calculator")
    ]
    
    table = Table(show_header=False, box=None)
    table.add_column(style="key")
    table.add_column(style="value")
    
    for cmd, desc in options:
        if cmd == "uml" and not UML_AVAILABLE:
            # Skip UML option if not available
            continue
        table.add_row(f"[bold]{cmd}[/bold]", desc)
    
    console.print(table)

if __name__ == "__main__":
    # Load settings and history
    load_settings()
    load_history()
    
    # Show welcome banner if enabled
    if SETTINGS.get("show_welcome", True):
        show_welcome_message()
    
    if len(sys.argv) == 1:
        # If no arguments provided, show interactive prompt
        while True:
            try:
                console.print("\n")
                show_interactive_menu()
                console.print("[bold info]>>>[/bold info]", end=" ")
                cmd = input().strip().lower()
                
                if cmd == "exit":
                    console.print("[warning]Goodbye![/warning]")
                    break
                elif cmd == "calc":
                    expr = Prompt.ask("Enter expression")
                    x_val = None
                    if 'x' in expr.lower():
                        use_x = Confirm.ask("Expression contains 'x'. Set value for x?", default=True)
                        if use_x:
                            x_val = float(Prompt.ask("Value for x"))
                    
                    mode = Prompt.ask("Mode (standard/ris)", default=SETTINGS["default_mode"])
                    explain = SETTINGS["default_mode"] == "ris" and Confirm.ask("Show RIS explanation?", default=False)
                    
                    calculate(expr, x_val, mode, explain)
                elif cmd == "ris":
                    a = float(Prompt.ask("Enter first number"))
                    b = float(Prompt.ask("Enter second number"))
                    mode = Prompt.ask("Mode (default/always_multiply/always_divide)", default="default")
                    exp = Confirm.ask("Show explanation?", default=False)
                    
                    ris_calc(a, b, mode, exp)
                elif cmd == "plot":
                    expr = Prompt.ask("Enter expression to plot")
                    x_min = float(Prompt.ask("Minimum x value", default="-10"))
                    x_max = float(Prompt.ask("Maximum x value", default="10"))
                    points = int(Prompt.ask("Number of points", default=str(SETTINGS["plot_points"])))
                    mode = Prompt.ask("Mode (standard/ris)", default=SETTINGS["default_mode"])
                    save = Prompt.ask("Save to file (leave empty to display in terminal)", default="")
                    
                    plot_expression(expr, x_min, x_max, points, mode, save if save else None)
                elif cmd == "uml":
                    if not UML_AVAILABLE:
                        console.print("[danger]UML generation requires pydot, graphviz and plantuml packages.[/danger]")
                        console.print("[info]Install them with: pip install pydot graphviz plantuml[/info]")
                        continue
                    
                    uml_type = Prompt.ask("UML type", choices=["ris", "function", "equation", "rules"])
                    
                    if uml_type == "ris":
                        a = float(Prompt.ask("First number (a)"))
                        b = float(Prompt.ask("Second number (b)"))
                        output = Prompt.ask("Output file (leave empty for auto-naming)", default="")
                        generate_uml("ris", None, a, b, output if output else None)
                    elif uml_type == "function":
                        expr = Prompt.ask("Function expression")
                        output = Prompt.ask("Output file (leave empty for auto-naming)", default="")
                        generate_uml("function", expr, None, None, output if output else None)
                    elif uml_type == "equation":
                        expr = Prompt.ask("Equation (e.g., 'x^2 - 4 = 0')")
                        output = Prompt.ask("Output file (leave empty for auto-naming)", default="")
                        generate_uml("equation", expr, None, None, output if output else None)
                    elif uml_type == "rules":
                        output = Prompt.ask("Output file (leave empty for auto-naming)", default="")
                        generate_uml("rules", None, None, None, output if output else None)
                elif cmd == "examples":
                    show_examples()
                elif cmd == "history":
                    limit = int(Prompt.ask("Number of entries to show", default="10"))
                    show_history(limit)
                elif cmd == "settings":
                    print("\nCurrent settings:")
                    configure_settings()
                    
                    update = Confirm.ask("Update settings?", default=False)
                    if update:
                        theme = Prompt.ask("Theme (default/dark/light)", default=SETTINGS["theme"])
                        default_mode = Prompt.ask("Default calculation mode (standard/ris)", default=SETTINGS["default_mode"])
                        history_size = int(Prompt.ask("History size", default=str(SETTINGS["history_size"])))
                        precision = int(Prompt.ask("Decimal precision", default=str(SETTINGS["precision"])))
                        plot_points = int(Prompt.ask("Plot points", default=str(SETTINGS["plot_points"])))
                        show_welcome = Confirm.ask("Show welcome on startup?", default=SETTINGS["show_welcome"])
                        
                        configure_settings(theme, history_size, precision, plot_points, show_welcome, default_mode)
                elif cmd == "help":
                    show_help()
                elif cmd == "table":
                    truth_table()
                else:
                    console.print("[danger]Unknown command. Try calc, ris, plot, examples, history, settings, help, or exit.[/danger]")
            except KeyboardInterrupt:
                console.print("\n[warning]Interrupted. Type 'exit' to quit.[/warning]")
            except Exception as e:
                console.print(f"[danger]Error:[/danger] {str(e)}")
    else:
        # Otherwise use typer to parse command line arguments
        app()
