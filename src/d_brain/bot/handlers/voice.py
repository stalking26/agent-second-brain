"""Voice message handler with Claude processing."""

import logging
from datetime import datetime

from aiogram import Bot, Router
from aiogram.types import Message

from d_brain.config import get_settings
from d_brain.services.session import SessionStore
from d_brain.services.storage import VaultStorage
from d_brain.services.transcription import DeepgramTranscriber
from d_brain.services.processor import ClaudeProcessor  # <-- Добавляем мозг

router = Router(name="voice")
logger = logging.getLogger(__name__)


@router.message(lambda m: m.voice is not None)
async def handle_voice(message: Message, bot: Bot) -> None:
    """Handle voice messages."""
    if not message.voice or not message.from_user:
        return

    # Показываем статус "печатает" (или "записывает аудио")
    await message.chat.do(action="typing")

    settings = get_settings()
    storage = VaultStorage(settings.vault_path)
    transcriber = DeepgramTranscriber(settings.deepgram_api_key)

    try:
        # 1. Скачиваем файл
        file = await bot.get_file(message.voice.file_id)
        if not file.file_path:
            await message.answer("Failed to download voice message")
            return

        file_bytes = await bot.download_file(file.file_path)
        if not file_bytes:
            await message.answer("Failed to download voice message")
            return

        # 2. Транскрибируем (Deepgram)
        audio_bytes = file_bytes.read()
        transcript = await transcriber.transcribe(audio_bytes)

        if not transcript:
            await message.answer("Could not transcribe audio")
            return

        # 3. Сохраняем в Daily
        timestamp = datetime.fromtimestamp(message.date.timestamp())
        storage.append_to_daily(transcript, timestamp, "[voice]")

        # Логируем сессию
        session = SessionStore(settings.vault_path)
        session.append(
            message.from_user.id,
            "voice",
            text=transcript,
            duration=message.voice.duration,
            msg_id=message.message_id,
        )

        status_msg = await message.answer(f"🎤 {transcript}\n\n✓ Сохранено. Анализирую...")
        logger.info("Voice message saved: %d chars", len(transcript))

        # 4. ВКЛЮЧАЕМ МОЗГ (ClaudeProcessor)
        # Инициализируем процессор
        processor = ClaudeProcessor(settings.vault_path, settings.todoist_api_key)
        
        # Отправляем расшифрованный текст Клоду
        result = processor.execute_prompt(transcript, message.from_user.id)
        
        # Обновляем сообщение с результатом
        if result.get("report"):
            await status_msg.edit_text(f"🎤 {transcript}\n\n{result['report']}", parse_mode="HTML")
        elif result.get("error"):
            await status_msg.edit_text(f"🎤 {transcript}\n\n✓ Сохранено (ошибка AI: {result['error']})")

    except Exception as e:
        logger.exception("Error processing voice message")
        await message.answer(f"Error: {e}")
