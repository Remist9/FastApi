from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Загружаем переменные из .env
load_dotenv()

# Формируем строку подключения из переменных
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "user_list")
DB_USER = os.getenv("DB_USER", "fastapi_user")
DB_PASS = os.getenv("DB_PASS", "user")

DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Создаём движок
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаём асинхронную сессию
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Базовый класс для моделей
Base = declarative_base()
