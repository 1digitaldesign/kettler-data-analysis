# Installing Python 3.14.0

Guide to install Python 3.14.0 on macOS for this project.

## Download

Python 3.14.0 installer has been downloaded to `/tmp/python-3.14.0-macos11.pkg`

## Installation Methods

### Method 1: Install via Installer (Recommended)

1. Open the installer:
```bash
open /tmp/python-3.14.0-macos11.pkg
```

2. Follow the installation wizard:
   - Click "Continue" through the introduction
   - Review the license and click "Agree"
   - Select installation location (default is recommended)
   - Click "Install" and enter your password
   - Wait for installation to complete

3. Verify installation:
```bash
python3.14 --version
```

### Method 2: Install via Homebrew (Alternative)

If you prefer using Homebrew:

```bash
brew install python@3.14
```

### Method 3: Download from Official Site

You can also download directly from:
- **macOS Universal2 Installer:** https://www.python.org/ftp/python/3.14.0/python-3.14.0-macos11.pkg
- **Release Page:** https://www.python.org/downloads/release/python-3140/

## After Installation

### Verify Installation

```bash
python3.14 --version
# Should output: Python 3.14.0
```

### Update PATH (if needed)

Add to your `~/.zshrc` or `~/.bash_profile`:

```bash
export PATH="/Library/Frameworks/Python.framework/Versions/3.14/bin:$PATH"
```

### Create Virtual Environment

```bash
cd /Users/machine/Documents/kettler-data-analysis
python3.14 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Verify Project Works

```bash
python3.14 scripts/utils/check_doc_links.py
```

## Python 3.14 Features

This project now uses Python 3.14 features:

- **PEP 779:** Free-threaded Python support
- **PEP 649:** Deferred evaluation of annotations
- **PEP 750:** Template string literals (t-strings)
- **PEP 734:** Multiple interpreters in stdlib
- **PEP 784:** `compression.zstd` module
- **PEP 758:** `except` expressions without brackets
- Improved error messages
- Better performance optimizations

## Troubleshooting

### Issue: Command not found

If `python3.14` is not found:
1. Check installation location: `/Library/Frameworks/Python.framework/Versions/3.14/bin/`
2. Add to PATH (see above)
3. Use full path: `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3.14`

### Issue: Multiple Python versions

Use `pyenv` to manage versions:
```bash
brew install pyenv
pyenv install 3.14.0
pyenv local 3.14.0
```

### Issue: Permission denied

You may need to run installer with sudo or adjust permissions:
```bash
sudo installer -pkg /tmp/python-3.14.0-macos11.pkg -target /
```

## Related Documentation

- [Python 3.14.0 Release Notes](https://www.python.org/downloads/release/python-3140/)
- [What's New in Python 3.14](https://docs.python.org/3.14/whatsnew/3.14.html)
- [Installation Guide](INSTALLATION.md)
