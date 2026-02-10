---
paths: "мысли/**/*.md"
---

# Thoughts Format

Rules for notes in `мысли/` folder and its subfolders.

## Folder Structure

```
мысли/
├── идеи/       # Creative ideas, concepts
├── рефлексии/  # Personal reflections, lessons
├── проекты/    # Project-related notes
└── находки/    # Knowledge, discoveries
```

## File Naming

- Format: `YYYY-MM-DD-slug.md`
- Slug: lowercase, hyphens, descriptive
- Example: `2024-12-20-voice-agent-architecture.md`

## Frontmatter (Required)

```yaml
---
date: 2024-12-20
type: idea | reflection | project | learning
tags: [relevant, tags]
source: дневник/2024-12-20.md
related: []
---
```

## Content Structure

```markdown
# Title

## Summary
One paragraph summary of the key insight.

## Details
Full content of the thought.

## Action Items
- [ ] Any tasks that emerged
- [ ] Follow-up actions

## Related
- [[Link to related note]]
- [[цели/1-год-2026#Section]]
```

## Tags Convention

Use hierarchical tags:

```
#type/idea
#type/learning
#topic/ai
#topic/productivity
#project/d-brain
#status/active
```

## Wiki-Links

When saving a thought:

1. **Search for related notes** in мысли/
2. **Check карта/ indexes** for topic clusters
3. **Link to relevant goals** in цели/
4. **Add backlinks** to source daily note

Example:
```markdown
Extracted from [[дневник/2024-12-20]].
Related to [[Voice Agents]] and [[цели/1-год-2026#AI Development]].
```

## Category Guidelines

### идеи/
- Novel concepts, inventions
- Business ideas
- Creative solutions
- "What if..." thoughts

### рефлексии/
- Personal insights
- Lessons learned
- Emotional processing
- Gratitude, wins

### проекты/
- Project-specific notes
- Meeting notes
- Status updates
- Decisions made

### находки/
- New knowledge
- Book/article insights
- Technical discoveries
- "TIL" moments
