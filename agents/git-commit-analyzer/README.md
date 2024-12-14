# Git Commit Analyzer

An AI agent that analyzes your git changes and suggests meaningful commit messages following conventional commit format.

## Features
- Analyzes `git diff` output using local Qwen 2.5 32B model
- Categorizes changes (feat, fix, refactor, etc.)
- Generates concise and descriptive commit messages
- Follows conventional commit format
- Stores conversation history in SQLite database

## Requirements
- Python 3.8+
- phi framework
- GitPython
- Local Qwen 2.5 32B model installation

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure you have the Qwen 2.5 32B model installed locally

## Usage
1. Navigate to your git repository
2. Run the analyzer:
```bash
python commit_analyzer.py
```

## Example Output
```
Suggested commit message:
feat(auth): implement OAuth2 authentication flow
```

## How it works
The agent:
1. Checks if you're in a git repository
2. Gets the current uncommitted changes using `git diff`
3. Uses the local Qwen 2.5 32B model to analyze the changes
4. Generates a conventional commit message
5. Stores the conversation history in a local SQLite database

## Notes
- Make sure you're in a git repository when running the script
- The script requires uncommitted changes to analyze
- The script uses a local instance of Qwen 2.5 32B model for generating commit messages
- Conversation history is stored in `agents.db` SQLite database