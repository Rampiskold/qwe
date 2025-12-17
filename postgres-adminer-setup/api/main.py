"""
Главный модуль FastAPI приложения.

Определяет эндпоинты для безопасного доступа к базе данных PostgreSQL
и управляет жизненным циклом приложения.
"""
from fastapi import FastAPI, Depends, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from contextlib import asynccontextmanager
from typing import Dict, Any, List
from datetime import timedelta, datetime
from pydantic import BaseModel
import json

from .database import db
from .auth import get_current_user_basic, create_access_token
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управляет жизненным циклом приложения.
    
    Подключается к базе данных при старте приложения,
    чтобы обеспечить готовность к обработке запросов,
    и корректно отключается при завершении работы.
    
    Args:
        app (FastAPI): Экземпляр приложения
    """
    # Startup: подключаемся к базе данных
    await db.connect()
    print("✅ Connected to database")
    
    yield
    
    # Shutdown: отключаемся от базы данных
    await db.disconnect()
    print("✅ Disconnected from database")


# Создаем экземпляр FastAPI приложения
app = FastAPI(
    title="SGR PostgreSQL API",
    description="API для доступа к базе данных PostgreSQL",
    version="1.0.0",
    lifespan=lifespan
)

# Настраиваем CORS для безопасного доступа из браузера
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic модель для SQL запроса
class SQLQueryRequest(BaseModel):
    """
    Модель запроса для выполнения SQL.
    
    Attributes:
        query (str): SQL запрос для выполнения
    """
    query: str


def format_result_to_markdown(result: Dict[str, Any]) -> str:
    """
    Форматирует результат SQL запроса в красивый Markdown.
    
    Создает таблицу в формате Markdown с результатами запроса,
    чтобы обеспечить читаемое представление данных.
    
    Args:
        result (Dict[str, Any]): Результат выполнения SQL запроса
        
    Returns:
        str: Отформатированная Markdown таблица
    """
    if result['row_count'] == 0:
        return f"# SQL Query Result\n\n**Query:** `{result.get('query', 'N/A')}`\n\n**Result:** No rows returned\n"
    
    columns = result['columns']
    rows = result['rows']
    
    # Начинаем формировать Markdown
    md = f"# SQL Query Result\n\n"
    md += f"**Query:** `{result.get('query', 'N/A')}`\n\n"
    md += f"**Rows returned:** {result['row_count']}\n\n"
    md += "---\n\n"
    
    # Создаем заголовок таблицы
    md += "| " + " | ".join(columns) + " |\n"
    md += "|" + "|".join(["---" for _ in columns]) + "|\n"
    
    # Добавляем строки данных
    for row in rows:
        row_values = []
        for col in columns:
            value = row.get(col)
            
            # Форматируем значение
            if value is None:
                formatted_value = "*NULL*"
            elif isinstance(value, (dict, list)):
                formatted_value = f"`{json.dumps(value, ensure_ascii=False)}`"
            elif isinstance(value, datetime):
                formatted_value = value.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(value, bool):
                formatted_value = "✅" if value else "❌"
            else:
                formatted_value = str(value)
            
            row_values.append(formatted_value)
        
        md += "| " + " | ".join(row_values) + " |\n"
    
    return md


@app.get("/", tags=["Health"])
async def root() -> Dict[str, str]:
    """
    Проверка работоспособности API.
    
    Returns:
        Dict[str, str]: Статус сервиса
    """
    return {
        "status": "ok",
        "service": "SGR PostgreSQL API",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, str]:
    """
    Проверка здоровья сервиса и подключения к БД.
    
    Выполняет тестовый запрос к базе данных,
    чтобы убедиться в работоспособности всей системы.
    
    Returns:
        Dict[str, str]: Статус здоровья сервиса
    """
    try:
        async with db.acquire() as conn:
            await conn.fetchval("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }


@app.get("/api/tables", tags=["Database"])
async def get_tables(
    page: int = Query(1, ge=1, description="Номер страницы (начиная с 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Количество записей на странице")
) -> Dict[str, Any]:
    """
    Получает список таблиц из базы данных с пагинацией.
    
    Возвращает информацию о таблицах в базе данных с поддержкой пагинации,
    чтобы эффективно работать с большим количеством таблиц.
    
    Args:
        page (int): Номер страницы (начиная с 1)
        page_size (int): Количество записей на странице (1-100)
        
    Returns:
        Dict[str, Any]: Список таблиц с метаданными и информацией о пагинации
    """
    try:
        result = await db.get_tables_with_pagination(page=page, page_size=page_size)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching tables: {str(e)}"
        )


@app.get("/api/tables/{table_name}/schema", tags=["Database"])
async def get_table_schema(
    table_name: str
) -> Dict[str, Any]:
    """
    Получает схему указанной таблицы.
    
    Возвращает детальную информацию о структуре таблицы,
    чтобы пользователь мог понять её колонки, типы данных и ограничения.
    
    Args:
        table_name (str): Название таблицы
        
    Returns:
        Dict[str, Any]: Схема таблицы с информацией о колонках и индексах
        
    Raises:
        HTTPException: Если таблица не найдена или произошла ошибка
    """
    try:
        result = await db.get_table_schema(table_name)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching table schema: {str(e)}"
        )


@app.post("/api/query", tags=["Database"])
async def execute_sql_query(
    request: SQLQueryRequest
) -> Dict[str, Any]:
    """
    Выполняет SQL запрос и возвращает результат в JSON формате.
    
    Принимает SELECT запрос и возвращает результаты в структурированном виде,
    чтобы обеспечить гибкий доступ к данным для анализа.
    
    Args:
        request (SQLQueryRequest): Объект с SQL запросом
        
    Returns:
        Dict[str, Any]: Результат выполнения запроса с колонками и строками
        
    Raises:
        HTTPException: Если запрос содержит ошибку или запрещенные операции
    """
    try:
        result = await db.execute_sql_query(request.query)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error executing query: {str(e)}"
        )


@app.post("/api/query/markdown", tags=["Database"])
async def execute_sql_query_markdown(
    request: SQLQueryRequest
) -> Response:
    """
    Выполняет SQL запрос и возвращает результат в красивом Markdown формате.
    
    Принимает SELECT запрос и форматирует результаты в виде Markdown таблицы,
    чтобы обеспечить читаемое представление данных для документации и отчетов.
    
    Args:
        request (SQLQueryRequest): Объект с SQL запросом
        
    Returns:
        Response: Результат в формате Markdown (text/markdown)
        
    Raises:
        HTTPException: Если запрос содержит ошибку или запрещенные операции
    """
    try:
        result = await db.execute_sql_query(request.query)
        markdown_output = format_result_to_markdown(result)
        
        return Response(
            content=markdown_output,
            media_type="text/markdown",
            headers={
                "Content-Disposition": "inline; filename=query_result.md"
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error executing query: {str(e)}"
        )


# Обработчик ошибок для более информативных ответов
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Глобальный обработчик исключений.
    
    Перехватывает необработанные исключения и возвращает структурированный ответ,
    чтобы клиент получил понятное сообщение об ошибке.
    
    Args:
        request: HTTP запрос
        exc: Исключение
        
    Returns:
        JSONResponse: Ответ с информацией об ошибке
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )
