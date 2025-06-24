# TREES Interactive Web Demo

This interactive demo showcases the capabilities of the TREES framework and UML Calculator in a user-friendly web interface.

## Features

- **Basic UML Calculator**: Try basic UML operations with letter-number notation
- **RIS Meta-Operators**: Explore recursive identity transformations
- **Symbolic Engine**: Perform symbolic algebra operations
- **Magic Squares**: Generate and analyze magic squares of different sizes

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Flask and Flask-CORS (installed automatically if using the run script)

### Running the Demo

1. From the `web_demo` directory, run:

   ```bash
   run_web_demo.bat
   ```

2. Open a web browser and navigate to:

   ```plaintext
   http://localhost:5000
   ```

## Structure

- `index.html` - The main demo interface
- `app.py` - Flask server that provides the API endpoints
- `requirements.txt` - Python dependencies
- `run_web_demo.bat` - Batch script to run the demo

## API Endpoints

- `/api/basic` - Calculate basic UML expressions
- `/api/ris` - Apply RIS meta-operators
- `/api/symbolic` - Perform symbolic calculations
- `/api/magic` - Generate magic squares

## Notes

This demo is designed to showcase the core capabilities of TREES. The actual implementation can:

- Work in stand-alone mode with simulated results
- Connect to the full UML Calculator engine when available
- Be easily extended with additional features

## Adding to GitHub Pages

To deploy this demo on GitHub Pages:

1. Push the entire `web_demo` directory to your repository
2. Enable GitHub Pages in your repository settings
3. Set the source to the `web_demo` directory
4. Access your demo at `https://[username].github.io/TREES/web_demo/`

Note: GitHub Pages is static hosting, so the API endpoints won't function without a backend server. For full functionality, deploy to a server that supports Python/Flask.
