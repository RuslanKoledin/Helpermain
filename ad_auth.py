"""
Модуль для аутентификации через Active Directory
Поддерживает проверку учетных данных Windows
"""
import os
from typing import Optional, Dict, Any
from ldap3 import Server, Connection, ALL, NTLM, SIMPLE
from ldap3.core.exceptions import LDAPException, LDAPBindError
from dotenv import load_dotenv

load_dotenv()


class ADAuth:
    """Аутентификация через Active Directory"""

    def __init__(self):
        self.server_uri = os.getenv('AD_SERVER', 'ldap://localhost')
        self.port = int(os.getenv('AD_PORT', '389'))
        self.domain = os.getenv('AD_DOMAIN', 'mbank.local')
        self.base_dn = os.getenv('AD_BASE_DN', 'DC=mbank,DC=local')
        self.use_ssl = os.getenv('AD_USE_SSL', 'false').lower() == 'true'
        self.admin_group = os.getenv('AD_ADMIN_GROUP', '')
        self.dev_mode = os.getenv('DEV_MODE', 'false').lower() == 'true'

        # Списки администраторов по логинам
        admins_str = os.getenv('AD_ADMINS', '')
        super_admins_str = os.getenv('AD_SUPER_ADMINS', '')

        self.admin_logins = set(u.strip().lower() for u in admins_str.split(',') if u.strip())
        self.super_admin_logins = set(u.strip().lower() for u in super_admins_str.split(',') if u.strip())

        # Тестовые пользователи для режима разработки
        self.test_users = {
            'test': {
                'password': 'test123',
                'username': 'test',
                'display_name': 'Тестовый Пользователь',
                'email': 'test@mbank.local',
                'department': 'Отдел тестирования',
                'title': 'Тестировщик',
                'role': 'editor'
            },
            'admin': {
                'password': 'admin123',
                'username': 'admin',
                'display_name': 'Администратор Системы',
                'email': 'admin@mbank.local',
                'department': 'IT отдел',
                'title': 'Системный администратор',
                'role': 'super_admin'
            },
            'gulsaya': {
                'password': 'test123',
                'username': 'gulsaya',
                'display_name': 'Гулсая Асанова',
                'email': 'gulsaya@mbank.local',
                'department': 'Отдел входящей линии',
                'title': 'Специалист',
                'role': 'editor'
            }
        }

    def verify_credentials(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Проверка учетных данных через Active Directory

        Args:
            username: Логин пользователя (формат: a_asanov или DOMAIN\\a_asanov)
            password: Пароль

        Returns:
            Dict с информацией о пользователе или None при ошибке
        """
        if not username or not password:
            return None

        # Ограничение длины для безопасности
        if len(username) > 100 or len(password) > 128:
            return None

        # Режим разработки - используем тестовых пользователей
        if self.dev_mode:
            print(f"[DEV MODE] Attempting login for: {username}")
            # Убираем домен если есть (DOMAIN\username -> username)
            clean_username = username.split('\\')[-1].lower()

            if clean_username in self.test_users:
                user = self.test_users[clean_username]
                if user['password'] == password:
                    print(f"[DEV MODE] Login successful for: {username}")

                    # Определяем роль (проверка по логину имеет приоритет)
                    role = user['role']  # По умолчанию из test_users
                    if clean_username in self.super_admin_logins:
                        role = 'super_admin'
                        print(f"[DEV MODE] Role override: super_admin (from AD_SUPER_ADMINS)")
                    elif clean_username in self.admin_logins:
                        role = 'admin'
                        print(f"[DEV MODE] Role override: admin (from AD_ADMINS)")

                    return {
                        'username': user['username'],
                        'display_name': user['display_name'],
                        'email': user['email'],
                        'department': user['department'],
                        'title': user['title'],
                        'role': role
                    }
                else:
                    print(f"[DEV MODE] Wrong password for: {username}")
            else:
                print(f"[DEV MODE] User not found: {username}")
            return None

        try:
            # Подготовка username для AD
            # Если username содержит домен (DOMAIN\user), используем как есть
            # Иначе добавляем домен
            if '\\' not in username and '@' not in username:
                # Формат DOMAIN\username
                user_dn = f"{self.domain}\\{username}"
            else:
                user_dn = username

            # Создаем сервер
            server = Server(
                self.server_uri,
                port=self.port,
                get_info=ALL,
                use_ssl=self.use_ssl
            )

            # Пытаемся подключиться с учетными данными пользователя
            conn = Connection(
                server,
                user=user_dn,
                password=password,
                authentication=NTLM,
                auto_bind=True
            )

            if not conn.bind():
                print(f"AD bind failed for user: {username}")
                return None

            # Получаем информацию о пользователе
            search_filter = f"(sAMAccountName={username.split('\\')[-1]})"
            conn.search(
                search_base=self.base_dn,
                search_filter=search_filter,
                attributes=['displayName', 'mail', 'memberOf', 'sAMAccountName', 'department', 'title']
            )

            if not conn.entries:
                print(f"User not found in AD: {username}")
                conn.unbind()
                return None

            entry = conn.entries[0]

            # Извлекаем данные пользователя
            user_info = {
                'username': str(entry.sAMAccountName) if hasattr(entry, 'sAMAccountName') else username.split('\\')[-1],
                'display_name': str(entry.displayName) if hasattr(entry, 'displayName') else username,
                'email': str(entry.mail) if hasattr(entry, 'mail') else '',
                'department': str(entry.department) if hasattr(entry, 'department') else '',
                'title': str(entry.title) if hasattr(entry, 'title') else '',
                'role': 'editor'  # По умолчанию редактор
            }

            # Проверка роли по логину (ПРИОРИТЕТ 1)
            clean_username = user_info['username'].lower()
            if clean_username in self.super_admin_logins:
                user_info['role'] = 'super_admin'
            elif clean_username in self.admin_logins:
                user_info['role'] = 'admin'
            # Проверяем принадлежность к группе администраторов (ПРИОРИТЕТ 2)
            elif self.admin_group and hasattr(entry, 'memberOf'):
                member_of = [str(group) for group in entry.memberOf]
                if self.admin_group in member_of:
                    user_info['role'] = 'super_admin'

            conn.unbind()
            return user_info

        except LDAPBindError as e:
            print(f"AD authentication failed: {e}")
            return None
        except LDAPException as e:
            print(f"LDAP error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error during AD auth: {e}")
            return None

    def is_configured(self) -> bool:
        """Проверка, настроен ли AD"""
        return bool(self.server_uri and self.server_uri != 'ldap://localhost')


# Глобальный экземпляр
ad_auth = ADAuth()
