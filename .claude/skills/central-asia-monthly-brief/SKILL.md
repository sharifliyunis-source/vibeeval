---
name: central-asia-monthly-brief
description: Produce this month's Central Asia Monthly Intelligence Brief by running the coordinator → analyst pipeline and compiling the result. Use when the user invokes /central-asia-monthly-brief, asks for "this month's Central Asia brief," or a monthly reminder Routine fires asking for that month's edition.
---

# Central Asia Monthly Intelligence Brief

This skill is the deterministic entry point into the Central Asia intelligence agent team. It exists so the monthly reminder Routine (and the user, on demand) has one reliable command rather than relying on fuzzy subagent auto-matching.

## What it does

1. **Check for user-supplied source material first.** Look at the current conversation for news, links, or documents the user has already shared for this reporting month.
   - If present: that material is the primary input for this edition.
   - If absent: this run will need to research independently via web search (only do this if the user has confirmed that's fine for this edition — the standing arrangement is that the user supplies monthly material themselves, and independent research is the exception, not the default).
2. **Invoke `central-asia-intelligence-coordinator`** (via the Task/Agent tool), passing it:
   - The reporting month (default: current month).
   - Whichever source material was found in step 1, or an explicit instruction to research independently if none was found and that's been confirmed.
3. The coordinator internally commissions `geopolitical-analyst` and `geoeconomic-analyst` in parallel, then `political-risk-analyst` (which needs both of their outputs), and compiles the final document.

## Output structure (fixed — the coordinator enforces this)

1. Title + reporting month
2. **Executive Summary** (top)
3. Geopolitical Landscape
4. Geoeconomic Landscape
5. Political Risk Assessment — Threats & Opportunities for Private Sector (covers both current operators and prospective entrants)
6. **Strategic Implications** (end)

## Output location

`reports/central-asia/central-asia-intelligence-brief-<YYYY-MM>.md`

## Scope

Country coverage is fixed to the core five: Kazakhstan, Uzbekistan, Turkmenistan, Kyrgyzstan, Tajikistan. All sections must stay balanced and objective — sourced claims, fact separated from analysis, no partisan framing of any government or power bloc.
