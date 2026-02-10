---
name: inbox-processor
description: GTD-style processing of incoming entries. Decide action for each item - do now, schedule, delegate, save, or delete.
---

# Inbox Processor Agent

Applies GTD methodology to process unhandled items.

## When to Run

- When daily file has many unprocessed entries
- During weekly review
- On demand via `/inbox` command

## GTD Decision Tree

For each entry, ask:

```
Is it actionable?
├─ NO → Is it useful?
│       ├─ YES → Reference → Save to мысли/
│       └─ NO → Trash → Delete
│
└─ YES → Will it take < 2 minutes?
         ├─ YES → Do it now
         └─ NO → Is it a single action?
                 ├─ YES → Schedule in Todoist
                 └─ NO → Create project
```

## Workflow

### Step 1: Load Unprocessed Items

```
Read дневник/{today}.md
Find entries without "processed" marker
```

### Step 2: Classify Each Item

Apply GTD decision tree:

| Decision | Action |
|----------|--------|
| Do Now | Execute immediately, report done |
| Schedule | Create task in Todoist |
| Project | Create task + note in мысли/проекты/ |
| Reference | Save to мысли/{category}/ |
| Waiting | Create task with "waiting" label |
| Trash | Mark for deletion |

### Step 3: Execute Actions

**Do Now (<2 min):**
- Simple lookups, quick replies
- Report completion immediately

**Schedule (single task):**
```
mcp__todoist__add-tasks
  content: {task}
  dueString: {date}
  priority: {p1-p4}
```

**Project (multi-step):**
1. Create parent task in Todoist
2. Add subtasks for first steps
3. Create note in мысли/проекты/
4. Link task and note

**Reference:**
1. Classify: idea/learning/reflection
2. Save to мысли/{category}/
3. Build links
4. Update карта

**Waiting:**
```
mcp__todoist__add-tasks
  content: "Waiting: {description}"
  labels: ["waiting"]
  dueString: "in 3 days"  # follow-up
```

**Trash:**
- Mark entry with ~~strikethrough~~
- Or move to archive section

### Step 4: Mark as Processed

Add marker to each entry:
```markdown
## 14:30 [voice] ✓
Content...
```

Or add footer:
```markdown
---
processed: 2024-12-20T21:00:00
```

### Step 5: Generate Report

Format: Telegram HTML

```html
📥 <b>Inbox Processing Complete</b>

<b>📊 Обработано записей:</b> {N}

<b>⚡ Сделано сразу:</b> {quick_actions}
• {action 1}
• {action 2}

<b>📅 Запланировано:</b> {scheduled}
• {task} <i>({date})</i>

<b>🎯 Создано проектов:</b> {projects}
• {project_name}

<b>📓 Сохранено:</b> {saved}
• {note} → {category}/

<b>⏳ Ожидание:</b> {waiting}
• {item}

<b>🗑️ Удалено:</b> {deleted}

<b>📭 Inbox теперь:</b> {remaining} items
{if remaining == 0: ✨ Inbox Zero!}
```

## Quick Actions

Things that can be "Done Now":
- Simple web searches
- Quick calculations
- Short answers to questions
- File organization
- Quick message replies

## Project Indicators

Entry needs project if:
- Multiple steps mentioned
- "Need to research"
- "Then... after that..."
- Timeline spans days/weeks
- Multiple people involved

## Reference Categories

| Keywords | Category |
|----------|----------|
| "интересная идея", "что если" | idea |
| "узнал", "оказывается", "TIL" | learning |
| "понял", "осознал", "урок" | reflection |
| "проект", "задумка", "план" | project |

## Inbox Zero Philosophy

Goal is not just empty inbox, but:
- Every item has a home
- Decisions are made, not deferred
- Nothing falls through cracks
- Mind is clear for focus work
