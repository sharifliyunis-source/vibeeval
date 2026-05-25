"""
Send Newsletter Email
Sends the final newsletter draft to the recipient email.
Automatically runs safety_scan.py before sending.
Blocks distribution if safety check fails.
"""

import os
import re
import smtplib
import subprocess
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DRAFTS_DIR = ROOT / "drafts"
PUBLISHED_DIR = ROOT / "published"
SCRIPTS_DIR = ROOT / "scripts"

# ── Environment variables ───────────────────────────────────────────────────────
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS", "")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL", "")


def validate_env() -> None:
    """Ensure all required environment variables are set."""
    missing = []
    for var, val in [
        ("EMAIL_ADDRESS", EMAIL_ADDRESS),
        ("EMAIL_PASSWORD", EMAIL_PASSWORD),
        ("SMTP_SERVER", SMTP_SERVER),
        ("SMTP_PORT", SMTP_PORT),
        ("RECIPIENT_EMAIL", RECIPIENT_EMAIL),
    ]:
        if not val:
            missing.append(var)
    if missing:
        sys.exit(
            f"ERROR: Missing required environment variables: {', '.join(missing)}\n"
            f"See /.env.example and /scripts/email_config.md for setup instructions."
        )


def get_latest_draft() -> Path:
    """Return the most recently modified draft file."""
    drafts = sorted(DRAFTS_DIR.glob("draft_issue_*.md"))
    if not drafts:
        sys.exit("ERROR: No draft files found in /drafts. Run generate_weekly_brief.py first.")
    return drafts[-1]


def run_safety_scan(draft_path: Path) -> bool:
    """Run safety_scan.py and return True if safe to send."""
    print("Running safety scan before distribution...")
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "safety_scan.py"), str(draft_path)],
        capture_output=False,
    )
    passed = result.returncode == 0
    if not passed:
        print("\nSafety scan FAILED. Distribution blocked.")
        print("Please address safety findings before resending.")
    return passed


def extract_issue_number(filename: str) -> int:
    """Extract issue number from draft filename."""
    match = re.search(r"issue_(\d+)", filename)
    return int(match.group(1)) if match else 0


def extract_executive_summary(content: str) -> str:
    """Extract Executive Summary section from newsletter Markdown."""
    match = re.search(
        r"## Executive Summary\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL
    )
    if match:
        summary = match.group(1).strip()
        # Remove Markdown formatting for plain email body
        summary = re.sub(r"\*\*(.*?)\*\*", r"\1", summary)
        summary = re.sub(r"\*(.*?)\*", r"\1", summary)
        return summary
    return "Executive summary not found. Please refer to the attached newsletter."


def extract_main_topic(content: str) -> str:
    """Extract a short topic string from the newsletter title or first heading."""
    match = re.search(r"^# (.+)$", content, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        # Extract subtitle or topic after issue number
        topic_match = re.search(r"Weekly Issue #\d+[^\n]*\n\*\*Subtitle:\*\* (.+)", title)
        if topic_match:
            return topic_match.group(1).strip()[:60]
        return "Multi-Layer Corridor Developments"
    return "Multi-Layer Corridor Developments"


def markdown_to_plain_text(content: str) -> str:
    """Convert Markdown to readable plain text for email body."""
    text = content
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"^---+$", "-" * 40, text, flags=re.MULTILINE)
    text = re.sub(r"\|[^\n]+\|", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def build_email(
    draft_path: Path,
    content: str,
    issue_number: int,
    main_topic: str,
    executive_summary: str,
) -> MIMEMultipart:
    """Construct the email message with Markdown and plain text attachments."""
    today = datetime.today().strftime("%Y-%m-%d")
    subject = f"Middle Corridor Brief | Weekly Issue #{issue_number} | {main_topic}"

    msg = MIMEMultipart("mixed")
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = subject

    # Email body (plain text executive summary)
    body_text = f"""Middle Corridor Brief — Weekly Issue #{issue_number}
{today}

EXECUTIVE SUMMARY

{executive_summary}

---

The full newsletter is attached as a Markdown file (.md) and plain text (.txt).

---
This is a personal research publication. Views are solely those of the author.
"""

    msg.attach(MIMEText(body_text, "plain", "utf-8"))

    # Attachment 1: Markdown version
    md_attachment = MIMEText(content, "plain", "utf-8")
    md_attachment.add_header(
        "Content-Disposition",
        "attachment",
        filename=f"middle_corridor_brief_issue_{issue_number:03d}_{today}.md",
    )
    msg.attach(md_attachment)

    # Attachment 2: Plain text version
    plain_text = markdown_to_plain_text(content)
    txt_attachment = MIMEText(plain_text, "plain", "utf-8")
    txt_attachment.add_header(
        "Content-Disposition",
        "attachment",
        filename=f"middle_corridor_brief_issue_{issue_number:03d}_{today}.txt",
    )
    msg.attach(txt_attachment)

    return msg


def send_email(msg: MIMEMultipart) -> None:
    """Send the email via SMTP."""
    print(f"Connecting to {SMTP_SERVER}:{SMTP_PORT}...")
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
    print("Email sent successfully.")


def archive_published(content: str, draft_path: Path, issue_number: int) -> None:
    """Copy the sent newsletter to /published."""
    PUBLISHED_DIR.mkdir(exist_ok=True)
    today = datetime.today().strftime("%Y%m%d")
    published_path = PUBLISHED_DIR / f"published_issue_{issue_number:03d}_{today}.md"
    published_path.write_text(content, encoding="utf-8")
    print(f"Issue archived to: {published_path}")


def main(draft_path_arg: str | None = None) -> None:
    print("=" * 60)
    print("Middle Corridor Brief — Newsletter Distribution")
    print("=" * 60)

    validate_env()

    draft_path = Path(draft_path_arg) if draft_path_arg else get_latest_draft()
    print(f"Draft selected: {draft_path.name}")

    # Safety gate
    safe = run_safety_scan(draft_path)
    if not safe:
        sys.exit(1)

    print("\nSafety check passed. Preparing email...")

    content = draft_path.read_text(encoding="utf-8")
    issue_number = extract_issue_number(draft_path.stem)
    main_topic = extract_main_topic(content)
    executive_summary = extract_executive_summary(content)

    msg = build_email(draft_path, content, issue_number, main_topic, executive_summary)

    print(f"Recipient: {RECIPIENT_EMAIL}")
    print(f"Subject: {msg['Subject']}")

    send_email(msg)
    archive_published(content, draft_path, issue_number)

    print("\nDistribution complete.")


if __name__ == "__main__":
    draft_arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(draft_arg)
