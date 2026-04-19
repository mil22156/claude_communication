# Claude Communication — CLAUDE.md

## Project Summary
An email-driven personal knowledge capture system. Emails sent with a `[CLAUDE]` subject
prefix are automatically parsed and routed to project folders in GitHub, committed as
context files. Designed to close the loop between Claude Code (desktop) and Claude.ai
(mobile/tablet).

## Stack
- Python 3.12
- Gmail API (Google Cloud)
- PyGitHub or git CLI (GitHub commits)
- JSON or YAML (routing config)

## Project Structure
```
main.py               — Entry point / scheduler
gmail/
  client.py           — Gmail API authentication and email fetching
  parser.py           — Parse [CLAUDE] emails into structured data
github/
  committer.py        — Commit parsed content to target GitHub repo/folder
config/
  routing.json        — Maps project keywords to target repos/folders
CLAUDE.md             — This file
PROJECT_LOG.md        — Milestone notes and decisions by date
AI_JOURNAL.md         — AI assistance log (CS50 academic honesty)
```

## How It Works
1. Script polls Gmail for unread emails with `[CLAUDE]` in the subject
2. Email subject and body are parsed to determine target project
3. Content is committed to the appropriate folder in the target GitHub repo
4. Email is marked as read

## Design Decisions
- TBD as project develops

## Public vs Private
- This repo (code + docs): public
- Captured knowledge/notes repo: private (personal content)

## AI Assistance Guidelines
- Claude Code role: tutor, explainer, reviewer, debugger — NOT code author
- GitHub Copilot role: inline suggestions while typing (user decides what to accept)
- Any significant Copilot-generated code must be logged in AI_JOURNAL.md
- **Claude Code must update AI_JOURNAL.md whenever PROJECT_LOG.md is updated**
- Work through problems step by step; let the user write the code
- When running git commands, briefly explain what each command is doing and why
- When in doubt, explain the concept and let the user implement it
