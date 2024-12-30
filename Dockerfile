FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r  requirements.txt

ENV BK_POSTGRES_USER=fastapi
ENV BK_POSTGRES_DB=bookstore
ENV BK_POSTGRES_PASSWORD=fastapi_admin
ENV BK_POSTGRES_PORT=5432
ENV BK_POSTGRES_HOST=bookstore_db
ENV BK_APP_TITLE=Library_Management
ENV BK_APP_DESCRIPTION=Application_for_bookstore_management
ENV BK_APP_VERSION=0.0.1
ENV BK_PG_URL=postgresql+asyncpg://${BK_POSTGRES_USER}:${BK_POSTGRES_PASSWORD}@${BK_POSTGRES_HOST}:${BK_POSTGRES_PORT}/${BK_POSTGRES_DB}

COPY . .

EXPOSE 8000
