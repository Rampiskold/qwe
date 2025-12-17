# SGR PostgreSQL API - Быстрый старт

## 🚀 Запуск

```bash
cd /srv/sgr-agetn-core-tool-search-context-compression/postgres-adminer-setup
docker compose up -d
```

## 📡 Доступные сервисы

- **PostgreSQL**: `localhost:18788`
- **Adminer**: `http://localhost:18789`
- **API**: `http://localhost:18790`
- **API Docs**: `http://localhost:18790/docs`

## 🔧 Разработка без пересборки

Код API смонтирован как volume, изменения применяются автоматически благодаря `--reload`:

1. Редактируйте файлы в `./api/`
2. Сохраните изменения
3. Uvicorn автоматически перезагрузит приложение (2-3 секунды)

**Не нужно** запускать `docker compose build` или `docker compose restart`!

## 📚 API Эндпоинты

### 1. Получить список таблиц с комментариями

```bash
curl "http://localhost:18790/api/tables?page=1&page_size=10"
```

**Ответ:**
```json
{
  "tables": [
    {
      "table_name": "app_logs",
      "table_type": "BASE TABLE",
      "table_size": "96 kB",
      "column_count": 8,
      "table_comment": "Логи приложения для отслеживания событий"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 10,
    "total_count": 8,
    "total_pages": 1
  }
}
```

### 2. Получить схему таблицы с комментариями

```bash
curl "http://localhost:18790/api/tables/app_logs/schema"
```

**Ответ:**
```json
{
  "table_name": "app_logs",
  "table_comment": "Логи приложения для отслеживания событий",
  "columns": [
    {
      "column_name": "id",
      "data_type": "integer",
      "is_nullable": "NO",
      "is_primary_key": true,
      "column_comment": "Уникальный идентификатор записи"
    }
  ],
  "indexes": [...],
  "column_count": 8
}
```

## 🔍 Просмотр логов

```bash
# Все логи
docker compose logs -f

# Только API
docker compose logs -f api

# Последние 50 строк
docker compose logs --tail=50 api
```

## 🛠️ Полезные команды

```bash
# Перезапустить только API (если нужно)
docker compose restart api

# Остановить все
docker compose down

# Проверить статус
docker compose ps

# Войти в контейнер API
docker exec -it sgr-api-standalone sh
```

## 📝 Структура проекта

```
postgres-adminer-setup/
├── api/                    # Код API (монтируется как volume)
│   ├── __init__.py
│   ├── main.py            # Основное приложение
│   ├── database.py        # Работа с БД
│   ├── config.py          # Конфигурация
│   └── auth.py            # Аутентификация (не используется)
├── docker-compose.yml     # Конфигурация всех сервисов
├── Dockerfile.api         # Dockerfile для API
└── requirements.txt       # Python зависимости
```

## ⚡ Пример изменения кода

1. Откройте `api/main.py`
2. Измените что-то, например добавьте новый эндпоинт:

```python
@app.get("/api/test")
async def test():
    return {"message": "Это работает без пересборки!"}
```

3. Сохраните файл
4. Через 2-3 секунды проверьте:

```bash
curl http://localhost:18790/api/test
```

## 🐛 Troubleshooting

### API не перезагружается автоматически

Проверьте логи:
```bash
docker compose logs api
```

Должна быть строка: `Uvicorn running on http://0.0.0.0:18790 (Press CTRL+C to quit)`

### Ошибка подключения к БД

```bash
# Проверьте, что PostgreSQL запущен
docker compose ps postgres

# Проверьте логи PostgreSQL
docker compose logs postgres
```

### Синтаксическая ошибка в коде

Uvicorn покажет ошибку в логах:
```bash
docker compose logs api
```

Исправьте ошибку в файле, и приложение перезапустится автоматически.

## 🎯 Быстрый тест

```bash
# Health check
curl http://localhost:18790/health

# Список таблиц
curl "http://localhost:18790/api/tables?page=1&page_size=5"

# Схема таблицы
curl http://localhost:18790/api/tables/app_logs/schema
```
