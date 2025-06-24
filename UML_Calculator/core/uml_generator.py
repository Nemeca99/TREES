"""
UML generation utilities for UML Calculator
"""
import os
import tempfile
import pydot
import plantuml
from pathlib import Path

class UMLGenerator:
    """Generate UML diagrams for mathematical operations and RIS logic"""
    
    def __init__(self):
        self.plantuml_server = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/img/')
        
    def generate_ris_diagram(self, a, b, result, operation, explanation=None):
        """Generate UML diagram for a RIS operation"""
        if operation == "×" or operation == "*":
            op_name = "Multiplication"
        elif operation == "÷" or operation == "/":
            op_name = "Division"
        elif operation == "+" or operation == "Addition":
            op_name = "Addition"
        else:
            op_name = "Operation"
            
        puml = f"""
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Courier
skinparam defaultFontSize 12

title RIS({a}, {b}) Operation

class "Input A" as A {{
  value = {a}
}}

class "Input B" as B {{
  value = {b}
}}

class "RIS Operation" as RIS {{
  determine_operation()
  apply_operation()
  operation = {op_name}
}}

class "Result" as Result {{
  value = {result}
}}

A --> RIS
B --> RIS
RIS --> Result

note right of RIS
  {explanation if explanation else f"RIS({a}, {b}) = {result} via {op_name}"}
end note

@enduml
"""
        return puml
        
    def generate_function_diagram(self, expression, variables=None):
        """Generate UML diagram for a mathematical function"""
        var_str = ", ".join([f"{k}={v}" for k, v in variables.items()]) if variables else "x"
        
        puml = f"""
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Courier
skinparam defaultFontSize 12

title Function: {expression}

class "Function" as F {{
  expression = "{expression}"
  variables = "{var_str}"
  evaluate()
}}

class "Input" as I {{
  {var_str}
}}

class "Output" as O {{
  result = f({var_str})
}}

I --> F : input
F --> O : output

@enduml
"""
        return puml
        
    def generate_equation_diagram(self, left_side, right_side, solutions=None):
        """Generate UML diagram for an equation and its solutions"""
        solution_text = ""
        if solutions:
            if isinstance(solutions, list):
                for i, sol in enumerate(solutions):
                    solution_text += f"  x{i+1} = {sol}\\n"
            else:
                solution_text = f"  x = {solutions}\\n"
        
        puml = f"""
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Courier
skinparam defaultFontSize 12

title Equation: {left_side} = {right_side}

class "Equation" as EQ {{
  left_side = "{left_side}"
  right_side = "{right_side}"
  solve()
}}

class "Solution" as S {{
{solution_text if solutions else "  No solution found"}
}}

EQ --> S : yields

@enduml
"""
        return puml
    
    def generate_ris_rules_diagram(self):
        """Generate UML diagram showing the RIS rules"""
        puml = """
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Courier
skinparam defaultFontSize 12

title RIS Rules

class "RIS Function" as RIS {
  ris(a, b)
}

class "Equal Values" as R1 {
  condition = "a == b"
  operation = "Multiplication"
  example = "RIS(5, 5) = 25"
}

class "Special Case" as R2 {
  condition = "a > b, special case"
  operation = "Multiplication"
  example = "RIS(6, 3) = 18"
}

class "Compact Division" as R3 {
  condition = "a % b == 0, a/b < a, b"
  operation = "Division"
  example = "RIS(8, 2) = 4"
}

class "Zero Values" as R4 {
  condition = "a == 0 or b == 0"
  operation = "Addition"
  example = "RIS(0, 5) = 5"
}

RIS --> R1 : rule 1
RIS --> R2 : rule 2
RIS --> R3 : rule 3
RIS --> R4 : rule 4

@enduml
"""
        return puml
        
    def render_plantuml(self, puml_content, output_file=None, format="svg"):
        """Render PlantUML content to a file or return as image data"""
        if output_file:
            # Write PlantUML content to temporary file
            with tempfile.NamedTemporaryFile(suffix='.puml', delete=False) as tmp:
                tmp.write(puml_content.encode('utf-8'))
                tmp_path = tmp.name
            
            # Render to the requested format
            if format == "svg":
                self.plantuml_server.processes_file(tmp_path, outfile=output_file, format="svg")
            else:
                self.plantuml_server.processes_file(tmp_path, outfile=output_file, format="png")
                
            # Clean up temporary file
            os.unlink(tmp_path)
            return output_file
        else:
            # Return image data for terminal display
            with tempfile.NamedTemporaryFile(suffix='.puml', delete=False) as tmp:
                tmp.write(puml_content.encode('utf-8'))
                tmp_path = tmp.name
            
            temp_output = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
            self.plantuml_server.processes_file(tmp_path, outfile=temp_output)
            
            # Clean up
            os.unlink(tmp_path)
            return temp_output
            
    def generate_graph(self, nodes, edges, title="Graph"):
        """Generate a graph with nodes and edges"""
        graph = pydot.Dot(graph_type="graph", label=title)
        
        # Add nodes
        for node_id, node_label in nodes.items():
            graph.add_node(pydot.Node(node_id, label=node_label))
            
        # Add edges
        for edge in edges:
            if len(edge) >= 2:
                if len(edge) > 2:  # If there's a label
                    graph.add_edge(pydot.Edge(edge[0], edge[1], label=edge[2]))
                else:
                    graph.add_edge(pydot.Edge(edge[0], edge[1]))
        
        # Save to a temp file
        temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        graph.write_png(temp_file.name)
        return temp_file.name
