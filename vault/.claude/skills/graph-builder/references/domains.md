# Domain Configuration

Domains define the organizational structure of the vault. Each domain has specific linking rules and priorities.

## Core Domains

### дневник/
**Purpose:** Daily journal entries, raw captures
**Format:** `YYYY-MM-DD.md`
**Linking:**
- Outgoing to мысли/ when content is processed
- Outgoing to проекты/ when project mentioned
- Should reference карта for categorization

### мысли/
**Purpose:** Processed and refined ideas
**Subdirectories:**
- `идеи/` — Creative concepts, innovations
- `рефлексии/` — Personal insights, lessons learned
- `находки/` — Knowledge captured from reading/experience
- `проекты/` — Project-specific notes

**Linking:**
- Incoming from дневник/ (source entries)
- Outgoing to карта/ (categorization)
- Cross-links within мысли/ (related concepts)

### цели/
**Purpose:** Goal hierarchy and tracking
**Files:**
- `0-видение-3г.md` — Long-term vision
- `1-год-YYYY.md` — Annual goals
- `2-месяц.md` — Monthly priorities
- `3-неделя.md` — Weekly focus

**Linking:**
- Incoming from мысли/ (ideas aligned with goals)
- Incoming from дневник/ (progress updates)
- Should be highly connected as navigation hubs

### карта/
**Purpose:** Maps of Content — index pages
**Linking:**
- Incoming from all domains (everything should have a карта)
- Outgoing to related карта
- Central navigation hubs

### проекты/
**Purpose:** Active project documentation
**Linking:**
- Incoming from дневник/ (work logs)
- Incoming from мысли/ (related ideas)
- Outgoing to цели/ (alignment)

## Link Priority Rules

When suggesting links, prioritize:

1. **Orphan → Карта** — Every note should belong to a Map of Content
2. **Дневник → Мысль** — Processed entries link to their refined notes
3. **Мысль → Цель** — Ideas should align with goals
4. **Cross-domain** — Bridge related concepts across domains

## Custom Domains

Add custom domains by creating subdirectories and documenting them here:

```markdown
### your-domain/
**Purpose:** Description
**Linking:** Rules for incoming/outgoing links
```

## Entity Patterns

Common patterns to detect for auto-linking:

- `[[Note Name]]` — Existing wiki-links
- `@mention` — People/contacts (if contacts domain exists)
- `#tag` — Tags that may map to notes
- Project names — Match against проекты/ directory
- Dates — Link to дневник/ entries
