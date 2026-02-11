---
date: 2026-02-11
type: learning
tags: [proxy, VPN, Outline, VPS, networking, privacy, tools]
linked: [[Лаборатория AI]], [[Claude Code]]
---

# Настройка прокси через Outline VPN на VPS

## Summary

Пошаговая инструкция по настройке собственного прокси-сервера через Outline VPN на VPS (европейский сервер). Установка занимает ~5 минут. Трафик идёт через VPS в Европе, обходя территориальные ограничения.

## Инструменты

- **Outline Manager** — для настройки сервера (getoutline.org/get-started)
- **Outline Client** — для подключения клиентских устройств
- **VPS сервер** — "европейский уютный домик"

## Пошаговая инструкция

1. Скачать Outline Manager (не клиент!)
2. Выбрать "Set up manually"
3. Скопировать команду установки:
   ```
   sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/Jigsaw-Code/outline-apps/master/server_manager/install_scripts/install_server.sh)"
   ```
4. SSH на сервер: `ssh root@ip_адрес`
5. Выполнить команду установки
6. Скопировать ключ в фигурных скобках `{...}`
7. Вставить ключ в Outline Manager → Done
8. Share → access key + добавить `&prefix=POST%20` в конец ключа
9. Вставить в Outline Client

## Важный нюанс

К access key нужно добавить `&prefix=POST%20` в самый конец без пробелов — иначе может не работать.

## Источник

Вебинар по Claude Code (@aimastersme). Видео будет на следующей неделе.
