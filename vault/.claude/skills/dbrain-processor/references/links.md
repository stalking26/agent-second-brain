# Wiki-Links Building

## Purpose

Build connections between notes to create a knowledge graph.

## When Saving a Thought

### Step 1: Search for Related Notes

Search мысли/ for related content:

```
Grep "keyword1" in мысли/**/*.md
Grep "keyword2" in мысли/**/*.md
```

Keywords to search:
- Main topic of the thought
- Key entities (people, projects, technologies)
- Domain terms

### Step 2: Check MOC Indexes

Read relevant MOC files:

```
карта/
├── карта-идеи.md
├── карта-проекты.md
├── карта-находки.md
└── карта-рефлексии.md
```

Find related entries.

### Step 3: Link to Goals

Check if thought relates to goals:

```
Read цели/1-год-2026.md
Find matching goal areas
```

### Step 4: Add Links to Note

In the thought file, add:

**In frontmatter:**
```yaml
related:
  - "[[мысли/идеи/2024-12-15-voice-agents.md]]"
  - "[[цели/1-год-2026#AI Development]]"
```

**In content (inline):**
```markdown
This connects to [[Voice Agents Architecture]] we explored earlier.
```

**In Related section:**
```markdown
## Related
- [[Previous related thought]]
- [[Project this belongs to]]
- [[Goal this supports]]
```

### Step 5: Update MOC Index

Add new note to appropriate MOC:

```markdown
# Карта: Идеи

## Recent
- [[мысли/идеи/2024-12-20-new-idea.md]] — Brief description

## By Topic
### AI & Voice
- [[мысли/идеи/2024-12-20-new-idea.md]]
- [[мысли/идеи/2024-12-15-voice-agents.md]]
```

### Step 6: Add Backlinks

In related notes, add backlink to new note if highly relevant.

## Link Format

### Internal Links
```markdown
[[Note Name]]                    # Simple link
[[Note Name|Display Text]]       # With alias
[[folder/Note Name]]             # With path
[[Note Name#Section]]            # To heading
```

### Link to Goals
```markdown
[[цели/1-год-2026#Career & Business]]
[[цели/3-неделя]] — ONE Big Thing
```

## Report Section

Track new links created:

```
<b>🔗 Новые связи:</b>
• [[Note A]] ↔ [[Note B]]
• [[New Thought]] → [[Related Project]]
```

## Example Workflow

<!-- Это пример — замените на свои реальные темы -->
New thought: "Новый инструмент X можно использовать для проекта Y"

1. **Search:**
   - Grep "keyword" in мысли/ → finds related notes
   - Grep "tool" in мысли/ → no results

2. **Check MOC:**
   - карта-находки.md has relevant section

3. **Goals:**
   - 1-год-2026.md has matching goal

4. **Create links:**
   ```yaml
   related:
     - "[[мысли/идеи/related-note.md]]"
     - "[[цели/1-год-2026#Your Goal]]"
   ```

5. **Update карта-находки.md:**
   ```markdown
   ### Your Category
   - [[мысли/находки/2024-12-20-new-learning.md]] — Description
   ```

6. **Report:**
   ```
   <b>🔗 Новые связи:</b>
   • [[New Note]] ↔ [[Related Note]]
   ```

## Orphan Detection

A note is "orphan" if:
- No incoming links from other notes
- No related notes in frontmatter
- Not listed in any карта

Flag orphans for review:
```
<b>⚠️ Изолированные заметки:</b>
• [[мысли/идеи/orphan-note.md]]
```
