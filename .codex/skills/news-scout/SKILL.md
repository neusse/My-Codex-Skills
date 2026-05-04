---
name: news-scout
description: Finds and summarizes high-signal recent news for a defined topic, company, or watchlist.
---

# Trigger
Use this skill when the user asks for recent news updates, market-moving headlines, watchlist monitoring, or a concise news brief.

# Workflow
1. Confirm scope: symbols/topics, time window, geography, and desired output format.
2. Gather recent items from credible primary sources and high-signal financial/industry sources.
3. Filter noise, deduplicate overlapping headlines, and prioritize event-level developments.
4. Produce a concise brief with exact dates, sources, and clearly separated interpretation.
5. End with follow-up watch items the user may want monitored next.

# Output
- Headline list with source and publication date.
- 3-5 key takeaways tied to potential impact.
- Watchlist of unresolved items or upcoming catalysts.

# Requirements
- Include exact dates (no ambiguous "today/yesterday" without a date).
- Distinguish facts from inference in the summary.
- Keep summaries concise, actionable, and bias-aware.
- Prefer primary sources where possible for high-impact claims.

# Guardrails
- Do not present speculation as confirmed facts.
- Do not omit source attribution for material claims.
- Flag low-confidence items and conflicting reports explicitly.
