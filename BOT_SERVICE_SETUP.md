# Настройка Telegram Bot как отдельного systemd сервиса

## Проблема
На сервере с systemd бот не запускается, потому что `web.helper.service` запускает только Flask через gunicorn/uwsgi, а блок `if __name__ == '__main__':` с ботом не выполняется.

## Решение
Запустить бота как отдельный systemd сервис `bot.helper.service`.

---

## Шаг 1: Скопировать файлы на сервер

Загрузите эти файлы на сервер:
- `bot.py` - код бота
- `bot.helper.service` - systemd service файл

---

## Шаг 2: Отредактировать bot.helper.service

Откройте файл `bot.helper.service` и замените пути:

```bash
nano bot.helper.service
```

Замените `/path/to/helper1bezsidebar` на реальный путь к проекту, например:
```
WorkingDirectory=/var/www/helper1bezsidebar
EnvironmentFile=/var/www/helper1bezsidebar/.env
ExecStart=/usr/bin/python3 /var/www/helper1bezsidebar/bot.py
```

Также проверьте:
- `User=www-data` и `Group=www-data` - замените на вашего пользователя если нужно
- `/usr/bin/python3` - путь к Python (проверьте через `which python3`)

---

## Шаг 3: Установить systemd service

```bash
# Скопировать service файл в systemd
sudo cp bot.helper.service /etc/systemd/system/

# Перезагрузить systemd
sudo systemctl daemon-reload

# Включить автозапуск
sudo systemctl enable bot.helper.service

# Запустить бот
sudo systemctl start bot.helper.service
```

---

## Шаг 4: Проверить статус

```bash
# Проверить статус бота
sudo systemctl status bot.helper.service

# Посмотреть логи бота
sudo journalctl -u bot.helper.service -f

# Посмотреть последние 100 строк логов
sudo journalctl -u bot.helper.service -n 100
```

---

## Управление сервисом

```bash
# Остановить бота
sudo systemctl stop bot.helper.service

# Перезапустить бота
sudo systemctl restart bot.helper.service

# Посмотреть логи в реальном времени
sudo journalctl -u bot.helper.service -f

# Проверить обе службы
sudo systemctl status web.helper.service
sudo systemctl status bot.helper.service
```

---

## Проверка работы

После запуска обеих служб:

1. **Flask работает:**
   ```bash
   curl http://localhost:5003
   ```

2. **Бот работает:**
   - Отправьте фото/видео боту - должен вернуть file_id
   - Нажмите кнопку "Готово" или "Не актуально" в Telegram - должно сработать

3. **Проверьте логи:**
   ```bash
   # Логи Flask
   sudo journalctl -u web.helper.service -n 50

   # Логи бота
   sudo journalctl -u bot.helper.service -n 50
   ```

---

## Troubleshooting

### Бот не запускается

```bash
# Проверьте путь к Python
which python3

# Проверьте права на файлы
ls -la /path/to/helper1bezsidebar/bot.py
ls -la /path/to/helper1bezsidebar/.env

# Проверьте .env файл
cat /path/to/helper1bezsidebar/.env | grep BOT_TOKEN
```

### Ошибки в логах

```bash
# Полные логи с момента запуска
sudo journalctl -u bot.helper.service --no-pager

# Логи с ошибками
sudo journalctl -u bot.helper.service -p err
```

### Переменные окружения не загружаются

Убедитесь что:
1. Файл `.env` существует
2. В нем есть `BOT_TOKEN=...`
3. Путь в `EnvironmentFile=` правильный
4. У пользователя `www-data` есть доступ на чтение `.env`

```bash
sudo -u www-data cat /path/to/helper1bezsidebar/.env
```

---

## Автозапуск при перезагрузке

Обе службы настроены на автозапуск:
```bash
sudo systemctl enable web.helper.service
sudo systemctl enable bot.helper.service
```

После перезагрузки сервера обе службы запустятся автоматически.

---

## Итоговая структура

```
/path/to/helper1bezsidebar/
├── helper7.py              # Flask приложение
├── bot.py                  # Telegram бот (новый файл)
├── .env                    # Переменные окружения
├── topics.db               # База данных
└── ...

/etc/systemd/system/
├── web.helper.service      # Служба Flask (уже есть)
└── bot.helper.service      # Служба бота (новый)
```

---

## Результат

После настройки у вас будет:
- ✅ Flask работает через `web.helper.service`
- ✅ Telegram бот работает через `bot.helper.service`
- ✅ Обе службы автоматически перезапускаются при падении
- ✅ Обе службы стартуют при перезагрузке сервера
- ✅ Кнопки "Готово" и "Не актуально" работают в Telegram
