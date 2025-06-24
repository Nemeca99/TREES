"""
Data visualization tools for UML Calculator
"""
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from rich.console import Console
import tempfile
import os

def create_plot(x_values, y_values, title="RIS Function", terminal_mode=True):
    """
    Create a plot from x,y data
    
    Args:
        x_values: Array of x values
        y_values: Array of y values
        title: Title for the plot
        terminal_mode: If True, returns ASCII art plot; otherwise returns plot file path
        
    Returns:
        ASCII representation or path to image file
    """
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_values)
    plt.title(title)
    plt.grid(True)
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    
    if terminal_mode:
        # Generate ASCII art plot for terminal
        import shutil
        term_width, term_height = shutil.get_terminal_size()
        
        # If terminal is very small, provide warning instead of plot
        if term_width < 60 or term_height < 20:
            return "Terminal too small for plot. Resize or use --save-plot option."
            
        # Create ASCII art
        from art import text2art
        ascii_plot = text2art("RIS PLOT")
        
        # Add basic plot representation
        plot_height = min(term_height - 10, 20)
        plot_width = term_width - 10
        
        # Normalize y values to fit in terminal
        valid_indices = ~np.isnan(y_values)
        if not np.any(valid_indices):
            return "Cannot create plot: No valid data points"
        
        y_valid = y_values[valid_indices]
        y_min, y_max = np.min(y_valid), np.max(y_valid)
        if y_min == y_max:
            # Handle flat plots
            y_normalized = np.zeros_like(y_values)
            y_normalized[valid_indices] = plot_height // 2
        else:
            y_normalized = np.full_like(y_values, float('nan'))
            y_normalized[valid_indices] = (y_valid - y_min) / (y_max - y_min) * plot_height
        
        # Resample to fit width
        indices = np.linspace(0, len(x_values)-1, plot_width).astype(int)
        y_sample = y_normalized[indices]
        
        # Create ASCII plot
        canvas = [[' ' for _ in range(plot_width)] for _ in range(plot_height)]
        for i, y in enumerate(y_sample):
            if not np.isnan(y):
                y_pos = plot_height - 1 - int(y)
                if 0 <= y_pos < plot_height:
                    canvas[y_pos][i] = '*'
        
        # Add axis
        zero_line = int(plot_height * (0 - y_min) / (y_max - y_min)) if y_min < 0 < y_max else None
        if zero_line is not None and 0 <= zero_line < plot_height:
            for i in range(plot_width):
                if canvas[zero_line][i] == ' ':
                    canvas[zero_line][i] = '-'
        
        # Convert to string
        plot_str = '\n'.join([''.join(row) for row in canvas])
        
        # Add scale indicators
        plot_info = f"y=[{y_min:.2f}, {y_max:.2f}], x=[{x_values[0]:.2f}, {x_values[-1]:.2f}]"
        
        return f"{ascii_plot}\n{plot_str}\n{plot_info}"
    
    else:
        # Save plot to temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        plt.savefig(temp_file.name)
        plt.close()
        return temp_file.name

def plot_function(expr_func, x_min=-10, x_max=10, points=100, title=None):
    """
    Plot a function across a range of x values
    
    Args:
        expr_func: Function that takes x value and returns y
        x_min, x_max: Range for x values
        points: Number of points to calculate
        title: Title for the plot
        
    Returns:
        Plot visualization
    """
    x_values = np.linspace(x_min, x_max, points)
    y_values = np.array([expr_func(x) for x in x_values])
    
    if title is None:
        title = "Function Plot"
    
    return create_plot(x_values, y_values, title)
