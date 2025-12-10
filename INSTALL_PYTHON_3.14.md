# Installing Python 3.14.0

Guide to install and use Python 3.14.0 for this project.

## Status

✅ **Python 3.14.0 is already installed!**

```bash
python3.14 --version

# Output: Python 3.14.0
```

**Location:** `/opt/homebrew/bin/python3.14` (installed via Homebrew)

## Using Python 3.14

### Option 1: Use Virtual Environment (Recommended)

A virtual environment has been created for this project:

```bash
cd /Users/machine/Documents/kettler-data-analysis
source venv314/bin/activate
python --version  # Should show Python 3.14.0
pip install -r requirements.txt
```

### Option 2: Use Python 3.14 Directly

```bash
python3.14 scripts/utils/check_doc_links.py
python3.14 bin/run_pipeline.py
```

### Option 3: Set as Default (Optional)

If you want Python 3.14 as your default Python 3:

```bash

# Add to ~/.zshrc or ~/.bash_profile
alias python3=python3.14
alias pip3=pip3.14
```

## Installation Methods (If Needed)

### Method 1: Install via Homebrew (Already Done)

Python 3.14.0 is installed via Homebrew at `/opt/homebrew/bin/python3.14`

To reinstall or update:
```bash
brew install python@3.14

# or
brew upgrade python@3.14
```

### Method 2: Install via Official Installer

The official installer has been downloaded to `/tmp/python-3.14.0-macos11.pkg`

To install:
```bash
open /tmp/python-3.14.0-macos11.pkg
```

Follow the installation wizard:
1. Click "Continue" through the introduction
2. Review the license and click "Agree"
3. Select installation location (default is recommended)
4. Click "Install" and enter your password
5. Wait for installation to complete

After installation, Python 3.14 will be available at:
- `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3`
- Or via `python3.14` if PATH is configured

### Method 3: Download from Official Site

Download directly from:
- **macOS Universal2 Installer:** https://www.python.org/ftp/python/3.14.0/python-3.14.0-macos11.pkg
- **Release Page:** https://www.python.org/downloads/release/python-3140/

## Verification

Verify Python 3.14 installation:

```bash
python3.14 --version

# Should output: Python 3.14.0

python3.14 -m pip --version

# Should show pip version
```

## Project Setup

### Create Virtual Environment

```bash
cd /Users/machine/Documents/kettler-data-analysis
python3.14 -m venv venv314
source venv314/bin/activate
pip install -r requirements.txt
```

### Verify Project Works

```bash
source venv314/bin/activate
python scripts/utils/check_doc_links.py
python bin/run_pipeline.py --help
```

## Python 3.14 Features

This project uses Python 3.14 features:

- **PEP 779:** Free-threaded Python support
- **PEP 649:** Deferred evaluation of annotations
- **PEP 750:** Template string literals (t-strings)
- **PEP 734:** Multiple interpreters in stdlib
- **PEP 784:** `compression.zstd` module
- **PEP 758:** `except` expressions without brackets
- Improved error messages
- Better performance optimizations
- Modern type hints (lowercase `dict`, `list`, `tuple`)

## Troubleshooting

### Issue: Command not found

If `python3.14` is not found:
1. Check if installed: `brew list | grep python`
2. Install via Homebrew: `brew install python@3.14`
3. Check PATH: `echo $PATH | grep homebrew`

### Issue: Virtual environment uses wrong Python

Recreate virtual environment:
```bash
rm -rf venv314
python3.14 -m venv venv314
source venv314/bin/activate
pip install -r requirements.txt
```

### Issue: Multiple Python versions

Use `pyenv` to manage versions:
```bash
brew install pyenv
pyenv install 3.14.0
pyenv local 3.14.0
```

## Related Documentation

- [Python 3.14.0 Release Notes](https://www.python.org/downloads/release/python-3140/)
- [What's New in Python 3.14](https://docs.python.org/3.14/whatsnew/3.14.html)
- [Installation Guide](INSTALLATION.md)
- [Quick Start Guide](QUICK_START.md)
