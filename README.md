# Pyrogram_tz

Ссылка на ТЗ - https://docs.google.com/spreadsheets/d/1xsE6GG-HXQ4LES_E1838nwsLgelUaghUrrsZwNBjXKY/edit#gid=0

Pyrogram_tz - это пример асинхронного приложения на Python с использованием Pyrogram, SQLAlchemy, Loguru и Aiosqlite.

## Установка

1. Сначала убедитесь, что у вас установлен Python 3.7 или выше.
2. Установите зависимости:

```
pip install -r requirements.txt
```

## Настройка
Создайте файл конфигурации config.ini и укажите необходимые параметры, такие как api_id и api_hash:
ini
```
[pyrogram]
api_id = YOUR_API_ID
api_hash = YOUR_API_HASH
```
## Запуск
```
python main.py
```