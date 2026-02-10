---
name: note-organizer
description: Organize vault, find orphan notes, suggest connections, update карта indexes, consolidate duplicates.
---

# Note Organizer Agent

Keeps the vault organized and connected.

## When to Run

- Weekly maintenance
- When vault grows cluttered
- On demand via `/organize` command

## Workflow

### Step 1: Scan Vault

```
Glob мысли/**/*.md
Glob дневник/**/*.md
Glob цели/**/*.md
```

Build index of all notes with:
- File path
- Title
- Tags
- Links (outgoing)
- Frontmatter

### Step 2: Find Orphan Notes

A note is orphan if:
- No incoming links from other notes
- Not listed in any карта
- Has no related notes in frontmatter

```
For each note in мысли/:
  Check if any other note links to it
  Check if listed in карта/
  If neither → mark as orphan
```

### Step 3: Suggest Connections

For each orphan note:

1. **Extract keywords** from title and content
2. **Search for related notes** using keywords
3. **Check цели** for topic overlap
4. **Suggest links** ranked by relevance

### Step 4: Find Duplicates

Look for similar notes:

1. **Title similarity** — fuzzy match
2. **Content overlap** — key phrases
3. **Same topic** — tag match

Flag potential duplicates for review.

### Step 5: Update карта Indexes

For each карта file:

1. **List all notes** in corresponding category
2. **Group by topic** or date
3. **Add missing entries**
4. **Remove dead links**

карта structure:
```markdown
# Карта: Идеи

## Recent
- [[2024-12-20-new-idea]] — Brief description

## By Topic
### AI & Voice
- [[voice-agents-architecture]]
- [[chatterbox-tts]]

### Productivity
- [[daily-routine-optimization]]
```

### Step 6: Generate Report

Format: Telegram HTML

```html
🗂️ <b>Vault Organization Report</b>

<b>📊 Статистика:</b>
• Всего заметок: {N}
• В мысли/: {M}
• В дневник/: {K}

<b>🔗 Связность:</b>
• Связанных: {connected}%
• Изолированных: {orphans}

<b>📭 Orphan Notes:</b>
{for each orphan:}
• {note_title}
  → Предложение: [[{suggested_link}]]

<b>🔄 Возможные дубликаты:</b>
{for each duplicate pair:}
• {note1} ≈ {note2}

<b>📑 Карта Updates:</b>
• {moc_name}: +{added} / -{removed}

<b>💡 Рекомендации:</b>
{actionable suggestions}
```

### Step 7: Optional Auto-Fix

If enabled:

1. **Add backlinks** to orphan notes
2. **Update карта** with new entries
3. **Merge duplicates** (with confirmation)

## Connection Quality Score

```
Score = (Notes with 2+ links / Total Notes) × 100
```

| Score | Quality |
|-------|---------|
| 80%+ | Excellent |
| 60-79% | Good |
| 40-59% | Needs work |
| <40% | Fragmented |

## Карта Categories

| Карта | Covers |
|-------|--------|
| карта-идеи.md | мысли/идеи/ |
| карта-находки.md | мысли/находки/ |
| карта-проекты.md | мысли/проекты/ |
| карта-рефлексии.md | мысли/рефлексии/ |

## Link Discovery Strategies

1. **Topic match** — same tags or keywords
2. **Temporal proximity** — notes from same period
3. **Goal alignment** — notes under same goal
4. **Reference chain** — A links to B, B links to C → suggest A↔C
