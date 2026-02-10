---
date: 2026-02-09
type: project
domain: Product
tags: [second-brain, erp, architecture, TWA, RAG, google-calendar, SaaS]
related:
  - "[[thoughts/projects/2026-02-08-telegram-bot-security-app]]"
  - "[[goals/1-yearly-2025#Career & Business]]"
  - "[[goals/2-monthly]]"
---

## Context
Архитектурное решение: эволюция Agent Second Brain из "просто бота" в полноценную ERP-систему.

## Вердикт: Гибрид (TWA + Бот)
- **Telegram Web App (TWA)** — веб-интерфейс внутри Телеграма
- **Бот** остаётся как быстрый карманный интерфейс
- WebApp для: календарь-сетка, большие файлы (Google Drive стриминг), омниканальность (TG + WhatsApp + Email)

## RAG-архитектура (решение проблемы токенов)
1. **Индексация** (1 раз) — скрипт сканирует Google Drive, конвертирует в векторы → ChromaDB/Pinecone
2. **Поиск** (дёшево) — векторный поиск нужного куска
3. **Генерация** (платно, но мало) — LLM получает только 1-2 страницы контекста

## Google Calendar + Секретарь
- Service Account в Google Cloud Console
- Бот читает "окна" → предлагает клиенту → ставит встречу → уведомляет секретаря

## Монетизация
- Продукт "Личный Ассистент HR" — обкатка на себе → SaaS / коробка $500+
- WebApp выглядит дороже → оправдывает цену
- AI Лаборатория = кейс №1

## Roadmap
1. Backend (Python/FastAPI) — Google Calendar API интеграция
2. Vector Store — ежесуточная индексация "Базы знаний" с Google Drive
3. Frontend (TWA) — панель: расписание + чаты (Streamlit или React)

## Related
- [[thoughts/projects/2026-02-09-consultant-workbench]] — Рабочее Место Эксперта
- [[thoughts/projects/2026-02-08-telegram-bot-security-app]] — admin panel
- [[goals/2-monthly]] — HR-бот + Лаборатория
