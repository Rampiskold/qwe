#!/bin/bash

# Скрипт для тестирования API эндпоинтов
# Использование: ./test_api.sh

API_URL="http://localhost:18790"

echo "=========================================="
echo "Тестирование SGR PostgreSQL API"
echo "=========================================="
echo ""

# 1. Health Check
echo "1. Health Check:"
echo "GET $API_URL/health"
curl -s "$API_URL/health" | jq .
echo ""
echo ""

# 2. Root endpoint
echo "2. Root endpoint:"
echo "GET $API_URL/"
curl -s "$API_URL/" | jq .
echo ""
echo ""

# 3. Получить список таблиц (первая страница)
echo "3. Получить список таблиц (страница 1, размер 5):"
echo "GET $API_URL/api/tables?page=1&page_size=5"
curl -s "$API_URL/api/tables?page=1&page_size=5" | jq .
echo ""
echo ""

# 4. Получить все таблицы
echo "4. Получить все таблицы:"
echo "GET $API_URL/api/tables?page=1&page_size=100"
curl -s "$API_URL/api/tables?page=1&page_size=100" | jq .
echo ""
echo ""

# 5. Получить схему конкретной таблицы (если есть)
echo "5. Получить схему таблицы 'app_logs':"
echo "GET $API_URL/api/tables/app_logs/schema"
curl -s "$API_URL/api/tables/app_logs/schema" | jq .
echo ""
echo ""

# 6. Тест несуществующей таблицы
echo "6. Тест несуществующей таблицы:"
echo "GET $API_URL/api/tables/nonexistent_table/schema"
curl -s "$API_URL/api/tables/nonexistent_table/schema" | jq .
echo ""
echo ""

echo "=========================================="
echo "Тестирование завершено!"
echo "=========================================="
