# SGR PostgreSQL API

Безопасный FastAPI сервис для доступа к базе данных PostgreSQL с аутентификацией.

## 🚀 Быстрый старт

### Запуск всех сервисов

```bash
cd /srv/sgr-agetn-core-tool-search-context-compression/postgres-adminer-setup
docker compose up -d
```

### Проверка статуса

```bash
docker compose ps
```

## 📡 Эндпоинты API

API доступен по адресу: `http://localhost:18790`

### 1. Health Check

**GET** `/health`

Проверка работоспособности API и подключения к БД.

```bash
curl http://localhost:18790/health
```

Ответ:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### 2. Аутентификация

**POST** `/auth/token`

Получение JWT токена (Basic Auth).

```bash
curl -X POST http://localhost:18790/auth/token \
  -u admin:secure_api_password_2024
```

Ответ:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 3. Получить список таблиц (с пагинацией)

**GET** `/api/tables`

Параметры:
- `page` (int, optional): Номер страницы (по умолчанию: 1)
- `page_size` (int, optional): Количество записей на странице (по умолчанию: 10, максимум: 100)

**Пример с Basic Auth:**

```bash
curl -X GET "http://localhost:18790/api/tables?page=1&page_size=10" \
  -u admin:secure_api_password_2024
```

**Пример с Bearer Token:**

```bash
# Сначала получаем токен
TOKEN=$(curl -s -X POST http://localhost:18790/auth/token \
  -u admin:secure_api_password_2024 | jq -r '.access_token')

# Используем токен для запроса
curl -X GET "http://localhost:18790/api/tables?page=1&page_size=10" \
  -H "Authorization: Bearer $TOKEN"
```

Ответ:
```json
{
  "tables": [
    {
      "table_name": "users",
      "table_type": "BASE TABLE",
      "table_size": "16 kB",
      "column_count": 5
    },
    {
      "table_name": "products",
      "table_type": "BASE TABLE",
      "table_size": "32 kB",
      "column_count": 8
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 10,
    "total_count": 15,
    "total_pages": 2
  }
}
```

### 4. Получить схему таблицы

**GET** `/api/tables/{table_name}/schema`

Параметры:
- `table_name` (string, required): Название таблицы

**Пример:**

```bash
curl -X GET "http://localhost:18790/api/tables/users/schema" \
  -u admin:secure_api_password_2024
```

Ответ:
```json
{
  "table_name": "users",
  "columns": [
    {
      "column_name": "id",
      "data_type": "integer",
      "character_maximum_length": null,
      "numeric_precision": 32,
      "numeric_scale": 0,
      "is_nullable": "NO",
      "column_default": "nextval('users_id_seq'::regclass)",
      "ordinal_position": 1,
      "is_primary_key": true,
      "is_foreign_key": false
    },
    {
      "column_name": "username",
      "data_type": "character varying",
      "character_maximum_length": 255,
      "numeric_precision": null,
      "numeric_scale": null,
      "is_nullable": "NO",
      "column_default": null,
      "ordinal_position": 2,
      "is_primary_key": false,
      "is_foreign_key": false
    }
  ],
  "indexes": [
    {
      "index_name": "users_pkey",
      "column_name": "id",
      "is_unique": true,
      "is_primary": true
    }
  ],
  "column_count": 5
}
```

## 🔐 Безопасность

### Методы аутентификации

API поддерживает два метода аутентификации:

1. **HTTP Basic Authentication** - простая аутентификация для быстрого доступа
2. **JWT Bearer Token** - токен-based аутентификация для более безопасного доступа

### Учетные данные по умолчанию

⚠️ **ВАЖНО**: Измените эти данные в продакшене!

- **Username**: `admin`
- **Password**: `secure_api_password_2024`
- **Secret Key**: Задается в `API_SECRET_KEY` переменной окружения

### Изменение учетных данных

Отредактируйте `docker-compose.yml`:

```yaml
environment:
  - API_USERNAME=your_username
  - API_PASSWORD=your_secure_password
  - API_SECRET_KEY=your-super-secret-key-min-32-chars
```

## 📚 Интерактивная документация

FastAPI автоматически генерирует интерактивную документацию:

- **Swagger UI**: http://localhost:18790/docs
- **ReDoc**: http://localhost:18790/redoc

## 🐳 Docker команды

### Пересборка API сервиса

```bash
docker compose build api
docker compose up -d api
```

### Просмотр логов

```bash
# Все сервисы
docker compose logs -f

# Только API
docker compose logs -f api
```

### Остановка сервисов

```bash
docker compose down
```

### Полная очистка (включая volumes)

```bash
docker compose down -v
```

## 🛠️ Разработка

### Структура проекта

```
postgres-adminer-setup/
├── api/
│   ├── __init__.py
│   ├── main.py          # Основное приложение FastAPI
│   ├── config.py        # Конфигурация
│   ├── database.py      # Работа с БД
│   ├── auth.py          # Аутентификация
│   └── .env             # Переменные окружения (локально)
├── Dockerfile.api       # Dockerfile для API
├── docker-compose.yml   # Конфигурация всех сервисов
├── requirements.txt     # Python зависимости
└── API_README.md        # Эта документация
```

### Локальная разработка (без Docker)

1. Создайте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Настройте переменные окружения в `api/.env`

4. Запустите сервер:

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 18790
```

## 📊 Примеры использования

### Python

```python
import requests
from requests.auth import HTTPBasicAuth

# Базовая аутентификация
auth = HTTPBasicAuth('admin', 'secure_api_password_2024')

# Получить список таблиц
response = requests.get(
    'http://localhost:18790/api/tables',
    auth=auth,
    params={'page': 1, 'page_size': 10}
)
tables = response.json()

# Получить схему таблицы
response = requests.get(
    'http://localhost:18790/api/tables/users/schema',
    auth=auth
)
schema = response.json()
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

const auth = {
  username: 'admin',
  password: 'secure_api_password_2024'
};

// Получить список таблиц
axios.get('http://localhost:18790/api/tables', {
  auth: auth,
  params: { page: 1, page_size: 10 }
})
.then(response => console.log(response.data))
.catch(error => console.error(error));

// Получить схему таблицы
axios.get('http://localhost:18790/api/tables/users/schema', { auth })
.then(response => console.log(response.data))
.catch(error => console.error(error));
```

## 🔧 Troubleshooting

### API не запускается

1. Проверьте логи:
```bash
docker compose logs api
```

2. Убедитесь, что PostgreSQL запущен:
```bash
docker compose ps postgres
```

### Ошибка подключения к БД

1. Проверьте healthcheck PostgreSQL:
```bash
docker compose ps
```

2. Проверьте переменные окружения в `docker-compose.yml`

### Порт 18790 занят

Измените порт в `docker-compose.yml`:
```yaml
ports:
  - "YOUR_PORT:18790"
```

## 📝 Лицензия

Этот проект создан для внутреннего использования SGR.
