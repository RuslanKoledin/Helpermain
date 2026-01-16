# Инструкция по отладке отображения видео

## Что я сделал:

1. **Добавил подробное логирование** в функции:
   - `get_file_url()` - строка 225-245
   - `show_manual()` - строка 800-833

2. **Проверил данные** - видео присутствует в:
   - Подпроблема 1.1 - "Заполнилась память"
   - Подпроблема 1.2 - "Не открывается OutLook"
   - Подпроблема 1.3 - "Письма в Исходящих"

## Как протестировать:

### Шаг 1: Запустите приложение
```bash
python3 helper7.py
```

### Шаг 2: Откройте браузер и пройдите по шагам:

1. Откройте http://localhost:5003
2. Заполните форму входа (отдел, имя, рабочее место)
3. Выберите "Мануалы по решению проблем"
4. Выберите "1. Проблемы с почтой"
5. Выберите подпроблему "Заполнилась память" (это будет URL вида `/show_manual/1.1`)

### Шаг 3: Смотрите в консоль/логи

Вы должны увидеть что-то типа:

```
[show_manual] Found video in subproblem_data, video_id: BAACAgIAAxkBAAIKeWkPK-xwmW5aQqkeYOGtHPeNMCS7AALofw...
[get_file_url] Successfully got URL for file_id=BAACAgIAAxkBAAIKeWkPK-xwmW5a...
[show_manual] Got video_url from get_file_url: https://api.telegram.org/file/bot...
[show_manual] Created video_data with caption: Видео-инструкция: Как очистить переполненную память в Outlook
[show_manual] Rendering template with:
  - manual_title: Заполнилась память
  - video_data: Present
  - photos count: 6
```

## Возможные проблемы:

### Проблема 1: video_url = None
Если видите:
```
[show_manual] WARNING: video_url is None - get_file_url failed!
```

**Причины:**
- BOT_TOKEN неверный или истек
- file_id устарел (файл удален из Telegram)
- Проблема с доступом к Telegram API

**Решение:**
- Проверьте BOT_TOKEN в .env
- Загрузите видео заново через админку

### Проблема 2: video_data не передается в шаблон
Если видите:
```
[show_manual] Rendering template with:
  - video_data: None
```

**Причины:**
- get_file_url вернул None
- video_id пустой

### Проблема 3: Видео не показывается в браузере

**Проверьте в браузере (F12 → Console):**
- Есть ли ошибки загрузки видео?
- Проверьте Network вкладку - загружается ли видео с Telegram API?

**Проверьте HTML код страницы:**
- Есть ли тег `<video>` с правильным `src`?
- Если нет - значит `video_data` = None в шаблоне

## Что отправить мне для диагностики:

1. **Логи из консоли** когда открываете страницу с мануалом
2. **Скриншот** того, что видите в браузере
3. **HTML код** секции с видео (правая кнопка → "Просмотр кода элемента")

## Быстрая проверка без браузера:

```bash
# Проверить что видео валидны
python3 test_video_display.py

# Проверить конкретный video file_id
python3 -c "
from helper7 import bot, get_file_url
video_id = 'BAACAgIAAxkBAAIKeWkPK-xwmW5aQqkeYOGtHPeNMCS7AALofwACQtR4SP7CmzLxLzl4NgQ'
url = get_file_url(video_id)
print(f'URL: {url}')
"
```
