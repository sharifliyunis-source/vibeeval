"""
Generate Weekly Brief
Reads middle_corridor_tracker.csv, filters high-relevance entries,
groups by Corridor Layer, and generates a Markdown newsletter draft.
"""

import csv
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "middle_corridor_tracker.csv"
TEMPLATE_FILE = ROOT / "templates" / "newsletter_template.md"
OUTPUT_DIR = ROOT / "weekly_briefs"
DRAFTS_DIR = ROOT / "drafts"

# ── Config ─────────────────────────────────────────────────────────────────────
MIN_RELEVANCE_SCORE = 4

LAYER_ORDER = [
    "Transit and Logistics",
    "Green Energy",
    "Fossil Fuel Export",
    "Digital Connectivity",
]

LAYER_HEADINGS = {
    "Transit and Logistics": "Transit and Logistics",
    "Green Energy": "Green Energy Corridor",
    "Fossil Fuel Export": "Fossil Fuel Export Corridor",
    "Digital Connectivity": "Digital Corridor",
}


def load_tracker(filepath: Path) -> list[dict]:
    """Load and validate the tracker CSV."""
    if not filepath.exists():
        sys.exit(f"ERROR: Tracker file not found at {filepath}")
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    print(f"Loaded {len(rows)} rows from tracker.")
    return rows


def filter_rows(rows: list[dict], min_score: int) -> list[dict]:
    """Keep only rows with Newsletter Relevance Score >= min_score."""
    filtered = []
    for row in rows:
        try:
            score = int(row.get("Newsletter Relevance Score", "0").strip())
        except ValueError:
            score = 0
        if score >= min_score:
            filtered.append(row)
    print(f"Filtered to {len(filtered)} rows with relevance score >= {min_score}.")
    return filtered


def group_by_layer(rows: list[dict]) -> dict[str, list[dict]]:
    """Group filtered rows by Corridor Layer."""
    grouped: dict[str, list[dict]] = {layer: [] for layer in LAYER_ORDER}
    for row in rows:
        layer = row.get("Corridor Layer", "").strip()
        if layer in grouped:
            grouped[layer].append(row)
        else:
            print(f"WARNING: Unknown corridor layer '{layer}' — row skipped.")
    return grouped


def format_entry(row: dict) -> str:
    """Format one tracker row as a newsletter subsection."""
    project = row.get("Project/Event", "").strip()
    country = row.get("Country", "").strip()
    date = row.get("Date", "").strip()
    actors = row.get("Key Actors", "").strip()
    implication = row.get("Potential Implication", "").strip()
    finance = row.get("Investment/Finance Relevance", "").strip()
    source_title = row.get("Source Title", "").strip()
    source_link = row.get("Source Link", "").strip()
    confirmed = row.get("Confirmed Fact", "").strip()
    safe_note = row.get("Safe Language Note", "").strip()

    lines = [
        f"**{project}**",
        f"*{country} | {date}*",
        "",
        f"{implication}" if implication else "",
        "",
        f"**Key actors:** {actors}" if actors else "",
        f"**Finance relevance:** {finance}" if finance else "",
        f"**Confirmed:** {confirmed}" if confirmed else "",
    ]
    if safe_note:
        lines += ["", f"*Language note: {safe_note}*"]
    if source_title:
        link_text = f"[{source_title}]({source_link})" if source_link else source_title
        lines += ["", f"**Source:** {link_text}"]

    return "\n".join(line for line in lines if line is not None)


def build_layer_section(layer: str, rows: list[dict]) -> str:
    """Build the Markdown section for one corridor layer."""
    heading = LAYER_HEADINGS.get(layer, layer)
    if not rows:
        return f"## {heading}\n\n*No significant developments tracked this week.*\n"

    entries = "\n\n---\n\n".join(format_entry(r) for r in rows)
    return f"## {heading}\n\n{entries}\n"


def get_issue_number() -> int:
    """Determine the next issue number from existing files."""
    existing = list(OUTPUT_DIR.glob("issue_*.md")) + list(DRAFTS_DIR.glob("draft_issue_*.md"))
    numbers = []
    for f in existing:
        parts = f.stem.replace("draft_", "").replace("issue_", "")
        try:
            numbers.append(int(parts.split("_")[0]) if "_" in parts else int(parts))
        except ValueError:
            pass
    return max(numbers, default=0) + 1


def build_newsletter(grouped: dict[str, list[dict]], issue_number: int) -> str:
    """Assemble the full newsletter Markdown."""
    today = datetime.today().strftime("%Y-%m-%d")
    week_label = datetime.today().strftime("Week of %B %d, %Y")

    header = f"""# Middle Corridor Brief | Weekly Issue #{issue_number}

**Publication Date:** {today}
**{week_label}**

---

*Disclaimer: This newsletter is a personal research publication. The views expressed are solely those of the author and do not represent any institutional, governmental, or organizational position. All information is drawn from publicly available sources cited throughout.*

---

## Executive Summary

*[DRAFT — To be completed by Agent 7 after reviewing all layer sections below.]*

The developments tracked this week across the Middle Corridor reinforce its evolution as a multi-layered connectivity platform. Significant progress is observed across transit infrastructure, energy connectivity, and digital integration, supported by active development finance engagement from multilateral institutions.

---

## Main Argument

The Middle Corridor continues its transition from a single-purpose transit route into an integrated Eurasian connectivity platform. This week's findings demonstrate coordinated progress across logistics, energy, and digital dimensions — each layer reinforcing the others and collectively expanding the corridor's strategic and commercial relevance.

---

"""

    layer_sections = "\n\n".join(
        build_layer_section(layer, grouped[layer]) for layer in LAYER_ORDER
    )

    footer = f"""

---

## Why It Matters

The developments documented in this issue collectively advance the corridor's profile as a commercially viable and institutionally supported connectivity platform. Infrastructure modernization across multiple layers, combined with sustained multilateral financing engagement, positions the Middle Corridor as a significant long-term development opportunity for the Eurasian region.

---

## What to Watch Next

- **EBRD Board meetings:** Monitor for new transport or energy project approvals linked to corridor countries
- **BTK rail volumes:** Watch monthly throughput data for block train services
- **Trans-Caspian fiber optic project:** Track feasibility study publication timeline
- **Green energy MOUs:** Monitor for binding agreements following recent frameworks
- **Kuryk port construction:** Track construction milestone announcements

---

*Generated by generate_weekly_brief.py | Middle Corridor Brief*
*Issue #{issue_number} | {today}*
"""

    return header + layer_sections + footer


def save_draft(content: str, issue_number: int) -> Path:
    """Save the draft to /drafts and a copy to /weekly_briefs."""
    DRAFTS_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    today = datetime.today().strftime("%Y%m%d")
    draft_path = DRAFTS_DIR / f"draft_issue_{issue_number:03d}_{today}.md"
    brief_path = OUTPUT_DIR / f"issue_{issue_number:03d}_{today}.md"

    draft_path.write_text(content, encoding="utf-8")
    brief_path.write_text(content, encoding="utf-8")

    print(f"Draft saved: {draft_path}")
    print(f"Brief saved: {brief_path}")
    return draft_path


def main():
    print("=" * 60)
    print("Middle Corridor Brief — Weekly Brief Generator")
    print("=" * 60)

    rows = load_tracker(DATA_FILE)
    filtered = filter_rows(rows, MIN_RELEVANCE_SCORE)
    grouped = group_by_layer(filtered)

    for layer, entries in grouped.items():
        print(f"  {layer}: {len(entries)} entries")

    issue_number = get_issue_number()
    print(f"\nGenerating Issue #{issue_number}...")

    newsletter = build_newsletter(grouped, issue_number)
    draft_path = save_draft(newsletter, issue_number)

    print("\nGeneration complete.")
    print(f"Next step: Run safety_scan.py on {draft_path}")
    return str(draft_path)


if __name__ == "__main__":
    main()
