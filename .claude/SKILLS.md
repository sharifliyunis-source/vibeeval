# Skills & Agents

## Agents

Stored in `.claude/agents/` — invoke with `@agent-name` or natural language.

| Agent | Description | Invoke |
|-------|-------------|--------|
| [strategist](agents/strategist.md) | Always-on strategic advisor. Analyzes projects, spots risks/opportunities, runs at session start. | `@strategist what should I prioritize?` |
| [academic-paper-reviewer](agents/academic-paper-reviewer.md) | Full journal peer review simulation: 5 reviewers (EIC + 3 peer + Devil's Advocate) with 6 modes. | `@academic-paper-reviewer review this paper` |

---

## Adding a New Agent

1. Create `.claude/agents/<name>.md`
2. Add frontmatter:
   ```yaml
   ---
   name: your-agent-name
   description: "One sentence — when should Claude delegate to this agent?"
   tools: [Read, Write, Bash, ...]
   model: sonnet  # or opus / haiku
   ---
   ```
3. Write the system prompt below the frontmatter.

## Adding a New Skill

1. Create `.claude/skills/<name>.md`
2. Add frontmatter:
   ```yaml
   ---
   name: your-skill-name
   description: "What this skill does and when to trigger it"
   ---
   ```
3. Write the skill instructions below the frontmatter.
4. Invoke with `/your-skill-name` or via the Skill tool.
