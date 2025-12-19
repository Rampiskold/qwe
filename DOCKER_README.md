# SQL Agent - Docker Deployment

Полное решение для запуска SQL Agent в Docker контейнерах.

## Архитектура

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   SQL Agent     │────▶│   API Service   │────▶│   PostgreSQL    │
│  (run_agent.py) │     │  (FastAPI)      │     │   (Database)    │
│   Port: -       │     │   Port: 18790   │     │   Port: 18788   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │    Adminer      │
                                               │  (Web UI)       │
                                               │   Port: 18789   │
                                               └─────────────────┘
```

## Быстрый старт

### 1. Запустить инфраструктуру

```bash
# Запуск PostgreSQL + API (+ опционально Adminer)
docker-compose up -d postgres api adminer

# Проверить что сервисы запущены
docker-compose ps

# Проверить health API
curl http://localhost:18790/health
```

### 2. Запустить SQL Agent

```bash
# Запуск агента с задачей
docker-compose run --rm sql-agent sql_database_agent "Покажи все таблицы в базе данных"

# Другие примеры
docker-compose run --rm sql-agent sql_database_agent "Сколько записей в таблице app_logs?"
docker-compose run --rm sql-agent sql_database_agent "Найди последние 5 ошибок в логах"
```

## Конфигурация

### Переменные окружения

Создайте файл `.env` в корне проекта:

```env
# LLM Configuration
OPENAI_API_KEY=your-api-key-here

# Или переопределите при запуске:
# docker-compose run -e OPENAI_API_KEY=sk-xxx --rm sql-agent ...
```

### config.yaml

Конфигурация LLM и других параметров в `config.yaml`. Этот файл монтируется в контейнер.

### agents.yaml

Определение агентов в `agents.yaml`. Этот файл также монтируется в контейнер.

## Команды Docker Compose

```bash
# Запуск всей инфраструктуры
docker-compose up -d postgres api adminer

# Остановка всех сервисов
docker-compose down

# Остановка с удалением данных БД
docker-compose down -v

# Просмотр логов
docker-compose logs -f api
docker-compose logs -f postgres

# Пересборка образов после изменений
docker-compose build --no-cache sql-agent
docker-compose build --no-cache api

# Запуск агента с custom переменными
docker-compose run -e SQL_API_URL=http://custom-api:8080 --rm sql-agent sql_database_agent "запрос"
```

## Порты

| Сервис    | Порт  | Описание                    |
|-----------|-------|----------------------------|
| PostgreSQL| 18788 | База данных                 |
| Adminer   | 18789 | Web UI для БД              |
| API       | 18790 | REST API для SQL запросов   |

## Веб-интерфейс Adminer

Откройте http://localhost:18789 для доступа к Adminer:

- **System**: PostgreSQL
- **Server**: postgres:18788
- **Username**: admin
- **Password**: Lol770905!
- **Database**: sgr_memory_vault

## Структура файлов

```
sql-agent/
├── Dockerfile                  # Dockerfile для SQL Agent
├── docker-compose.yml          # Основной docker-compose
├── .dockerignore               # Игнорируемые файлы для Docker
├── config.yaml                 # Конфигурация LLM
├── agents.yaml                 # Определения агентов
├── run_agent.py                # Точка входа агента
├── sgr_agent_core/             # Локальная библиотека
│   └── tools/sql_agent/        # SQL инструменты
├── postgres-adminer-setup/
│   ├── Dockerfile.api          # Dockerfile для API
│   ├── requirements.txt        # Зависимости API
│   ├── api/                    # Код API
│   ├── init_db.sql             # Инициализация БД
│   └── sample_data.sql         # Тестовые данные
├── logs/                       # Логи (монтируется как volume)
└── reports/                    # Отчёты (монтируется как volume)
```

## Troubleshooting

### API недоступен
```bash
# Проверить статус контейнеров
docker-compose ps

# Проверить логи API
docker-compose logs api

# Проверить health
docker-compose exec api wget -qO- http://localhost:18790/health
```

### База данных не подключается
```bash
# Проверить статус PostgreSQL
docker-compose logs postgres

# Подключиться напрямую
docker-compose exec postgres psql -U admin -d sgr_memory_vault -p 18788
```

### Агент не находит API
```bash
# Убедитесь что API запущен и healthy
docker-compose ps

# Проверить сетевое подключение
docker-compose run --rm sql-agent sh -c "wget -qO- http://api:18790/health"
```

## Разработка

### Локальный запуск без Docker

```bash
# Установить зависимости
pip install -e .

# Запустить PostgreSQL и API в Docker
docker-compose up -d postgres api

# Запустить агента локально (использует localhost:18790)
python run_agent.py sql_database_agent "Ваш запрос"
```

### Пересборка после изменений кода

```bash
# Пересобрать только sql-agent
docker-compose build sql-agent

# Пересобрать всё
docker-compose build --no-cache
```
