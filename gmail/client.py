import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes define what the app is allowed to do with the Gmail account.
# readonly = read and label emails; modify = also mark as read.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), '..', 'config', 'credentials.json')
TOKEN_FILE = os.path.join(os.path.dirname(__file__), '..', 'config', 'token.json')


def get_gmail_service():
    """Authenticate and return an authorized Gmail API service instance.

    On first run, opens a browser for OAuth authorization and saves token.json.
    On subsequent runs, loads the saved token and refreshes it if expired.
    """
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def fetch_claude_emails(service):
    """Fetch unread emails with [CLAUDE] in the subject. Returns list of message dicts."""
    results = service.users().messages().list(
        userId='me',
        q='subject:[CLAUDE] is:unread'
    ).execute()

    messages = results.get('messages', [])
    emails = []

    for msg in messages:
        detail = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='full'
        ).execute()
        emails.append(detail)

    return emails


def mark_as_read(service, message_id):
    """Mark a Gmail message as read after processing."""
    service.users().messages().modify(
        userId='me',
        id=message_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()
