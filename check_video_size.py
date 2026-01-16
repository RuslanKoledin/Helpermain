#!/usr/bin/env python3
"""
Проверяет размер видео файлов в Telegram
"""

import os
from dotenv import load_dotenv
import telebot

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# ID видео из базы данных
video_ids = [
    "BAACAgIAAxkBAAIKeWkPK-xwmW5aQqkeYOGtHPeNMCS7AALofwACQtR4SP7CmzLxLzl4NgQ",  # 1.1
    "BAACAgIAAyEGAAS2wnenAAICq2knvkZLWHvzAAGP3VmKlihAAjr2CQACo3oAAl5EQEnP142j3ZJkhTYE",  # 1.2
    "BAACAgIAAyEGAAS2wnenAAIC-2lA1syGJZtbNMK7OP7Rk6g_JYhkAAKOggACg-wJSoCwRLGDaYouNgQ",  # 1.3
]

print("=" * 70)
print("ПРОВЕРКА РАЗМЕРОВ ВИДЕО В TELEGRAM")
print("=" * 70)

for i, video_id in enumerate(video_ids, 1):
    print(f"\n📹 Видео {i}: {video_id[:50]}...")
    try:
        file_info = bot.get_file(video_id)
        file_size_mb = file_info.file_size / (1024 * 1024)
        print(f"   ✅ Размер: {file_size_mb:.2f} МБ")
        print(f"   ✅ file_path: {file_info.file_path}")

        if file_size_mb > 20:
            print(f"   ⚠️  ВНИМАНИЕ: Файл больше 20 МБ - getFile работает, но скачать не получится!")
    except telebot.apihelper.ApiTelegramException as e:
        print(f"   ❌ ОШИБКА: {e}")
        print(f"   ℹ️  Файл вероятно больше 20 МБ")
    except Exception as e:
        print(f"   ❌ Неизвестная ошибка: {e}")

print("\n" + "=" * 70)
print("ВАЖНО:")
print("- Если файл < 20 МБ: getFile работает, можно скачать")
print("- Если файл > 20 МБ: getFile падает с ошибкой 'file is too big'")
print("- Telegram Bot API НЕ позволяет скачивать файлы > 20 МБ")
print("=" * 70)
