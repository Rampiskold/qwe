# 🔍 SQL Query API - Примеры использования

## 📡 Новые эндпоинты

### 1. `/api/query` - Выполнить SQL и получить JSON

**POST** запрос с телом:
```json
{
  "query": "SELECT * FROM table_name LIMIT 10"
}
```

### 2. `/api/query/markdown` - Выполнить SQL и получить Markdown

**POST** запрос с телом:
```json
{
  "query": "SELECT * FROM table_name LIMIT 10"
}
```

## 🛡️ Безопасность

✅ **Разрешены:** только `SELECT` запросы

❌ **Запрещены:** `INSERT`, `UPDATE`, `DELETE`, `DROP`, `TRUNCATE`, `ALTER`, `CREATE`

## 📝 Примеры запросов

### Пример 1: Простой SELECT (JSON)

```bash
curl -X POST "http://localhost:18790/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT * FROM dict_currencies LIMIT 5"
  }'
```

**Ответ:**
```json
{
  "columns": ["id", "code", "name", "symbol", "is_active", "created_at", "updated_at"],
  "rows": [
    {
      "id": 1,
      "code": "RUB",
      "name": "Российский рубль",
      "symbol": "₽",
      "is_active": true,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": null
    }
  ],
  "row_count": 5,
  "query": "SELECT * FROM dict_currencies LIMIT 5"
}
```

### Пример 2: Тот же запрос (Markdown)

```bash
curl -X POST "http://localhost:18790/api/query/markdown" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT * FROM dict_currencies LIMIT 5"
  }'
```

**Ответ:**
```markdown
# SQL Query Result

**Query:** `SELECT * FROM dict_currencies LIMIT 5`

**Rows returned:** 5

---

| id | code | name | symbol | is_active | created_at | updated_at |
|---|---|---|---|---|---|---|
| 1 | RUB | Российский рубль | ₽ | ✅ | 2024-01-01 00:00:00 | *NULL* |
| 2 | USD | Доллар США | $ | ✅ | 2024-01-01 00:00:00 | *NULL* |
| 3 | EUR | Евро | € | ✅ | 2024-01-01 00:00:00 | *NULL* |
```

### Пример 3: Агрегация данных

```bash
curl -X POST "http://localhost:18790/api/query/markdown" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT log_level, COUNT(*) as count FROM app_logs GROUP BY log_level ORDER BY count DESC"
  }'
```

**Ответ в Markdown:**
```markdown
# SQL Query Result

**Query:** `SELECT log_level, COUNT(*) as count FROM app_logs GROUP BY log_level ORDER BY count DESC`

**Rows returned:** 5

---

| log_level | count |
|---|---|
| INFO | 1250 |
| WARNING | 340 |
| ERROR | 89 |
| DEBUG | 45 |
| CRITICAL | 12 |
```

### Пример 4: JOIN запрос

```bash
curl -X POST "http://localhost:18790/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT t.table_name, COUNT(c.column_name) as column_count FROM information_schema.tables t LEFT JOIN information_schema.columns c ON t.table_name = c.table_name WHERE t.table_schema = '\''public'\'' GROUP BY t.table_name ORDER BY column_count DESC LIMIT 5"
  }'
```

### Пример 5: Сложный аналитический запрос

```bash
curl -X POST "http://localhost:18790/api/query/markdown" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT tribe_name, SUM(amount) as total_amount, AVG(amount) as avg_amount FROM budget_actuals ba JOIN dict_tribes dt ON ba.tribe_id = dt.id GROUP BY tribe_name ORDER BY total_amount DESC LIMIT 10"
  }'
```

## 🐍 Python примеры

### Пример 1: Получить JSON результат

```python
import requests

url = "http://localhost:18790/api/query"
payload = {
    "query": "SELECT * FROM dict_currencies LIMIT 5"
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Найдено строк: {result['row_count']}")
for row in result['rows']:
    print(row)
```

### Пример 2: Получить Markdown результат

```python
import requests

url = "http://localhost:18790/api/query/markdown"
payload = {
    "query": "SELECT log_level, COUNT(*) as count FROM app_logs GROUP BY log_level"
}

response = requests.post(url, json=payload)
markdown = response.text

# Сохранить в файл
with open("query_result.md", "w", encoding="utf-8") as f:
    f.write(markdown)

print("Результат сохранен в query_result.md")
```

### Пример 3: Динамический запрос с параметрами

```python
import requests

def execute_query(query: str, format: str = "json"):
    """
    Выполняет SQL запрос через API.
    
    Args:
        query: SQL запрос
        format: 'json' или 'markdown'
    
    Returns:
        Результат запроса
    """
    endpoint = "/api/query" if format == "json" else "/api/query/markdown"
    url = f"http://localhost:18790{endpoint}"
    
    response = requests.post(url, json={"query": query})
    
    if format == "json":
        return response.json()
    else:
        return response.text

# Использование
result = execute_query("SELECT * FROM dict_tribes", format="markdown")
print(result)
```

## 🌐 JavaScript примеры

### Пример 1: Fetch API (JSON)

```javascript
async function executeQuery(query) {
  const response = await fetch('http://localhost:18790/api/query', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query }),
  });
  
  const result = await response.json();
  console.log(`Найдено строк: ${result.row_count}`);
  console.table(result.rows);
}

executeQuery('SELECT * FROM dict_currencies LIMIT 5');
```

### Пример 2: Axios (Markdown)

```javascript
const axios = require('axios');

async function getMarkdownResult(query) {
  const response = await axios.post(
    'http://localhost:18790/api/query/markdown',
    { query },
    { headers: { 'Content-Type': 'application/json' } }
  );
  
  return response.data;
}

getMarkdownResult('SELECT * FROM app_logs LIMIT 10')
  .then(markdown => console.log(markdown));
```

## ⚠️ Обработка ошибок

### Попытка выполнить запрещенный запрос

```bash
curl -X POST "http://localhost:18790/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "DELETE FROM dict_currencies WHERE id = 1"
  }'
```

**Ответ (400 Bad Request):**
```json
{
  "detail": "Query contains forbidden keyword: delete"
}
```

### Синтаксическая ошибка в SQL

```bash
curl -X POST "http://localhost:18790/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT * FORM dict_currencies"
  }'
```

**Ответ (500 Internal Server Error):**
```json
{
  "detail": "Error executing query: syntax error at or near \"FORM\""
}
```

## 🎯 Полезные запросы

### 1. Статистика по таблицам

```sql
SELECT 
    table_name,
    pg_size_pretty(pg_total_relation_size(quote_ident(table_name)::regclass)) as size
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY pg_total_relation_size(quote_ident(table_name)::regclass) DESC;
```

### 2. Топ записей по дате

```sql
SELECT * FROM app_logs 
ORDER BY created_at DESC 
LIMIT 20;
```

### 3. Агрегация с группировкой

```sql
SELECT 
    DATE(created_at) as date,
    log_level,
    COUNT(*) as count
FROM app_logs
GROUP BY DATE(created_at), log_level
ORDER BY date DESC, count DESC;
```

## 📚 Swagger UI

Интерактивная документация доступна по адресу:
**http://localhost:18790/docs**

Там можно протестировать все эндпоинты прямо в браузере!
