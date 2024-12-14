from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.storage.agent.sqlite import SqlAgentStorage
from git import Repo
import os

git_agent = Agent(
    name="Git Commit Analyzer",
    model=Ollama(
        id="qwen2.5:32b",
        temperature=0.7
    ),
    stream=True,
    instructions=[
        "You are an expert at analyzing git changes and creating conventional commit messages.",
        "Always follow the conventional commit format: <type>(<scope>): <description>",
        "Types include: feat, fix, docs, style, refactor, test, chore",
        "Be concise and specific in commit messages"
    ],
    storage=SqlAgentStorage(table_name="git_agent", db_file="/agents/history.db"),
    add_history_to_messages=True,
    markdown=True,
)

def analyze_changes():
    # Get git repository
    try:
        repo = Repo(os.getcwd())
        if not repo.git.rev_parse("--is-inside-work-tree"):
            return "Error: Not inside a git repository"
    except Exception as e:
        return f"Error accessing git repository: {str(e)}"

    # Get uncommitted changes
    try:
        diff = repo.git.diff()
    except Exception as e:
        return f"Error getting git diff: {str(e)}"

    if not diff:
        return "No changes to analyze"

    # Analyze changes with AI
    prompt = f"""
    Analyze these git changes and suggest a conventional commit message:
    
    {diff}
    """

    return git_agent.print_response(prompt)

if __name__ == "__main__":
    suggestion = analyze_changes()
    print("\nSuggested commit message:")
    print(suggestion)