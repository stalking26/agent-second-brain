"""Text message handler with Claude processing."""

import asyncio
import logging
from datetime import datetime

from aiogram import Router
from aiogram.types import Message

from d_brain.config import get_settings
from d_brain.services.session import SessionStore
from d_brain.services.storage import VaultStorage
from d_brain.services.processor import ClaudeProcessor

router = Router(name="text")
logger = logging.getLogger(__name__)


async def _process_with_claude(
    text: str,
    user_id: int,
    status_msg: Message,
    settings,
) -> None:
    """Background task for Claude processing."""
    try:
        # Показываем статус "печатает"
        await status_msg.chat.do(action="typing")
        
        # Инициализируем процессор
        processor = ClaudeProcessor(settings.vault_path, settings.todoist_api_key)
        
        # Запускаем Claude в executor (чтобы не блокировать event loop)
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            processor.execute_prompt,
            text,
            user_id,
        )
        
        # Обновляем сообщение с результатом
        if result.get("report"):
            await status_msg.edit_text(result["report"], parse_mode="HTML")
        elif result.get("error"):
            error_msg = result['error']
            await status_msg.edit_text(
                f"✓ Сохранено\n❌ Ошибка анализа: {error_msg}"
            )
            
    except Exception as e:
        logger.exception("Error in Claude background processing")
        try:
            await status_msg.edit_text(f"✓ Сохранено\n❌ Ошибка анализа: {str(e)}")
        except Exception:
            pass  # Ignore if message edit fails


@router.message(lambda m: m.text is not None and not m.text.startswith("/"))
async def handle_text(message: Message) -> None:
    """Handle text messages and trigger Claude."""
    if not message.text or not message.from_user:
        return

    # 1. Сначала сохраняем
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

    # 2. СРАЗУ отправляем подтверждение с превью текста
    preview = message.text[:50] + "..." if len(message.text) > 50 else message.text
    status_msg = await message.answer(f"📝 Текст принят: {preview}\n\n⏳ Анализирую...")
    logger.info("Text message processed: %d chars", len(message.text))

    # 3. Запускаем Claude в фоновой задаче (не блокируем обработчик)
    asyncio.create_task(
        _process_with_claude(message.text, message.from_user.id, status_msg, settings)
    )
