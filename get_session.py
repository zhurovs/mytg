from telethon.sync import TelegramClient
from telethon.sessions import StringSession

print("=== Получение STRING SESSION для UserBot ===\n")
print("Сначала получите API_ID и API_HASH на https://my.telegram.org\n")

api_id = input("Введите API_ID: ")
api_hash = input("Введите API_HASH: ")
phone = input("Введите номер телефона (с кодом страны, например +79991234567): ")

# Создаем клиент с пустой StringSession
with TelegramClient(StringSession(), int(api_id), api_hash) as client:
    client.start(phone)
    
    # Получаем session string правильным способом
    session_string = client.session.save()
    
    print("\n" + "="*60)
    print("STRING_SESSION получен успешно!")
    print("="*60)
    print("\nВаш STRING_SESSION:\n")
    print(session_string)
    print("\n" + "="*60)
    print("\n⚠️  ВАЖНО: Никогда не публикуйте эту строку!")
    print("Эта строка - ваш полный доступ к аккаунту!")
    print("\n✅ Скопируйте строку выше для GitHub Secrets")
