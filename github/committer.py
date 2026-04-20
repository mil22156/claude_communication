import os
from datetime import datetime
from github import Github

# GitHub personal access token — stored in .env, never committed
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

# Target repo where notes will be committed (private repo for personal content)
NOTES_REPO = os.environ.get('NOTES_REPO', 'mil22156/claude-notes')


def commit_note(project, subject, body):
    """Commit an email note to the appropriate project folder in the notes repo.

    Creates a markdown file named by timestamp under notes/<project>/.
    """
    if not GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN environment variable not set")

    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(NOTES_REPO)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"notes/{project}/{timestamp}.md"

    content = f"# {subject}\n\n{body}\n"

    try:
        existing = repo.get_contents(filename)
        repo.update_file(filename, f"Update note: {subject}", content, existing.sha)
    except Exception:
        repo.create_file(filename, f"Add note: {subject}", content)
