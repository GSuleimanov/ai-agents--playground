# AI Development Agents Collection

A collection of practical AI agents to assist with daily development tasks.

## Projects Overview

1. **git-commit-analyzer** - Analyzes git diffs and suggests commit messages
2. **code-documenter** - Generates documentation for Java code
3. **pr-reviewer** - Reviews pull requests and provides feedback
4. **jira-assistant** - Helps with JIRA ticket creation and updates

## Requirements
- Python 3.8+
- System-specific dependencies (installed automatically)

## Installation

The project uses system-specific dependencies for secure credential storage:
- Windows: Windows Credential Manager (via pywin32)
- macOS: Keychain (built-in)
- Linux: Secret Service (via secretstorage)

To install, simply run:

```bash
python setup.py
```

This will automatically install the appropriate dependencies for your operating system.

## Manual Installation

If you prefer to install dependencies manually, you can use the requirements files directly:

```bash
# Windows
pip install -r requirements/windows.txt

# macOS
pip install -r requirements/macos.txt

# Linux
pip install -r requirements/linux.txt

# Other systems
pip install -r requirements/base.txt
```

## Project Structure
```
agents/
├── requirements/          # System-specific requirements
│   ├── base.txt          # Common dependencies
│   ├── windows.txt       # Windows-specific
│   ├── linux.txt         # Linux-specific
│   └── macos.txt         # macOS-specific
├── utils/                # Shared utilities
│   ├── credentials.py    # Secure credential storage
│   └── ...
└── git-commit-analyzer/  # Individual agents
    ├── README.md
    └── commit_analyzer.py
```
