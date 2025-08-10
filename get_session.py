from telethon import TelegramClient
import asyncio

print("=== Получение STRING SESSION для UserBot ===\n")
print("Сначала получите API_ID и API_HASH на https://my.telegram.org\n")

api_id = input("Введите API_ID: ")
api_hash = input("Введите API_HASH: ")
phone = input("Введите номер телефона (с кодом страны, например +79991234567): ")

client = TelegramClient('temp_session', int(api_id), api_hash)

async def main():
    await client.start(phone)
    
    session_string = client.session.save()
    
    print("\n" + "="*60)
    print("STRING_SESSION получен успешно!")
    print("="*60)
    print("\nВаш STRING_SESSION:\n")
    print(session_string)
    print("\n" + "="*60)
    print("\n⚠️  ВАЖНО: Никогда не публикуйте эту строку!")
    print("Сохраните её для добавления в GitHub Secrets")
    
    await client.disconnect()

asyncio.run(main())

# Удаляем временные файлы
import os
try:
    os.remove('temp_session.session')
except:
    pass
