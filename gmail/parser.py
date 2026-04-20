import base64
import re


def parse_email(message):
    """Extract subject, body, and project tag from a Gmail message dict.

    Returns a dict with keys: message_id, subject, project, body.
    project is parsed from [CLAUDE:project-name] in the subject, or 'general' if not found.
    """
    headers = {h['name']: h['value'] for h in message['payload']['headers']}
    subject = headers.get('Subject', '')
    message_id = message['id']

    project = _extract_project(subject)
    body = _extract_body(message['payload'])

    return {
        'message_id': message_id,
        'subject': subject,
        'project': project,
        'body': body
    }


def _extract_project(subject):
    """Parse project name from subject line.

    Expects format: [CLAUDE] or [CLAUDE:project-name]
    Returns project name string, or 'general' if none specified.
    """
    match = re.search(r'\[CLAUDE:([^\]]+)\]', subject, re.IGNORECASE)
    if match:
        return match.group(1).strip().lower().replace(' ', '-')
    return 'general'


def _extract_body(payload):
    """Decode the email body from base64. Handles plain text and multipart emails."""
    if payload.get('mimeType') == 'text/plain':
        data = payload.get('body', {}).get('data', '')
        return base64.urlsafe_b64decode(data).decode('utf-8') if data else ''

    if 'parts' in payload:
        for part in payload['parts']:
            if part.get('mimeType') == 'text/plain':
                data = part.get('body', {}).get('data', '')
                return base64.urlsafe_b64decode(data).decode('utf-8') if data else ''

    return ''
