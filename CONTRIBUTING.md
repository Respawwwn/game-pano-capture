# Developing on Game Pano Capture

* Issues should be filed at
https://github.com/Respawwwn/game-pano-capture/issues
* Pull requests can be made against
https://github.com/Respawwwn/game-pano-capture/pulls

## 📦 Repositories

Github repo

  ```bash
  $ git remote add origin git@github.com:Respawwwn/game-pano-capture.git
  ```

## 🔧 Prerequisites

First of all, you will need to have the following tools installed
globally on your environment:

  * Python 3.8+
  * pip
  * git

## Project bootstrap

Clone the repository and set up the development environment:

    git clone git@github.com:Respawwwn/game-pano-capture.git
    cd game-pano-capture
    
    # Create virtual environment (recommended)
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    
    # Install dependencies
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    
    # Test the installation
    python pano_capture.py --help

## Install Python

If you don't have Python installed:

```bash
# Using package manager on various systems
# Windows: Download from python.org
# macOS: 
brew install python
# Linux (Ubuntu/Debian):
sudo apt install python python-pip
```

Verify the installation:
```bash
python --version
```

## 🏆 Tests

We use pytest for testing to ensure code quality and prevent regressions. Tests are organized by platform and functionality using pytest markers.

### Test Structure

Tests are organized into different categories:

- **Unit tests** (`@pytest.mark.unit`) - Platform-agnostic tests that run on all platforms
- **Platform-specific tests** - Tests that only run on specific platforms:
  - `@pytest.mark.linux` - Linux/generic keyboard tests
  - `@pytest.mark.windows` - Windows-specific tests
  - `@pytest.mark.macos` - macOS-specific tests

### Running Tests

Run different test categories:

```bash
# Run all tests with coverage
pytest

# Run only unit tests (platform-agnostic)
pytest -m "unit"

# Run platform-specific tests (automatically detected)
pytest -m "linux"    # On Linux systems
pytest -m "windows"  # On Windows systems  
pytest -m "macos"    # On macOS systems

# Run tests with verbose output
pytest --verbose
```

### Coverage Reports

After running tests with coverage, you can view the HTML report by opening `htmlcov/index.html` in your browser.

## 🚔 Check Python coding standards & best practices

During development, we use Ruff for linting and formatting to maintain code quality.

The following tools are available:

- `ruff` (linting and formatting)

#### Running Ruff Linter

https://github.com/astral-sh/ruff

Ruff is an extremely fast Python linter, written in Rust. It can replace Flake8, isort, pydocstyle, pyupgrade, autoflake, and more.

  ```bash
  # Check for linting issues.
  ruff check .
  
  # Auto-fix all fixable issues.
  ruff check --fix .
  ```

#### Running Ruff Formatter

Ruff also includes a formatter that can format your Python code according to the Black code style.

  ```bash
  # Check formatting (dry run).
  ruff format --check .
  
  # Actually format files.
  ruff format .
  ```

## 📦 Building Standalone Executable

You can create a standalone executable using PyInstaller for distribution without requiring Python installation.

### Prerequisites

Install development dependencies including PyInstaller:

```bash
pip install -r requirements-dev.txt
```

### Building

#### Using the Build Script (Recommended)

```bash
python3 build.py
```

This will:
- Clean previous build artifacts
- Create a standalone executable using PyInstaller
- Show the output file size and location

#### Manual Build

```bash
# Simple one-file build
pyinstaller --onefile --name pano-capture pano_capture.py

# Using the custom spec file (recommended)
pyinstaller pano-capture.spec

# For debugging (shows console output)
pyinstaller --onefile --console --name pano-capture pano_capture.py
```

### Output

The executable will be created in the `dist/` directory:
- **Windows**: `dist/pano-capture.exe`
- **macOS/Linux**: `dist/pano-capture`

### Distribution

The standalone executable:
- Contains all dependencies and Python interpreter
- Does not require Python installation on target machine
- Is platform-specific (build on each target platform)
- Typical size: 50-100MB depending on dependencies

### Testing the Executable

```bash
# Windows
.\dist\pano-capture.exe --help

# macOS/Linux
./dist/pano-capture --help
```
