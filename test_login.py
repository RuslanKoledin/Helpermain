#!/usr/bin/env python3
"""
Скрипт для тестирования AD-аутентификации в режиме разработки
"""

from ad_auth import ad_auth

def test_authentication():
    """Тестирование аутентификации с тестовыми пользователями"""

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ AD-АУТЕНТИФИКАЦИИ В РЕЖИМЕ РАЗРАБОТКИ")
    print("=" * 60)
    print()

    # Проверяем режим разработки
    if ad_auth.dev_mode:
        print("✅ DEV_MODE включен")
    else:
        print("❌ DEV_MODE выключен - включите в .env файле")
        return

    print()
    print("-" * 60)

    # Тест 1: Успешный вход обычного пользователя
    print("\nТЕСТ 1: Вход обычного пользователя")
    print("Логин: test, Пароль: test123")
    result = ad_auth.verify_credentials('test', 'test123')
    if result:
        print(f"✅ Успешно!")
        print(f"   ФИО: {result['display_name']}")
        print(f"   Отдел: {result['department']}")
        print(f"   Email: {result['email']}")
        print(f"   Роль: {result['role']}")
    else:
        print("❌ Ошибка аутентификации")

    print()
    print("-" * 60)

    # Тест 2: Успешный вход администратора
    print("\nТЕСТ 2: Вход администратора")
    print("Логин: admin, Пароль: admin123")
    result = ad_auth.verify_credentials('admin', 'admin123')
    if result:
        print(f"✅ Успешно!")
        print(f"   ФИО: {result['display_name']}")
        print(f"   Отдел: {result['department']}")
        print(f"   Роль: {result['role']}")
    else:
        print("❌ Ошибка аутентификации")

    print()
    print("-" * 60)

    # Тест 3: Вход с доменом
    print("\nТЕСТ 3: Вход с доменом (MBANK\\gulsaya)")
    print("Логин: MBANK\\gulsaya, Пароль: test123")
    result = ad_auth.verify_credentials('MBANK\\gulsaya', 'test123')
    if result:
        print(f"✅ Успешно!")
        print(f"   ФИО: {result['display_name']}")
        print(f"   Отдел: {result['department']}")
    else:
        print("❌ Ошибка аутентификации")

    print()
    print("-" * 60)

    # Тест 4: Неверный пароль
    print("\nТЕСТ 4: Неверный пароль")
    print("Логин: test, Пароль: wrongpass")
    result = ad_auth.verify_credentials('test', 'wrongpass')
    if result:
        print("❌ Ошибка: вход разрешен с неверным паролем!")
    else:
        print("✅ Вход корректно заблокирован")

    print()
    print("-" * 60)

    # Тест 5: Несуществующий пользователь
    print("\nТЕСТ 5: Несуществующий пользователь")
    print("Логин: nonexistent, Пароль: test123")
    result = ad_auth.verify_credentials('nonexistent', 'test123')
    if result:
        print("❌ Ошибка: вход разрешен для несуществующего пользователя!")
    else:
        print("✅ Вход корректно заблокирован")

    print()
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("=" * 60)
    print()
    print("Доступные тестовые пользователи:")
    for username, data in ad_auth.test_users.items():
        print(f"  • {username} / {data['password']} - {data['display_name']}")
    print()

if __name__ == '__main__':
    test_authentication()
