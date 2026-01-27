# Руководство по управлению ролями администраторов

## Введение

В системе Helper реализовано три уровня доступа:
- **editor** - обычный пользователь (просмотр мануалов, создание заявок)
- **admin** - администратор (доступ к админ-панели)
- **super_admin** - супер-администратор (полный доступ)

## Способы назначения ролей

### 1. По логинам (РЕКОМЕНДУЕТСЯ) ⭐

Самый простой и гибкий способ - указать логины в `.env`:

```bash
# Обычные администраторы (роль: admin)
AD_ADMINS=r_koledin,a_ivanov,i_petrov

# Супер-администраторы (роль: super_admin)
AD_SUPER_ADMINS=r_koledin,s_sidorov
```

**Преимущества:**
- ✅ Не требует настройки групп в Active Directory
- ✅ Быстрое изменение ролей (просто отредактировать .env)
- ✅ Работает как в dev mode, так и с реальным AD
- ✅ Можно использовать сразу после получения доступа к AD

**Как использовать:**
1. Откройте файл `.env`
2. Найдите секцию `# Active Directory Configuration`
3. Добавьте/измените переменные `AD_ADMINS` и `AD_SUPER_ADMINS`
4. Перезапустите Flask сервер: `python3 helper7.py`

### 2. По группе Active Directory

Можно указать группу AD, члены которой получат роль `super_admin`:

```bash
AD_ADMIN_GROUP=CN=HelperAdmins,OU=Groups,DC=mbank,DC=local
```

**Когда использовать:**
- У вас уже есть группа администраторов в AD
- Вы хотите централизованно управлять доступом через AD

## Приоритет назначения ролей

При проверке пользователя система применяет следующий порядок:

1. **AD_SUPER_ADMINS** - если логин найден → роль `super_admin`
2. **AD_ADMINS** - если логин найден → роль `admin`
3. **AD_ADMIN_GROUP** - если пользователь в группе → роль `super_admin`
4. **По умолчанию** - роль `editor`

### Примеры

```bash
# Пример 1: r_koledin будет super_admin (приоритет 1)
AD_SUPER_ADMINS=r_koledin
AD_ADMINS=r_koledin,a_ivanov
# Результат: r_koledin → super_admin, a_ivanov → admin

# Пример 2: Комбинация методов
AD_SUPER_ADMINS=r_koledin
AD_ADMIN_GROUP=CN=HelperAdmins,OU=Groups,DC=mbank,DC=local
# r_koledin → super_admin (по логину)
# члены HelperAdmins → super_admin (по группе)
# остальные → editor
```

## Тестирование

### В режиме разработки (DEV_MODE=true)

Запустите тестовый скрипт:

```bash
python3 test_admin_roles.py
```

Он покажет:
- Списки администраторов из `.env`
- Какие роли назначаются тестовым пользователям
- Инструкции по настройке

### С реальным Active Directory

1. Убедитесь что `DEV_MODE=false`
2. Войдите на http://localhost:5003/login с AD-учеткой
3. Проверьте доступ к админ-панели: http://localhost:5003/admin/login

## Практические сценарии

### Сценарий 1: Быстрое добавление нового админа

```bash
# Было:
AD_ADMINS=r_koledin

# Стало:
AD_ADMINS=r_koledin,new_admin

# Перезапуск:
# Ctrl+C в терминале с Flask
python3 helper7.py
```

### Сценарий 2: Повышение админа до супер-админа

```bash
# Было:
AD_ADMINS=r_koledin,a_ivanov
AD_SUPER_ADMINS=

# Стало:
AD_ADMINS=r_koledin,a_ivanov
AD_SUPER_ADMINS=r_koledin

# r_koledin теперь super_admin (приоритет выше)
```

### Сценарий 3: Удаление прав администратора

```bash
# Было:
AD_ADMINS=r_koledin,a_ivanov,fired_admin

# Стало:
AD_ADMINS=r_koledin,a_ivanov

# fired_admin теперь editor (обычный пользователь)
```

## Безопасность

### ⚠️ Важные рекомендации:

1. **Не коммитьте .env в Git** - файл уже в `.gitignore`
2. **Минимум привилегий** - давайте super_admin только тем, кому действительно нужен полный доступ
3. **Регулярная проверка** - периодически проверяйте списки администраторов
4. **Логирование** - в dev mode логи показывают процесс назначения ролей

### Проверка текущих администраторов

```bash
# Посмотреть списки в .env:
grep "AD_.*ADMINS" .env

# Запустить тест:
python3 test_admin_roles.py
```

## Миграция на production

Когда получите доступ к AD от сисадминов:

1. **Отключите dev mode:**
   ```bash
   DEV_MODE=false
   ```

2. **Настройте AD параметры:**
   ```bash
   AD_SERVER=ldap://ad.mbank.local
   AD_DOMAIN=mbank.local
   AD_BASE_DN=DC=mbank,DC=local
   ```

3. **Укажите администраторов:**
   ```bash
   AD_ADMINS=r_koledin,a_ivanov
   AD_SUPER_ADMINS=r_koledin
   ```

4. **Перезапустите сервер**

5. **Проверьте вход** с реальными AD-учетками

## Часто задаваемые вопросы

### Можно ли использовать домен в логине?

Нет, указывайте только username без домена:

```bash
# ✅ Правильно:
AD_ADMINS=r_koledin

# ❌ Неправильно:
AD_ADMINS=MBANK\\r_koledin
AD_ADMINS=r_koledin@mbank.local
```

Система автоматически обрабатывает различные форматы входа пользователя.

### Регистр букв имеет значение?

Нет, система автоматически приводит к нижнему регистру:

```bash
AD_ADMINS=R_Koledin,A_IVANOV  # Будет работать
```

### Сколько администраторов можно добавить?

Технических ограничений нет, но рекомендуется:
- Super admins: 2-3 человека
- Admins: по необходимости

### Нужно ли перезапускать сервер после изменения .env?

Да, изменения в `.env` применяются только при запуске приложения.

## Поддержка

При возникновении проблем:

1. Запустите `python3 test_admin_roles.py`
2. Проверьте логи Flask сервера
3. Убедитесь что `.env` содержит корректные значения
4. В dev mode проверьте консольные логи `[DEV MODE]`
