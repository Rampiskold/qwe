"""
Модуль аутентификации и авторизации.

Предоставляет функции для безопасной проверки учетных данных
и создания JWT токенов для защиты API эндпоинтов.
"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from .config import settings


# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Схемы безопасности
security_basic = HTTPBasic()
security_bearer = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие пароля его хешу.
    
    Args:
        plain_password (str): Пароль в открытом виде
        hashed_password (str): Хешированный пароль
        
    Returns:
        bool: True если пароль совпадает, иначе False
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Создает хеш пароля для безопасного хранения.
    
    Args:
        password (str): Пароль в открытом виде
        
    Returns:
        str: Хешированный пароль
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Создает JWT токен доступа.
    
    Генерирует подписанный токен с указанным временем жизни,
    чтобы обеспечить безопасную аутентификацию пользователей.
    
    Args:
        data (dict): Данные для включения в токен
        expires_delta (Optional[timedelta]): Время жизни токена
        
    Returns:
        str: Закодированный JWT токен
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.api_access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.api_secret_key, algorithm=settings.api_algorithm)
    
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Проверяет и декодирует JWT токен.
    
    Валидирует подпись токена и извлекает данные,
    чтобы убедиться в подлинности запроса.
    
    Args:
        token (str): JWT токен
        
    Returns:
        dict: Декодированные данные токена
        
    Raises:
        HTTPException: Если токен невалиден или истек
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.api_secret_key, algorithms=[settings.api_algorithm])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
            
        return payload
    except JWTError:
        raise credentials_exception


async def get_current_user_basic(credentials: HTTPBasicCredentials = Depends(security_basic)) -> str:
    """
    Проверяет учетные данные Basic Auth.
    
    Валидирует имя пользователя и пароль из HTTP Basic Authentication,
    чтобы обеспечить доступ только авторизованным пользователям.
    
    Args:
        credentials (HTTPBasicCredentials): Учетные данные из заголовка
        
    Returns:
        str: Имя пользователя
        
    Raises:
        HTTPException: Если учетные данные неверны
    """
    # В продакшене пароль должен быть захеширован в БД
    # Для простоты используем прямое сравнение
    is_correct_username = credentials.username == settings.api_username
    is_correct_password = credentials.password == settings.api_password
    
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return credentials.username


async def get_current_user_bearer(credentials: HTTPAuthorizationCredentials = Depends(security_bearer)) -> dict:
    """
    Проверяет JWT токен из Bearer Authentication.
    
    Валидирует токен доступа из заголовка Authorization,
    чтобы обеспечить безопасный доступ к защищенным эндпоинтам.
    
    Args:
        credentials (HTTPAuthorizationCredentials): Токен из заголовка
        
    Returns:
        dict: Данные пользователя из токена
        
    Raises:
        HTTPException: Если токен невалиден
    """
    return verify_token(credentials.credentials)
