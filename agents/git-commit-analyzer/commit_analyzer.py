from phi.agent import Agent
from git import Repo
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.agent_utils import parameters

def analyze_changes():
    """Analyze staged git changes."""
    try:
        repo = Repo(os.getcwd())
        if not repo.git.rev_parse("--is-inside-work-tree"):
            return "Error: Not inside a git repository"

        # Get only staged changes
        staged_diff = repo.git.diff("--staged")

        if not staged_diff:
            return "No staged changes to analyze. Use 'git add' to stage your changes."

        # Get the list of staged files
        staged_files = repo.git.diff("--staged", "--name-only").split('\n')

        result = ["Staged files:"]
        result.extend([f"- {file}" for file in staged_files if file])
        result.append("\nDetailed changes:")
        result.append(staged_diff)

        return "\n".join(result)

    except Exception as e:
        return f"Error analyzing git repository: {str(e)}"

if __name__ == "__main__":
    result = analyze_changes()
    if result.startswith("Error") or result.startswith("No staged"):
        print(result)
    else:
        try:
            git_agent = Agent(**parameters("git-commit-analyzer"))
            prompt = "Analyze these git changes and suggest a conventional commit message:"
            prompt += "\n\n"
            prompt += f"## Context:\n{result}"
            prompt += "\n\n"
            prompt += "## Suggested Commit Message:"
            git_agent.print_response(prompt)
        except Exception as e:
            print(f"Error creating agent or analyzing changes: {str(e)}")
