---
date: 2026-02-11
type: learning
tags: [AI-safety, cost-optimization, system-instructions, Roo-Code, Claude-Code, security]
linked: [[2026-02-09-roo-code-modes]], [[Лаборатория AI]]
---

# "Железные правила" для AI-агентов — ограничение системных директорий

## Summary

Концепция разделения навыков (skills) и правил (system instructions) для AI-агентов. Навык — "что я умею", правило — "чего я делать НЕ должен". Решает проблему сканирования системных папок (AppData, /var/log и т.д.), которое сжигает токены и опасно.

## Проблема

AI-агент при неточной команде ("обнови ключ") начинает рекурсивный поиск по всей ФС, включая:
- Windows: `C:\Users\*\AppData\`, `C:\Windows\`, `C:\Program Files\`
- Linux: `/var/log`, `/usr/bin`, `/etc`, `/proc`

Результат: массивный расход токенов на чтение бинарных файлов, потенциальная утечка данных.

## Аналогия

Уборщик, которого попросили вытереть пыль со стола, начал разбирать стену дома в поисках кирпичей. Дорого, глупо и опасно.

## Решение

### Windows (глобальное правило в VS Code / Roo Code)

В Custom Instructions добавить:
```
⛔️ SECURITY & COST PROTOCOL (WINDOWS):
1. RESTRICTED ZONES: FORBIDDEN from accessing C:\Windows\, C:\Users\*\AppData\, C:\Program Files\
2. REASON: Token waste + binary files = money waste
3. IF ASKED: REFUSE and ask for specific path
4. SCOPE: ONLY current project directory
```

### Linux (серверная версия — .clinerules)

Добавить правило для всех ролей:
```
Запрет сканирования /var, /usr, /etc, /bin, /proc без явной команды.
Зона ответственности — только /home/myuser/
```

## Правило экономии

- Никогда не проси AI искать что-то в системных настройках (VS Code, Chrome, Windows)
- Плохо: "Найди, где лежат настройки VS Code" (перероет весь диск)
- Хорошо: "Напиши мне путь, я сам открою"

## Ключевой инсайт

Это произошло не из-за глупости AI, а из-за чрезмерной старательности. Правила (constraints) важнее навыков (capabilities) для контроля AI-агентов.
