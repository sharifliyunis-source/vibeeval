# Middle Corridor Brief

## A Personal Research Intelligence Workflow

---

## Project Purpose

Middle Corridor Brief is an AI-assisted research operating system that tracks, analyzes, and publishes weekly executive-grade intelligence briefs on the Trans-Caspian International Transport Route (TITR), commonly known as the Middle Corridor.

The project produces one high-quality LinkedIn newsletter per week, structured as an executive intelligence brief combining development finance analysis, infrastructure tracking, and geoeconomic research.

---

## Strategic Thesis

> The Middle Corridor is no longer only a transit route. It is emerging as a multi-layered connectivity platform linking logistics, green energy, conventional energy exports, and digital infrastructure across Eurasia.

The corridor must be understood across four integrated layers:

| Layer | Description |
|---|---|
| **Transit and Logistics** | Rail, ports, Caspian shipping, customs facilitation, dry ports, multimodal infrastructure |
| **Green Energy Corridor** | Renewable energy projects, electricity transmission, green hydrogen discussions, grid interconnection |
| **Fossil Fuel Export Corridor** | Oil, gas, and petrochemical export infrastructure connecting Central Asia, the Caspian, Türkiye, and Europe |
| **Digital Corridor** | Fiber optic cables (including Caspian fiber optic cable project), telecom cooperation, digital trade infrastructure |

Development finance and investment flows are tracked across all four layers as a fifth analytical dimension.

---

## Output Format

Each weekly issue is structured as an **executive intelligence brief** resembling:

- Executive-grade strategic connectivity research
- Development finance analysis
- Institutional-grade geoeconomic analysis

**Not:**
- Political commentary
- Activist writing
- Sensational journalism
- Ideological analysis
- Security or military analysis

---

## Safety and Positioning Rules

### Approved Tone
- Executive, neutral, factual, evidence-based
- Development-oriented and institutionally safe
- Professional, analytical, concise

### Approved Framing
- Connectivity diversification
- Trade route resilience
- Infrastructure modernization
- Regional integration
- Multimodal connectivity
- Energy connectivity
- Digital integration
- Supply chain adjustment
- Commercial route development
- Development finance coordination

### Prohibited Framing
- Sanctions evasion or sanctions-sensitive language
- Anti-Russia, anti-China, or anti-West framing
- Military or security-heavy language
- Regime criticism or geopolitical weapon narratives
- Strategic encirclement or great power competition framing
- Speculative intelligence-style claims

---

## Multi-Agent Workflow

The research system uses eight specialized analytical agents:

| Agent | Specialization |
|---|---|
| Agent 1 | Logistics and Transit Analyst |
| Agent 2 | Green Energy Corridor Analyst |
| Agent 3 | Fossil Fuel Export Corridor Analyst |
| Agent 4 | Digital Corridor Analyst |
| Agent 5 | Policy and Private Sector Impact Analyst |
| Agent 6 | Editorial and Safety Reviewer |
| Agent 7 | Newsletter Editor |
| Agent 8 | Strategic Synthesis Agent |

Each agent produces structured weekly outputs reviewed by Agent 6 before Agent 7 compiles the final newsletter.

---

## Weekly Operating Routine

| Day | Task |
|---|---|
| **Monday** | Collect developments and sources |
| **Tuesday** | Update the research database (`middle_corridor_tracker.csv`) |
| **Wednesday** | Identify the strongest strategic theme for the week |
| **Thursday** | Generate first newsletter draft using `generate_weekly_brief.py` |
| **Friday** | Run safety review (`safety_scan.py`), finalize, and distribute |
| **Weekend** | Archive the issue, prepare next topic |

---

## Folder Structure

```
/sources          — Raw source materials and links
/data             — Structured research database (CSV tracker)
/agents           — Agent role definitions and instructions
/agent_outputs    — Weekly structured findings per agent
/drafts           — Working newsletter drafts
/published        — Final published newsletter versions
/templates        — Newsletter and agent output templates
/visuals          — Charts, maps, and data visualizations
/scripts          — Python automation scripts
/weekly_briefs    — Final weekly newsletter files
/safety_review    — Safety review reports
```

---

## Key Files

| File | Purpose |
|---|---|
| `/data/middle_corridor_tracker.csv` | Central research database |
| `/agents/agent_roles.md` | Agent definitions and responsibilities |
| `/templates/newsletter_template.md` | Standard newsletter structure |
| `/templates/weekly_agent_output_template.md` | Agent output structure |
| `/safety_review/safe_language_checklist.md` | Risky phrases and safer alternatives |
| `/scripts/generate_weekly_brief.py` | Automates newsletter draft generation |
| `/scripts/safety_scan.py` | Scans drafts for risky language |
| `/scripts/send_newsletter_email.py` | Distributes final newsletter by email |

---

## Publication Process

1. Agents produce structured findings
2. Agent 6 performs safety review
3. Agent 7 integrates findings into final newsletter
4. `safety_scan.py` runs automated language check
5. If safety score passes, `send_newsletter_email.py` distributes to recipient
6. Issue is archived in `/published` and `/weekly_briefs`

---

*This is a personal research project. Views expressed are solely those of the author and do not represent any institutional position.*
