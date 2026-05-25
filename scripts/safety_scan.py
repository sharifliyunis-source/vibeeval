"""
Safety Scan
Scans a newsletter draft for risky phrases, flags problematic wording,
suggests safer alternatives, and generates a safety review report.
Blocks distribution if the safety score falls below the threshold.
"""

import re
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
SAFETY_REVIEW_DIR = ROOT / "safety_review"
DRAFTS_DIR = ROOT / "drafts"

# ── Config ─────────────────────────────────────────────────────────────────────
SAFETY_THRESHOLD = 7  # Minimum score (out of 10) to allow distribution

# ── Risky phrase dictionary ─────────────────────────────────────────────────────
# Format: (risky_phrase, safer_alternative, severity)
# severity: "high" = -2 points, "medium" = -1 point, "low" = -0.5 points
RISKY_PHRASES: list[tuple[str, str, str]] = [
    # Sanctions framing
    ("sanctions evasion", "connectivity diversification", "high"),
    ("circumventing sanctions", "supply chain adjustment", "high"),
    ("avoiding sanctions", "trade route development", "high"),
    ("sanctions-busting", "alternative corridor development", "high"),
    ("forbidden trade", "emerging trade corridor", "high"),
    ("illicit trade", "commercial corridor activity", "high"),
    # Russia-bypass framing
    ("bypassing russia", "corridor route diversification", "high"),
    ("bypass russia", "trans-Caspian connectivity", "high"),
    ("anti-russia route", "Middle Corridor development", "high"),
    ("anti-russia corridor", "regional connectivity", "high"),
    ("avoiding russian territory", "alternative routing", "medium"),
    ("cutting out russia", "supply chain resilience", "high"),
    ("replace russia", "complementary connectivity", "medium"),
    ("exclud.*russia", "route diversification", "medium"),
    # Geopolitical weapon framing
    ("geopolitical weapon", "connectivity infrastructure", "high"),
    ("strategic tool against", "infrastructure investment", "high"),
    ("weaponiz", "trade route development", "high"),
    ("pressure instrument", "infrastructure modernization", "medium"),
    ("coercive connectivity", "regional integration", "high"),
    ("strategic encirclement", "regional connectivity development", "high"),
    # Great power rivalry
    ("great power battlefield", "Eurasian connectivity region", "high"),
    ("great power competition", "multilateral infrastructure development", "medium"),
    ("nato vs. russia", "regional infrastructure cooperation", "high"),
    ("containment strategy", "trade route modernization", "high"),
    ("counter-china", "development finance-backed investment", "high"),
    ("anti-china", "alternative connectivity", "high"),
    ("us vs. china", "multilateral infrastructure development", "medium"),
    # Military framing
    ("military corridor", "transport corridor", "high"),
    ("military route", "commercial transit route", "high"),
    ("nato supply line", "transport infrastructure", "high"),
    ("arms route", "transport corridor", "high"),
    ("defense logistics", "transport logistics", "medium"),
    ("dual-use infrastructure", "multimodal infrastructure", "low"),
    # Energy weapon
    ("energy weapon", "energy export infrastructure", "high"),
    ("weaponizing gas", "gas transit development", "high"),
    ("energy leverage", "energy connectivity", "medium"),
    ("energy blackmail", "energy supply disruption", "high"),
    ("held hostage.*energy", "energy supply resilience", "high"),
    ("energy dependency exploit", "energy diversification", "medium"),
    # Regime framing
    ("authoritarian regime", "government", "high"),
    ("dictator", "head of state", "high"),
    ("regime competition", "government-to-government cooperation", "high"),
    ("autocratic government", "government", "high"),
    ("regime-backed", "state-sponsored", "medium"),
    # China framing
    ("china threat", "Chinese infrastructure investment", "high"),
    ("chinese debt trap", "infrastructure financing", "high"),
    ("chinese influence operation", "Chinese commercial investment", "high"),
    ("chinese dominance", "Chinese corridor investment", "medium"),
    ("countering china", "connectivity diversification", "high"),
    ("excluding china", "multilateral corridor development", "high"),
]

SEVERITY_DEDUCTIONS = {"high": 2.0, "medium": 1.0, "low": 0.5}


def load_draft(path: Path) -> str:
    """Load the newsletter draft."""
    if not path.exists():
        sys.exit(f"ERROR: Draft file not found at {path}")
    return path.read_text(encoding="utf-8")


def scan_for_risky_phrases(text: str) -> list[dict]:
    """Scan text for all risky phrases and return findings."""
    findings = []
    text_lower = text.lower()
    for phrase, alternative, severity in RISKY_PHRASES:
        pattern = re.compile(phrase, re.IGNORECASE)
        matches = list(pattern.finditer(text))
        if matches:
            for match in matches:
                start = max(0, match.start() - 80)
                end = min(len(text), match.end() + 80)
                context = text[start:end].replace("\n", " ").strip()
                findings.append(
                    {
                        "phrase": match.group(),
                        "pattern": phrase,
                        "alternative": alternative,
                        "severity": severity,
                        "deduction": SEVERITY_DEDUCTIONS[severity],
                        "context": f"...{context}...",
                    }
                )
    return findings


def calculate_safety_score(findings: list[dict]) -> float:
    """Calculate safety score (10 = perfect, lower = more issues found)."""
    total_deduction = sum(f["deduction"] for f in findings)
    score = max(0.0, 10.0 - total_deduction)
    # Round to one decimal
    return round(score, 1)


def check_structural_elements(text: str) -> list[str]:
    """Check for required structural elements in the newsletter."""
    warnings = []
    required_sections = [
        ("## Executive Summary", "Missing Executive Summary section"),
        ("## Main Argument", "Missing Main Argument section"),
        ("Disclaimer", "Missing disclaimer"),
        ("## Why It Matters", "Missing 'Why It Matters' section"),
        ("## What to Watch Next", "Missing 'What to Watch Next' section"),
    ]
    for marker, warning in required_sections:
        if marker not in text:
            warnings.append(warning)
    return warnings


def generate_report(
    draft_path: Path,
    findings: list[dict],
    score: float,
    structural_warnings: list[str],
) -> tuple[str, Path]:
    """Generate the safety review report and return (content, report_path)."""
    today = datetime.today().strftime("%Y-%m-%d")
    timestamp = datetime.today().strftime("%Y%m%d_%H%M%S")

    status = "APPROVED FOR DISTRIBUTION" if score >= SAFETY_THRESHOLD else "BLOCKED — MANUAL REVIEW REQUIRED"
    status_marker = "PASS" if score >= SAFETY_THRESHOLD else "FAIL"

    # Group findings by severity
    high = [f for f in findings if f["severity"] == "high"]
    medium = [f for f in findings if f["severity"] == "medium"]
    low = [f for f in findings if f["severity"] == "low"]

    def fmt_finding(f: dict) -> str:
        return (
            f"  - **Found:** `{f['phrase']}`\n"
            f"    **Replace with:** {f['alternative']}\n"
            f"    **Context:** {f['context']}\n"
            f"    **Score deduction:** -{f['deduction']}\n"
        )

    high_section = "\n".join(fmt_finding(f) for f in high) or "  None found.\n"
    medium_section = "\n".join(fmt_finding(f) for f in medium) or "  None found.\n"
    low_section = "\n".join(fmt_finding(f) for f in low) or "  None found.\n"

    structural_section = (
        "\n".join(f"  - {w}" for w in structural_warnings)
        if structural_warnings
        else "  All required sections present."
    )

    report = f"""# Safety Review Report

**Issue Draft:** {draft_path.name}
**Review Date:** {today}
**Overall Safety Score:** {score}/10
**Minimum Threshold:** {SAFETY_THRESHOLD}/10
**Status:** [{status_marker}] {status}

---

## Summary

- Total risky phrases found: {len(findings)}
- High severity: {len(high)}
- Medium severity: {len(medium)}
- Low severity: {len(low)}
- Total score deduction: -{sum(f['deduction'] for f in findings):.1f}
- Final safety score: {score}/10

---

## High Severity Findings (−2 points each)

{high_section}

---

## Medium Severity Findings (−1 point each)

{medium_section}

---

## Low Severity Findings (−0.5 points each)

{low_section}

---

## Structural Checks

{structural_section}

---

## Decision

{'**APPROVED:** Safety score meets the minimum threshold. The newsletter may proceed to distribution via send_newsletter_email.py.' if score >= SAFETY_THRESHOLD else f'**BLOCKED:** Safety score {score}/10 is below the required threshold of {SAFETY_THRESHOLD}/10. Manual review and revision are required before distribution. Address all high and medium severity findings above.'}

---

*Generated by safety_scan.py | Middle Corridor Brief*
*{today}*
"""

    SAFETY_REVIEW_DIR.mkdir(exist_ok=True)
    report_filename = f"safety_review_{draft_path.stem}_{timestamp}.md"
    report_path = SAFETY_REVIEW_DIR / report_filename
    report_path.write_text(report, encoding="utf-8")

    return report, report_path


def main(draft_path_arg: str | None = None) -> bool:
    """
    Run safety scan. Returns True if safe to distribute, False if blocked.
    Accepts optional draft path argument; otherwise scans the most recent draft.
    """
    print("=" * 60)
    print("Middle Corridor Brief — Safety Scanner")
    print("=" * 60)

    if draft_path_arg:
        draft_path = Path(draft_path_arg)
    else:
        drafts = sorted(DRAFTS_DIR.glob("draft_issue_*.md"))
        if not drafts:
            sys.exit("ERROR: No draft files found in /drafts. Run generate_weekly_brief.py first.")
        draft_path = drafts[-1]
        print(f"Scanning most recent draft: {draft_path.name}")

    text = load_draft(draft_path)
    print(f"Draft loaded: {len(text)} characters, {len(text.splitlines())} lines\n")

    print("Scanning for risky phrases...")
    findings = scan_for_risky_phrases(text)
    print(f"Found {len(findings)} risky phrase occurrence(s).")

    structural_warnings = check_structural_elements(text)
    if structural_warnings:
        print(f"Structural warnings: {len(structural_warnings)}")

    score = calculate_safety_score(findings)
    print(f"\nSafety Score: {score}/10 (threshold: {SAFETY_THRESHOLD}/10)")

    report_content, report_path = generate_report(draft_path, findings, score, structural_warnings)

    print(f"Safety review report saved: {report_path}")

    if score >= SAFETY_THRESHOLD:
        print(f"\n[PASS] Newsletter approved for distribution.")
        return True
    else:
        print(f"\n[FAIL] Newsletter BLOCKED. Score {score}/10 is below threshold {SAFETY_THRESHOLD}/10.")
        print("Please address the findings in the safety review report before distributing.")
        return False


if __name__ == "__main__":
    draft_arg = sys.argv[1] if len(sys.argv) > 1 else None
    safe = main(draft_arg)
    sys.exit(0 if safe else 1)
