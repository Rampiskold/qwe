# SQL Agent Dockerfile
# Включает локальную библиотеку sgr_agent_core без внешних зависимостей

FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем pyproject.toml для установки зависимостей
COPY pyproject.toml .

# Копируем локальную библиотеку sgr_agent_core (вместо установки из GitHub)
COPY sgr_agent_core/ ./sgr_agent_core/

# Устанавливаем pip и зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Копируем файлы приложения
COPY run_agent.py .
COPY config.yaml .
COPY agents.yaml .
COPY logging_config.yaml .

# Создаём директории для логов и отчётов
RUN mkdir -p logs reports

# Создаём непривилегированного пользователя
RUN useradd -m -u 1000 agent && \
    chown -R agent:agent /app

USER agent

# Точка входа - запуск агента
ENTRYPOINT ["python", "run_agent.py"]

# По умолчанию показываем справку
CMD ["--help"]
