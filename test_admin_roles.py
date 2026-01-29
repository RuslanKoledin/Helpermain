#!/usr/bin/env python3
"""
Скрипт для тестирования назначения ролей администраторов по логинам
"""

from ad_auth import ad_auth

def test_admin_role_assignment():
    """Тестирование назначения ролей по логинам из .env"""

    print("=" * 70)
    print("ТЕСТИРОВАНИЕ НАЗНАЧЕНИЯ РОЛЕЙ АДМИНИСТРАТОРОВ ПО ЛОГИНАМ")
    print("=" * 70)
    print()

    # Проверяем режим разработки
    if not ad_auth.dev_mode:
        print("❌ DEV_MODE выключен - включите в .env файле для тестирования")
        return

    print("✅ DEV_MODE включен")
    print()
    print("Списки администраторов из .env:")
    print(f"  AD_ADMINS: {ad_auth.admin_logins}")
    print(f"  AD_SUPER_ADMINS: {ad_auth.super_admin_logins}")
    print()
    print("-" * 70)

    # Тест 1: Обычный пользователь test (должен остаться editor)
    print("\nТЕСТ 1: Обычный пользователь (не в списках админов)")
    print("Логин: test, Пароль: test123")
    result = ad_auth.verify_credentials('test', 'test123')
    if result:
        role = result['role']
        expected = 'editor'
        status = "✅" if role == expected else "❌"
        print(f"{status} Роль: {role} (ожидалось: {expected})")
        print(f"   ФИО: {result['display_name']}")
    else:
        print("❌ Ошибка аутентификации")

    print()
    print("-" * 70)

    # Тест 2: Пользователь admin (в списке super_admins)
    print("\nТЕСТ 2: Супер-администратор из списка AD_SUPER_ADMINS")
    print("Логин: admin, Пароль: admin123")
    result = ad_auth.verify_credentials('admin', 'admin123')
    if result:
        role = result['role']
        # Проверяем: admin не в AD_SUPER_ADMINS по умолчанию
        # Но если добавить в .env, то будет super_admin
        print(f"✅ Роль: {role}")
        print(f"   ФИО: {result['display_name']}")
        if 'admin' in ad_auth.super_admin_logins:
            print("   📝 'admin' найден в AD_SUPER_ADMINS")
    else:
        print("❌ Ошибка аутентификации")

    print()
    print("-" * 70)

    # Тест 3: Проверка с доменом (MBANK\username)
    print("\nТЕСТ 3: Вход с доменом")
    print("Логин: MBANK\\gulsaya, Пароль: test123")
    result = ad_auth.verify_credentials('MBANK\\gulsaya', 'test123')
    if result:
        role = result['role']
        print(f"✅ Роль: {role}")
        print(f"   Username: {result['username']}")
        print(f"   ФИО: {result['display_name']}")
    else:
        print("❌ Ошибка аутентификации")

    print()
    print("=" * 70)
    print("ИНСТРУКЦИЯ ПО НАЗНАЧЕНИЮ РОЛЕЙ")
    print("=" * 70)
    print()
    print("Чтобы назначить роль администратора пользователю:")
    print()
    print("1. Откройте файл .env")
    print()
    print("2. Добавьте логин в нужную переменную:")
    print("   - AD_ADMINS=username1,username2      # Обычные админы")
    print("   - AD_SUPER_ADMINS=username1          # Супер-админы")
    print()
    print("3. Примеры:")
    print("   AD_ADMINS=r_koledin,a_ivanov")
    print("   AD_SUPER_ADMINS=r_koledin")
    print()
    print("4. Перезапустите сервер Flask")
    print()
    print("Приоритет ролей:")
    print("  1️⃣  AD_SUPER_ADMINS (высший)")
    print("  2️⃣  AD_ADMINS")
    print("  3️⃣  AD_ADMIN_GROUP (группа в AD)")
    print("  4️⃣  По умолчанию: editor")
    print()

if __name__ == '__main__':
    test_admin_role_assignment()
