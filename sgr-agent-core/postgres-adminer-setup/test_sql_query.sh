#!/bin/bash

# Скрипт для тестирования SQL query эндпоинтов
# Использование: ./test_sql_query.sh

API_URL="http://localhost:18790"

echo "=========================================="
echo "Тестирование SQL Query эндпоинтов"
echo "=========================================="
echo ""

# 1. Простой SELECT запрос (JSON)
echo "1. Простой SELECT запрос (JSON формат):"
echo "POST $API_URL/api/query"
curl -s -X POST "$API_URL/api/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * FROM dict_currencies LIMIT 5"}' | jq .
echo ""
echo ""

# 2. Тот же запрос в Markdown формате
echo "2. Тот же запрос (Markdown формат):"
echo "POST $API_URL/api/query/markdown"
curl -s -X POST "$API_URL/api/query/markdown" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * FROM dict_currencies LIMIT 5"}'
echo ""
echo ""

# 3. Запрос с агрегацией (JSON)
echo "3. Запрос с агрегацией (JSON формат):"
echo "POST $API_URL/api/query"
curl -s -X POST "$API_URL/api/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT table_name, column_count FROM (SELECT t.table_name, COUNT(*) as column_count FROM information_schema.tables t JOIN information_schema.columns c ON t.table_name = c.table_name WHERE t.table_schema = '\''public'\'' GROUP BY t.table_name) AS subq ORDER BY column_count DESC LIMIT 5"}' | jq .
echo ""
echo ""

# 4. Тот же запрос в Markdown
echo "4. Тот же запрос (Markdown формат):"
echo "POST $API_URL/api/query/markdown"
curl -s -X POST "$API_URL/api/query/markdown" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT table_name, column_count FROM (SELECT t.table_name, COUNT(*) as column_count FROM information_schema.tables t JOIN information_schema.columns c ON t.table_name = c.table_name WHERE t.table_schema = '\''public'\'' GROUP BY t.table_name) AS subq ORDER BY column_count DESC LIMIT 5"}'
echo ""
echo ""

# 5. Попытка выполнить запрещенный запрос (должна быть ошибка)
echo "5. Попытка выполнить DELETE запрос (должна быть ошибка):"
echo "POST $API_URL/api/query"
curl -s -X POST "$API_URL/api/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "DELETE FROM dict_currencies WHERE id = 1"}' | jq .
echo ""
echo ""

# 6. Запрос с JOIN (Markdown)
echo "6. Запрос из app_logs (Markdown формат):"
echo "POST $API_URL/api/query/markdown"
curl -s -X POST "$API_URL/api/query/markdown" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT log_level, COUNT(*) as count FROM app_logs GROUP BY log_level ORDER BY count DESC"}'
echo ""
echo ""

echo "=========================================="
echo "Тестирование завершено!"
echo "=========================================="
