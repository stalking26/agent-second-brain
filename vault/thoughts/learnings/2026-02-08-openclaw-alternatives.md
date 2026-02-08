---
date: 2026-02-08
type: learning
domain: AI & Tech
tags: [openclaw, nanoclaw, nanobot, ai-agents, telegram, security]
---

## Context
Пост 03:18 — анализ OpenClaw и его альтернатив.

## Insight
OpenClaw (бывш. Clawdbot) — первый массовый AI-агент в Telegram. Дал обычным людям почувствовать AI-ассистента. Но:
- Дыры в безопасности (слив данных в групповые чаты)
- 430K строк кода — невозможно аудировать

Альтернативы:
- **NanoClaw** — код за 8 мин, изолированные контейнеры. Только WhatsApp + Claude.
- **nanobot** (Гонконг) — 4K строк, любые модели включая локальные.

## Implication
Тренд: AI-агенты идут к массовому пользователю. Вопрос безопасности критичен. Наш HR-бот должен учесть эти уроки: минимальный код, изоляция, прозрачность.

## Next Action
Изучить архитектуру NanoClaw как референс для безопасного бот-дизайна.

## Related
- [[thoughts/projects/2026-02-08-telegram-bot-security-app]] — защита бота
