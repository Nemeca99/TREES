"""
Setup script for TREES Framework and UML Calculator
"""
from setuptools import setup, find_packages

setup(
    name="trees-framework",
    version="0.1.0",
    description="T.R.E.E.S. Framework and UML Calculator - Recursive systems theory and implementation",
    author="Travis Miner",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "sympy>=1.8",
        "matplotlib>=3.4.0",
        "rich>=10.0.0",
        "typer>=0.4.0",
        "networkx>=2.5",
        "pydot>=1.4.2",
        "graphviz>=0.16",
        "pillow>=8.0.0"
    ],
    entry_points={
        "console_scripts": [
            "uml-calculator=UML_Calculator.uml_calculator:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
