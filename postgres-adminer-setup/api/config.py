"""
Модуль конфигурации приложения.

Загружает настройки из переменных окружения для подключения к БД и безопасности API.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Класс настроек приложения.
    
    Загружает конфигурацию из переменных окружения для обеспечения
    безопасного подключения к базе данных и настройки API.
    """
    
    # Database settings
    database_host: str = "postgres"
    database_port: int = 18788
    database_name: str = "sgr_memory_vault"
    database_user: str = "admin"
    database_password: str
    
    # API Security
    api_secret_key: str
    api_algorithm: str = "HS256"
    api_access_token_expire_minutes: int = 30
    
    # Basic Auth
    api_username: str = "admin"
    api_password: str
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def database_url(self) -> str:
        """
        Формирует URL для подключения к PostgreSQL.
        
        Returns:
            str: URL подключения в формате postgresql://user:pass@host:port/db
        """
        return f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"


settings = Settings()
