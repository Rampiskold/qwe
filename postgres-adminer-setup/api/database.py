"""
Модуль для работы с базой данных.

Предоставляет пул подключений и функции для безопасного выполнения запросов к PostgreSQL.
"""
import asyncpg
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager
from .config import settings


class Database:
    """
    Класс для управления подключениями к базе данных.
    
    Использует пул соединений для эффективной работы с PostgreSQL
    и предоставляет методы для выполнения запросов.
    """
    
    def __init__(self):
        """Инициализирует объект базы данных без создания пула."""
        self.pool: Optional[asyncpg.Pool] = None
    
    async def connect(self) -> None:
        """
        Создает пул подключений к базе данных.
        
        Устанавливает соединение с PostgreSQL используя настройки из конфига,
        чтобы обеспечить эффективное управление подключениями.
        """
        self.pool = await asyncpg.create_pool(
            host=settings.database_host,
            port=settings.database_port,
            database=settings.database_name,
            user=settings.database_user,
            password=settings.database_password,
            min_size=2,
            max_size=10,
            command_timeout=60
        )
    
    async def disconnect(self) -> None:
        """
        Закрывает пул подключений к базе данных.
        
        Корректно освобождает все ресурсы при завершении работы приложения.
        """
        if self.pool:
            await self.pool.close()
    
    @asynccontextmanager
    async def acquire(self):
        """
        Контекстный менеджер для получения подключения из пула.
        
        Yields:
            asyncpg.Connection: Подключение к базе данных
        """
        async with self.pool.acquire() as connection:
            yield connection
    
    async def get_tables_with_pagination(
        self, 
        page: int = 1, 
        page_size: int = 10
    ) -> Dict[str, Any]:
        """
        Получает список таблиц из базы данных с пагинацией.
        
        Запрашивает информацию о таблицах из information_schema,
        чтобы предоставить пользователю структурированный список с метаданными.
        
        Args:
            page (int): Номер страницы (начиная с 1)
            page_size (int): Количество записей на странице
            
        Returns:
            Dict[str, Any]: Словарь с таблицами, общим количеством и информацией о пагинации
        """
        offset = (page - 1) * page_size
        
        async with self.acquire() as conn:
            # Получаем общее количество таблиц, чтобы рассчитать пагинацию
            count_query = """
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
            """
            total_count = await conn.fetchval(count_query)
            
            # Получаем таблицы с пагинацией и дополнительной информацией, включая комментарии
            tables_query = """
                SELECT 
                    t.table_name,
                    t.table_type,
                    pg_size_pretty(pg_total_relation_size(quote_ident(t.table_name)::regclass)) as table_size,
                    (SELECT COUNT(*) 
                     FROM information_schema.columns c 
                     WHERE c.table_name = t.table_name 
                     AND c.table_schema = 'public') as column_count,
                    obj_description((quote_ident(t.table_name))::regclass, 'pg_class') as table_comment
                FROM information_schema.tables t
                WHERE t.table_schema = 'public' 
                AND t.table_type = 'BASE TABLE'
                ORDER BY t.table_name
                LIMIT $1 OFFSET $2
            """
            rows = await conn.fetch(tables_query, page_size, offset)
            
            tables = [dict(row) for row in rows]
            
            return {
                "tables": tables,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_count": total_count,
                    "total_pages": (total_count + page_size - 1) // page_size
                }
            }
    
    async def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """
        Получает схему указанной таблицы.
        
        Извлекает детальную информацию о колонках таблицы из information_schema,
        чтобы предоставить полное описание структуры таблицы.
        
        Args:
            table_name (str): Название таблицы
            
        Returns:
            Dict[str, Any]: Словарь со схемой таблицы, включая колонки и их свойства
            
        Raises:
            ValueError: Если таблица не найдена
        """
        async with self.acquire() as conn:
            # Проверяем существование таблицы, чтобы избежать SQL-инъекций
            check_query = """
                SELECT EXISTS (
                    SELECT 1 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = $1
                )
            """
            exists = await conn.fetchval(check_query, table_name)
            
            if not exists:
                raise ValueError(f"Table '{table_name}' not found")
            
            # Получаем детальную схему таблицы с комментариями к колонкам
            schema_query = """
                SELECT 
                    c.column_name,
                    c.data_type,
                    c.character_maximum_length,
                    c.numeric_precision,
                    c.numeric_scale,
                    c.is_nullable,
                    c.column_default,
                    c.ordinal_position,
                    CASE 
                        WHEN pk.column_name IS NOT NULL THEN true 
                        ELSE false 
                    END as is_primary_key,
                    CASE 
                        WHEN fk.column_name IS NOT NULL THEN true 
                        ELSE false 
                    END as is_foreign_key,
                    col_description((quote_ident($1))::regclass, c.ordinal_position) as column_comment
                FROM information_schema.columns c
                LEFT JOIN (
                    SELECT ku.column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage ku
                        ON tc.constraint_name = ku.constraint_name
                        AND tc.table_schema = ku.table_schema
                    WHERE tc.constraint_type = 'PRIMARY KEY'
                        AND tc.table_name = $1
                        AND tc.table_schema = 'public'
                ) pk ON c.column_name = pk.column_name
                LEFT JOIN (
                    SELECT ku.column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage ku
                        ON tc.constraint_name = ku.constraint_name
                        AND tc.table_schema = ku.table_schema
                    WHERE tc.constraint_type = 'FOREIGN KEY'
                        AND tc.table_name = $1
                        AND tc.table_schema = 'public'
                ) fk ON c.column_name = fk.column_name
                WHERE c.table_name = $1
                    AND c.table_schema = 'public'
                ORDER BY c.ordinal_position
            """
            rows = await conn.fetch(schema_query, table_name)
            
            columns = [dict(row) for row in rows]
            
            # Получаем индексы таблицы для дополнительной информации
            indexes_query = """
                SELECT
                    i.relname as index_name,
                    a.attname as column_name,
                    ix.indisunique as is_unique,
                    ix.indisprimary as is_primary
                FROM pg_class t
                JOIN pg_index ix ON t.oid = ix.indrelid
                JOIN pg_class i ON i.oid = ix.indexrelid
                JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = ANY(ix.indkey)
                WHERE t.relname = $1
                ORDER BY i.relname, a.attnum
            """
            index_rows = await conn.fetch(indexes_query, table_name)
            indexes = [dict(row) for row in index_rows]
            
            # Получаем комментарий к таблице
            table_comment_query = """
                SELECT obj_description((quote_ident($1))::regclass, 'pg_class') as table_comment
            """
            table_comment = await conn.fetchval(table_comment_query, table_name)
            
            return {
                "table_name": table_name,
                "table_comment": table_comment,
                "columns": columns,
                "indexes": indexes,
                "column_count": len(columns)
            }
    
    async def execute_sql_query(self, sql_query: str) -> Dict[str, Any]:
        """
        Выполняет SQL запрос и возвращает результат.
        
        Выполняет произвольный SQL запрос к базе данных,
        чтобы предоставить гибкий доступ к данным для анализа.
        
        Args:
            sql_query (str): SQL запрос для выполнения
            
        Returns:
            Dict[str, Any]: Результат запроса с данными и метаданными
            
        Raises:
            Exception: Если запрос содержит ошибку или запрещенные операции
        """
        # Проверяем, что это SELECT запрос (безопасность)
        sql_lower = sql_query.strip().lower()
        if not sql_lower.startswith('select'):
            raise ValueError("Only SELECT queries are allowed for security reasons")
        
        # Запрещаем опасные операции
        dangerous_keywords = ['drop', 'delete', 'truncate', 'insert', 'update', 'alter', 'create']
        for keyword in dangerous_keywords:
            if keyword in sql_lower:
                raise ValueError(f"Query contains forbidden keyword: {keyword}")
        
        async with self.acquire() as conn:
            try:
                # Выполняем запрос
                rows = await conn.fetch(sql_query)
                
                if not rows:
                    return {
                        "columns": [],
                        "rows": [],
                        "row_count": 0,
                        "message": "Query executed successfully but returned no rows"
                    }
                
                # Получаем названия колонок
                columns = list(rows[0].keys())
                
                # Преобразуем результаты в список словарей
                data = [dict(row) for row in rows]
                
                return {
                    "columns": columns,
                    "rows": data,
                    "row_count": len(data),
                    "query": sql_query
                }
                
            except Exception as e:
                raise Exception(f"SQL execution error: {str(e)}")


# Глобальный экземпляр базы данных для использования в приложении
db = Database()
