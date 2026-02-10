---
date: 2026-02-10
type: learning
tags: [voice-processing, prompts, LLM, transcript, STT, tools, AI-tools]
linked: [[Second Brain Processor]], [[Лаборатория AI]], [[Obsidian]]
---

# Обработка голосовых транскрипций: промпты, инструменты, техники

## Summary

Исчерпывающее исследование: как чистить голосовые транскрипции с помощью LLM (Claude, GPT), какие промпты использовать, какие open-source инструменты существуют, и как извлекать структуру из хаотичной речи. Всё готово к копированию и применению.

---

## 1. Базовый промпт для чистки транскрипции

### Минимальный (проверенный на Claude)

```
Clean up this voice transcription. Remove any filler words, typos and correct
any words that are not in the context. If I correct myself, only include the
corrected version. Only output the cleaned transcript, do not say anything
like "Here is the cleaned up transcript" in the beginning.
```

Источник: [Shing Lyu — Using LLM to get cleaner voice transcriptions](https://shinglyu.com/ai/2024/01/17/using-llm-to-get-cleaner-voice-transcriptions.html)

### Продвинутый (с сохранением голоса автора)

```
Objective: Edit the transcript for grammar, spelling, punctuation.

Instructions:
1. Remove all timestamps
2. Fix grammatical errors and punctuation (capitalize proper nouns, sentences)
3. Remove filler words ("um," "uh," "like," "you know," "ну," "это," "вот,"
   "короче," "типа," "в общем")
4. Do NOT condense the content — preserve ALL speaker's thoughts and viewpoints
5. Maintain conversational flow, pauses, interruptions
6. Preserve the speaker's unique voice and style
7. Add bracketed notes [unclear] for ambiguous phrasing
8. Keep existing emphasis (bold/italic)
```

Источник: [Scott King — How to Clean Up Raw Transcriptions](https://thescottking.com/how-to-clean-up-raw-transcriptions)

---

## 2. Полноценный system prompt для STT-чистки (копируй и используй)

Из проекта danielrosehill/STT-Basic-Cleanup-System-Prompt (MIT лицензия):

```
Your task is to take text provided by the user and improve it for flow
and accuracy.

The text was captured using speech-to-text software. You can expect that
it will contain common deficiencies of STT generated text such as pause
words that were not removed, missing punctuation, and missing paragraphs.
You should fix these for the user.

You may also be able to infer obvious typos. For example, the transcript
you receive might contain something like: "I am using Ollama with LLAMA
3.2". You would rewrite this to: "I am using Ollama with Llama 3.2".
If you encounter these, you should remediate them.

The text which the user provides may contain a mixture of instructions
for editing and content to be added to the text. Adhere precisely to
the instructions provided by the user and use those in writing the
edited version.

Here are some further editing instructions you must adhere to:

- Break up the text into short readable paragraphs of ideally no more
  than 3 sentences per paragraph.
- Improve the text for flow and coherence.
- Add subheadings to the text. Subheadings should capture the essence
  of the forthcoming text, but do not add more than one subheading
  every 400 words.

In your editing you should:
- Preserve the content of the text provided by the user.
- Preserve the uniqueness of their voice and perspective.

In your editing you should not:
- Surpass the scope of these editing instructions.
- Change the content of the text provided by the user or its tone/style.

Your objective is to take the raw text provided by the user and return
it in an improved and easier to read fashion with defects remedied.

After applying all these edits you must return the edited text to the
user. Do not add any preface or suffix to the text including friendly
messages. Simply provide the full text in your response without
additional commentary.
```

Источник: [GitHub — danielrosehill/STT-Basic-Cleanup-System-Prompt](https://github.com/danielrosehill/STT-Basic-Cleanup-System-Prompt)

Дополнительно: [Speech-To-Text-System-Prompt-Library](https://github.com/danielrosehill/Speech-To-Text-System-Prompt-Library) — целая библиотека промптов для STT (business, academic, casual, technical стили).

---

## 3. Двухпроходная техника: Voice Memo -> Structured Markdown

### Промпт 1: Структуризация (из хаоса в буллеты)

```
Take this raw voice transcript and transform it into bullet-point form
with nested structure.

Rules:
- Extract ALL points without omission — this is structuring, not summarization
- Use markdown * bullets with nested levels for logical organization
- Include substantive topic titles (avoid generic catch-alls)
- Write in first person using complete sentences
- Regroup scattered topics so related content flows together
- Ignore sound descriptions and introductory remarks
- Replace awkward phrasing with natural language
- Remove filler words and self-corrections
```

### Промпт 2: Логическая переупорядочка

```
Reorganize the structured output for better flow:

- Reorder sections using hierarchy: personal → relationships → work → broader
- Combine similar topics to eliminate redundancy
- Ensure bullet points within sections follow logical progression
- Apply consistent punctuation
- Minimize topic-jumping by grouping related content
- Preserve ALL information from the input
```

Источник: [GitHub Gist — adamsmith — voice-memo transcript to organized markdown](https://gist.github.com/adamsmith/2a22b08d3d4a11fb9fe06531aea4d67c)

---

## 4. Извлечение Action Items и ключевых решений

### Промпт для meeting/voice note анализа

```
Analyze this transcript and provide a structured summary:

1. Meeting Overview
   - Date, duration, participants (if mentioned)
   - Main objectives discussed

2. Key Decisions
   - All final decisions made
   - Deadlines or timelines established
   - Budgets or resources allocated

3. Action Items
   - List each with:
     * Assigned owner
     * Due date (if specified)
     * Dependencies or prerequisites
     * Current status (if mentioned)

4. Discussion Topics
   - Main points for each topic
   - Challenges or risks identified
   - Unresolved questions requiring follow-up

5. Next Steps
   - Upcoming milestones
   - Scheduled follow-ups
   - Required preparations

ROLE: You are a professional meeting analyst focused on extracting
actionable insights.
FORMAT: Clear sections with bullet points for easy scanning.
Keep descriptions concise but include specific details (names, dates, numbers).
If elements are not discussed, note their absence rather than making assumptions.
```

Источник: [AssemblyAI — How to summarize meetings with LLMs](https://www.assemblyai.com/blog/summarize-meetings-llms-python)

### Только action items (быстрое извлечение)

```
Review this transcript and extract ONLY the action items mentioned.
For each action item, provide:
1. The specific task
2. Who is responsible
3. The deadline if mentioned
4. Any context needed to understand the task

Format as a clear, bulleted list.
```

---

## 5. Промпт для Claude с XML-тегами (оптимально для Claude)

Claude лучше работает с XML-разметкой для структурирования:

```xml
<task>Process this voice transcript</task>

<rules>
- Remove filler words (um, uh, like, you know, ну, вот, типа, короче)
- Fix grammar and punctuation
- Remove self-corrections (keep only final version)
- Break into logical paragraphs
- Preserve speaker's intent and meaning
- Do NOT summarize — keep ALL content
</rules>

<output_format>
Return the result in this structure:

<cleaned_text>
[Full cleaned transcript here]
</cleaned_text>

<extracted>
  <action_items>
  - [task 1]
  - [task 2]
  </action_items>

  <key_decisions>
  - [decision 1]
  </key_decisions>

  <ideas>
  - [idea 1]
  </ideas>

  <questions>
  - [open question 1]
  </questions>
</extracted>
</output_format>

<transcript>
{PASTE_TRANSCRIPT_HERE}
</transcript>
```

---

## 6. Промпт для русскоязычных транскрипций

```
Ты — редактор голосовых заметок. Тебе дают расшифровку голосового сообщения
на русском языке.

Твоя задача:
1. ЧИСТКА: Убрать слова-паразиты (ну, вот, это, короче, типа, в общем,
   как бы, то есть, значит, блин, ладно). Убрать повторы, заикания,
   незаконченные мысли. Исправить грамматику и пунктуацию.

2. СТРУКТУРА: Разбить на логические абзацы. Добавить подзаголовки если
   текст длиннее 200 слов. Сгруппировать разрозненные мысли по темам.

3. ИЗВЛЕЧЕНИЕ:
   - Задачи (что сделать, кому, когда)
   - Решения (что решил)
   - Идеи (новые мысли, которые стоит запомнить)
   - Вопросы (что осталось открытым)

Формат вывода:

## Чистый текст
[Полный очищенный текст, сохраняя ВСЮ информацию]

## Извлечено
**Задачи:**
- [ ] задача 1 (срок, если указан)

**Решения:**
- решение 1

**Идеи:**
- идея 1

**Вопросы:**
- ? вопрос 1

---
Правила:
- НЕ сокращай содержание — это чистка, не пересказ
- Сохраняй стиль и тон автора
- Не добавляй от себя
- Если что-то неясно, пометь [неясно]
```

---

## 7. Open-source инструменты

### clean-transcribe (Python CLI)

```bash
pip install clean-transcribe

# Транскрибация + чистка YouTube видео
clean-transcribe youtube "https://youtube.com/watch?v=..." --cleaning-style presentation

# Локальный файл
clean-transcribe local audio.mp3 --cleaning-style conversation --llm-model claude-sonnet

# Стили чистки:
# presentation — профессиональный формат
# conversation — минимальная чистка, естественный диалог
# lecture — образовательный формат с секциями
```

Источник: [GitHub — itsmevictor/clean-transcribe](https://github.com/itsmevictor/clean-transcribe)

### Obsidian плагины

| Плагин | Что делает |
|--------|-----------|
| **Scribe** | Запись -> транскрипция -> суммаризация -> Mermaid-диаграммы |
| **NeuroVox** | Запись в заметках, Whisper/Groq транскрипция, кастомные промпты |
| **Obsidian Voice Input** | GPT-4o Transcribe API, словарная коррекция |
| **Whisper Plugin** | Простая speech-to-text через Whisper API |

Самый мощный — **Scribe**: транскрибирует, чистит, суммирует, генерирует Mermaid-диаграммы, интегрируется с OpenAI и AssemblyAI.

Источники:
- [Scribe plugin](https://www.obsidianstats.com/plugins/scribe)
- [NeuroVox plugin](https://www.obsidianstats.com/plugins/neurovox)
- [Obsidian Voice Input](https://github.com/mssoftjp/obsidian-voice-input)

### Voice-Memo-Data-Processor

Структурированное хранилище для транскрипций голосовых заметок в markdown, оптимизированное для AI-инструментов.

Источник: [GitHub — ajdedeaux/Voice-Memo-Data-Processor](https://github.com/ajdedeaux/Voice-Memo-Data-Processor)

### Transcript Cleaner (онлайн)

Бесплатный инструмент для быстрой чистки: убирает таймстампы, филлеры, метки спикеров.

Источник: [transcriptcleaner.org](https://transcriptcleaner.org/)

---

## 8. Техника "слоёного промпта" (layering)

Из библиотеки danielrosehill: базовый промпт чистки используется как фундамент, поверх которого накладываются модификаторы:

```
[Базовый промпт чистки STT]
+
[Модификатор стиля: formal / casual / academic / technical]
+
[Модификатор формата: email / bullet points / blog post / task list]
+
[Модификатор вывода: JSON / markdown / plain text]
```

Примеры комбинаций:
- STT cleanup + formal + email = деловое письмо из голосовой заметки
- STT cleanup + casual + bullet points = быстрые заметки
- STT cleanup + technical + JSON = структурированные данные для автоматизации

---

## 9. JSON-вывод для автоматизации

Для интеграции с Todoist, календарём, или MCP:

```
Process this voice transcript and return a JSON object with these keys:

{
  "summary": "1-2 sentence summary",
  "cleaned_text": "Full cleaned transcript",
  "action_items": [
    {
      "task": "description",
      "owner": "name or null",
      "due_date": "date or null",
      "priority": "high/medium/low"
    }
  ],
  "decisions": ["decision 1", "decision 2"],
  "ideas": ["idea 1"],
  "open_questions": ["question 1"],
  "topics": ["topic 1", "topic 2"],
  "sentiment": "positive/neutral/negative"
}

Return ONLY valid JSON. No additional text.
```

---

## 10. Лучшие практики (из всех источников)

1. **Двухпроходная обработка** лучше однопроходной: сначала чисти, потом структурируй
2. **XML-теги** для Claude, **markdown-синтаксис** для GPT, **жёсткий формат сверху** для Gemini
3. **Не суммируй, а чисти** — главная ошибка: LLM сокращает текст вместо чистки
4. **Указывай язык** явно (особенно для русского) — STT часто путает языки
5. **Словарь терминов** в промпте повышает точность (имена, бренды, термины)
6. **temperature=0** для чистки транскрипций (меньше "творчества")
7. **Фильтры-паразиты** нужно перечислять ЯВНО для русского языка
8. **Контекст** помогает: "this is a voice note about project management" лучше чем ничего

---

## Применение для Second Brain

Эти промпты можно интегрировать в `dbrain-processor`:
- Шаг 0 (перед классификацией): чистка [voice] записей через промпт #6
- При создании мыслей в мысли/: использовать двухпроходную технику (#3)
- При создании задач: JSON-извлечение (#9) для точных action items

## Related

- [[Second Brain Processor]]
- [[мысли/проекты/2026-02-09-second-brain-erp-architecture]]
