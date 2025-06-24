# UML Calculator Modern CLI

### Get Started

Run the calculator:
```
python modern_cli.py
```

### Features

- **Interactive Mode**: Just run `modern_cli.py` without arguments
- **Command Mode**: Run specific calculations from command line
- **History Tracking**: Automatically saves your calculations
- **Batch Processing**: Process multiple calculations from CSV files
- **Beautiful UI**: Color-coded output and formatted tables

### Command Reference

- `calc` - Calculate RIS of two numbers
  ```
  modern_cli.py calc 6 3 --explain
  ```

- `history` - Show calculation history
  ```
  modern_cli.py history --limit 20
  ```

- `batch` - Process calculations from CSV file
  ```
  modern_cli.py batch input.csv --output-file results.csv
  ```

- `export` - Export history to CSV/JSON
  ```
  modern_cli.py export history.csv
  ```

- `table` - Display the RIS truth table
  ```
  modern_cli.py table
  ```

- `sample` - Generate a sample batch input file
  ```
  modern_cli.py sample
  ```

### CSV Batch Format

Create a CSV file with format: `a,b,mode`

Example:
```
6,3,default
8,2,default
5,5,default
10,5,always_multiply
```

### Requirements

- Python 3.x
- Rich library (`pip install rich`)
- Typer library (`pip install typer`)
