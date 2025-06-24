"""
TREES Web Demo Server

This Flask application serves as a simple web server for the TREES framework demo.
It provides API endpoints to calculate UML expressions, RIS operations, symbolic math,
and generate magic squares.

Author: @Nemeca99
"""

from flask import Flask, request, jsonify, send_from_directory
import os
import sys
import json

# Add the path to UML_Calculator
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'UML_Calculator'))

# Import UML modules (try/except for graceful fallback if modules aren't available)
try:
    from uml_core import parse_uml, eval_uml
    from symbolic_extensions import demo_symbolic_extensions
    UML_AVAILABLE = True
except ImportError:
    print("Warning: UML Calculator modules not found. Running in demo mode only.")
    UML_AVAILABLE = False

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    """Serve the main demo page"""
    return send_from_directory('.', 'index.html')

@app.route('/api/basic', methods=['POST'])
def calculate_basic():
    """Calculate basic UML expressions"""
    data = request.json
    expression = data.get('expression', '')
    
    if UML_AVAILABLE:
        try:
            # Use actual UML Calculator to evaluate the expression
            result = eval_uml(expression)
            return jsonify({"result": str(result), "success": True})
        except Exception as e:
            return jsonify({"result": f"Error: {str(e)}", "success": False})
    else:
        # Demo mode - return simulated results
        results = {
            "A5:B7+C3": "K15 (equivalent to 5 + 7 + 3 = 15)",
            "D8*E4": "P32 (equivalent to 8 × 4 = 32)",
            "F9:G3:H7": "T19 (composite operation result)"
        }
        return jsonify({"result": results.get(expression, "Demo mode: Cannot calculate custom expressions"), "success": True})

@app.route('/api/ris', methods=['POST'])
def calculate_ris():
    """Apply RIS meta-operators"""
    data = request.json
    expression = data.get('expression', '')
    
    if UML_AVAILABLE:
        try:
            # This would use the actual RIS implementation
            # For now just extracting the inner expression
            inner_expr = expression.replace("RIS(", "").replace(")", "")
            # This is a placeholder - actual implementation would use the RIS meta-operator
            result = f"RIS({inner_expr}) = Transformed result"
            return jsonify({"result": result, "success": True})
        except Exception as e:
            return jsonify({"result": f"Error: {str(e)}", "success": False})
    else:
        # Demo mode
        results = {
            "RIS(A5:B7)": "F12 (recursive identity expansion)",
            "RIS(C9*D4)": "M36 (recursive multiplication transform)",
            "RIS(E2:F8:G1)": "R11 (multi-level recursive transformation)"
        }
        return jsonify({"result": results.get(expression, "Demo mode: Cannot calculate custom expressions"), "success": True})

@app.route('/api/symbolic', methods=['POST'])
def calculate_symbolic():
    """Perform symbolic calculations"""
    data = request.json
    expression = data.get('expression', '')
    
    if UML_AVAILABLE:
        try:
            # This would use the actual symbolic engine
            # result = symbolic_engine.evaluate(expression)
            result = f"Symbolic result for: {expression}"
            return jsonify({"result": result, "success": True})
        except Exception as e:
            return jsonify({"result": f"Error: {str(e)}", "success": False})
    else:
        # Demo mode
        results = {
            "expand((x+y)^2)": "x^2 + 2xy + y^2",
            "solve(x^2-4=0, x)": "x = -2, x = 2",
            "diff(sin(x)*cos(x), x)": "cos(x)^2 - sin(x)^2"
        }
        return jsonify({"result": results.get(expression, "Demo mode: Cannot calculate custom expressions"), "success": True})

@app.route('/api/magic', methods=['POST'])
def generate_magic():
    """Generate magic squares"""
    data = request.json
    size = data.get('size', 3)
    
    # Predefined magic squares for demo
    magic_squares = {
        3: [
            [8, 1, 6],
            [3, 5, 7],
            [4, 9, 2]
        ],
        4: [
            [16, 3, 2, 13],
            [5, 10, 11, 8],
            [9, 6, 7, 12],
            [4, 15, 14, 1]
        ],
        5: [
            [17, 24, 1, 8, 15],
            [23, 5, 7, 14, 16],
            [4, 6, 13, 20, 22],
            [10, 12, 19, 21, 3],
            [11, 18, 25, 2, 9]
        ]
    }
    
    size = int(size)
    if size in magic_squares:
        square = magic_squares[size]
        magic_sum = size * (size**2 + 1) // 2  # Formula for magic constant
        
        return jsonify({
            "square": square,
            "magic_sum": magic_sum,
            "success": True
        })
    else:
        return jsonify({"error": "Unsupported size", "success": False})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
