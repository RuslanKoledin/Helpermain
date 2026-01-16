#!/usr/bin/env python3
"""
Тестовый скрипт для проверки отображения видео в мануалах
"""

import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_video_in_manuals():
    """Проверяет наличие видео в мануалах"""

    print("=" * 60)
    print("ТЕСТ: Проверка видео в manuals_data.json")
    print("=" * 60)

    # Загружаем данные
    with open('manuals_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    manuals = data.get('manuals', {})

    # Проверяем каждую подпроблему
    total_videos = 0
    for manual_id, manual in manuals.items():
        if 'subproblems' not in manual:
            continue

        for sub_id, sub in manual['subproblems'].items():
            if 'video' in sub:
                total_videos += 1
                video_id = sub['video'].get('id')
                video_caption = sub['video'].get('caption', 'N/A')

                print(f"\n✅ Видео найдено в подпроблеме {manual_id}.{sub_id}")
                print(f"   Название: {sub.get('title', 'N/A')}")
                print(f"   Video ID: {video_id[:50] if video_id else 'None'}...")
                print(f"   Caption: {video_caption}")

                # Проверка валидности video_id
                if not video_id:
                    print(f"   ⚠️  WARNING: video_id пустой!")
                elif not isinstance(video_id, str):
                    print(f"   ⚠️  WARNING: video_id не строка! type={type(video_id)}")
                elif len(video_id) > 200:
                    print(f"   ⚠️  WARNING: video_id слишком длинный! len={len(video_id)}")
                else:
                    print(f"   ✓ video_id валиден")

    print("\n" + "=" * 60)
    print(f"ИТОГО: Найдено {total_videos} видео в мануалах")
    print("=" * 60)

    # Проверяем переменные окружения
    print("\n" + "=" * 60)
    print("ПРОВЕРКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ")
    print("=" * 60)

    bot_token = os.getenv('BOT_TOKEN')
    if bot_token:
        print(f"✓ BOT_TOKEN установлен (длина: {len(bot_token)})")
    else:
        print("✗ BOT_TOKEN не установлен!")

    tech_support_chat_id = os.getenv('TECH_SUPPORT_CHAT_ID')
    if tech_support_chat_id:
        print(f"✓ TECH_SUPPORT_CHAT_ID установлен: {tech_support_chat_id}")
    else:
        print("✗ TECH_SUPPORT_CHAT_ID не установлен!")

if __name__ == '__main__':
    test_video_in_manuals()
