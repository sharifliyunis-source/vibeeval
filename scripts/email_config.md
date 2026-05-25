# Email Configuration Guide

## Middle Corridor Brief — Email Distribution Setup

---

## Overview

The newsletter is distributed via `send_newsletter_email.py` using Gmail SMTP. The script uses environment variables — no credentials are ever hardcoded.

---

## Step 1 — Create Your App Password

Gmail requires an App Password for SMTP access when 2-Factor Authentication is enabled.

1. Go to your Google Account: https://myaccount.google.com/
2. Navigate to **Security** → **2-Step Verification** (enable if not already active)
3. Scroll to **App Passwords**
4. Select **Mail** as the app, **Other** as the device (name it "Middle Corridor Brief")
5. Copy the 16-character app password generated

---

## Step 2 — Configure Environment Variables

Copy the example file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```
EMAIL_ADDRESS=your_gmail@gmail.com
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx   # 16-character App Password (spaces optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
RECIPIENT_EMAIL=sharifli.yunis@gmail.com
```

---

## Step 3 — Load Environment Variables

Before running the email script, load the environment variables:

```bash
# Option A: Export manually
export $(grep -v '^#' .env | xargs)

# Option B: Use python-dotenv (install if needed)
pip install python-dotenv
```

If using `python-dotenv`, add this to the top of any script:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Step 4 — Run the Distribution Pipeline

Full pipeline (generates draft → runs safety scan → sends email):

```bash
# Step 1: Generate the draft
python scripts/generate_weekly_brief.py

# Step 2: Review the draft manually (optional but recommended)
# Edit drafts/draft_issue_XXX_YYYYMMDD.md

# Step 3: Send (automatically runs safety scan first)
python scripts/send_newsletter_email.py
```

To send a specific draft file:

```bash
python scripts/send_newsletter_email.py drafts/draft_issue_001_20240601.md
```

---

## Email Format

**Subject line format:**
```
Middle Corridor Brief | Weekly Issue #[X] | [Main Topic]
```

**Email body:**
- Plain text executive summary
- Issue date and number

**Attachments:**
- `middle_corridor_brief_issue_XXX_YYYYMMDD.md` — Full Markdown version
- `middle_corridor_brief_issue_XXX_YYYYMMDD.txt` — Plain text version

---

## Safety Gate

The email script automatically runs `safety_scan.py` before sending.

- If the safety score is **7/10 or above**: email proceeds
- If the safety score is **below 7/10**: distribution is **blocked**
- A safety review report is saved to `/safety_review/`

To override the safety gate (not recommended), you can run `send_newsletter_email.py` with the `--force` flag — but this should only be used after manual review confirms the draft is safe.

---

## Troubleshooting

| Error | Solution |
|---|---|
| `SMTPAuthenticationError` | Check your App Password; ensure 2FA is enabled on Google account |
| `Missing required environment variables` | Ensure `.env` is loaded before running the script |
| `No draft files found` | Run `generate_weekly_brief.py` first |
| `Safety scan FAILED` | Review `/safety_review/` report and revise the draft |
| Connection timeout | Check SMTP_SERVER and SMTP_PORT values |

---

## Security Notes

- **Never commit `.env` to version control** — add it to `.gitignore`
- App Passwords can be revoked at any time from your Google Account settings
- The script uses TLS encryption (`STARTTLS`) for all SMTP connections
- No credentials are logged or stored by the scripts
