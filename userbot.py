from telethon import TelegramClient, events
import os
import logging
import asyncio
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Получаем переменные из окружения
api_id = int(os.environ.get('API_ID', 0))
api_hash = os.environ.get('API_HASH', '')
phone = os.environ.get('PHONE', '')
string_session = os.environ.get('STRING_SESSION', '')

# ИСТОЧНИКИ - легко добавлять новые группы через запятую
source_chats_str = os.environ.get('SOURCE_CHATS', '-1002706823424')  # Appzh по умолчанию
SOURCE_CHATS = [int(chat_id.strip()) for chat_id in source_chats_str.split(',')]

# ЦЕЛЕВАЯ ГРУППА для копирования
TARGET_CHAT = int(os.environ.get('TARGET_CHAT', '-1002699982539'))  # Appzh_backup

# Проверка переменных
if not all([api_id, api_hash, phone, string_session]):
    logger.error("Отсутствуют необходимые переменные окружения!")
    exit(1)

# Создаем клиент
client = TelegramClient(string_session, api_id, api_hash)

# Словарь для хранения названий групп
chat_names = {}

@client.on(events.NewMessage(chats=SOURCE_CHATS))
async def forward_handler(event):
    """Обработчик новых сообщений для пересылки"""
    try:
        # Получаем название группы-источника
        chat_name = chat_names.get(event.chat_id, f"Chat {event.chat_id}")
        
        # Формируем заголовок с информацией об источнике
        sender = await event.get_sender()
        sender_name = getattr(sender, 'first_name', 'Unknown')
        if hasattr(sender, 'username') and sender.username:
            sender_info = f"{sender_name} (@{sender.username})"
        else:
            sender_info = sender_name
        
        # Отправляем информацию об источнике
        header_text = f"📨 **Из группы:** {chat_name}\n👤 **От:** {sender_info}\n➖➖➖➖➖➖➖➖➖➖"
        await client.send_message(TARGET_CHAT, header_text)
        
        # Пересылаем само сообщение
        await client.forward_messages(
            entity=TARGET_CHAT,
            messages=event.message,
            from_peer=event.chat_id
        )
        
        logger.info(f"Переслано из '{chat_name}' от {sender_name}")
        
    except Exception as e:
        logger.error(f"Ошибка при пересылке: {e}")
        await asyncio.sleep(5)

async def main():
    """Основная функция"""
    try:
        # Подключаемся
        await client.start(phone)
        
        # Информация о боте
        me = await client.get_me()
        logger.info(f"UserBot запущен как {me.first_name} (@{me.username})")
        
        # Проверяем и сохраняем названия групп-источников
        logger.info(f"\n📥 ГРУППЫ-ИСТОЧНИКИ ({len(SOURCE_CHATS)}):")
        for i, chat_id in enumerate(SOURCE_CHATS, 1):
            try:
                chat = await client.get_entity(chat_id)
                chat_name = getattr(chat, 'title', f'Chat {chat_id}')
                chat_names[chat_id] = chat_name
                logger.info(f"{i}. {chat_name} (ID: {chat_id})")
            except Exception as e:
                logger.error(f"❌ Не удалось подключиться к чату {chat_id}: {e}")
        
        # Проверяем целевую группу
        logger.info(f"\n📤 ЦЕЛЕВАЯ ГРУППА:")
        try:
            target = await client.get_entity(TARGET_CHAT)
            target_name = getattr(target, 'title', 'Unknown')
            logger.info(f"✅ {target_name} (ID: {TARGET_CHAT})")
        except Exception as e:
            logger.error(f"❌ Не удалось подключиться к целевой группе: {e}")
            return
        
        # Запускаем
        logger.info("\n🚀 UserBot готов! Ожидание сообщений...")
        logger.info("➖" * 30)
        await client.run_until_disconnected()
        
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        raise

if __name__ == '__main__':
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("UserBot остановлен")
