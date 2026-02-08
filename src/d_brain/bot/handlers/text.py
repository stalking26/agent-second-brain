"""Text message handler with Claude processing."""

import logging
from datetime import datetime

from aiogram import Router
from aiogram.types import Message

from d_brain.config import get_settings
from d_brain.services.session import SessionStore
from d_brain.services.storage import VaultStorage
from d_brain.services.processor import ClaudeProcessor  # <-- Импортируем мозг!

router = Router(name="text")
logger = logging.getLogger(__name__)


@router.message(lambda m: m.text is not None and not m.text.startswith("/"))
async def handle_text(message: Message) -> None:
    """Handle text messages and trigger Claude."""
    if not message.text or not message.from_user:
        return

    # 1. Сначала сохраняем (как и раньше)
    settings = get_settings()
    storage = VaultStorage(settings.vault_path)
    timestamp = datetime.fromtimestamp(message.date.timestamp())
    storage.append_to_daily(message.text, timestamp, "[text]")

    session = SessionStore(settings.vault_path)
    session.append(
        message.from_user.id,
        "text",
        text=message.text,
        msg_id=message.message_id,
    )

    # Сообщаем, что записали
    status_msg = await message.answer("✓ Сохранено. Анализирую...")

    # 2. ВКЛЮЧАЕМ МОЗГ (ClaudeProcessor)
    try:
        await message.chat.do(action="typing")
        
        # Инициализируем процессор с ключами
        processor = ClaudeProcessor(settings.vault_path, settings.todoist_api_key)
        
        # Отправляем текст Клоду на выполнение
        # ВАЖНО: Это может занять 5-10 секунд
        result = processor.execute_prompt(message.text, message.from_user.id)
        
        # Если есть отчет от Клода — показываем его
        if result.get("report"):
            await status_msg.edit_text(result["report"], parse_mode="HTML")
        elif result.get("error"):
            await status_msg.edit_text(f"✓ Сохранено, но ошибка анализа: {result['error']}")
            
    except Exception as e:
        logger.exception("Error calling Claude processor")
        await status_msg.edit_text(f"✓ Сохранено (ошибка AI: {e})")

    logger.info("Text message processed: %d chars", len(message.text))
