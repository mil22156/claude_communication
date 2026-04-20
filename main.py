from gmail.client import get_gmail_service, fetch_claude_emails, mark_as_read
from gmail.parser import parse_email
from github.committer import commit_note


def run():
    """Fetch unread [CLAUDE] emails, commit them as notes to GitHub, mark as read."""
    print("Connecting to Gmail...")
    service = get_gmail_service()

    emails = fetch_claude_emails(service)
    if not emails:
        print("No new [CLAUDE] emails found.")
        return

    print(f"Found {len(emails)} email(s) to process.")

    for message in emails:
        email = parse_email(message)
        print(f"Processing: {email['subject']} → project: {email['project']}")

        commit_note(email['project'], email['subject'], email['body'])
        mark_as_read(service, email['message_id'])
        print(f"  Committed and marked as read.")

    print("Done.")


if __name__ == '__main__':
    run()
