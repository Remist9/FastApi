from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.hash import bcrypt
from routes.dependencies import get_current_user
from configs.database import async_session
from models.user import User
from schemas.user import UserCreate, UserRead

from utils.jwt_handler import create_access_token
from utils.redis_cache import cache_token

router = APIRouter()


async def get_db():
    async with async_session() as session:
        yield session


@router.post("/register", response_model=UserRead)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.login == user_data.login))
    if result.scalar():
        raise HTTPException(status_code=400, detail="Login already exists")

    hashed_password = bcrypt.hash(user_data.password)
    new_user = User(login=user_data.login, password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post("/login")
async def login(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.login == user_data.login))
    user = result.scalar()
    if not user or not bcrypt.verify(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    await cache_token(token, user.id)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def profile(user_id: int = Depends(get_current_user)):
    return {"message": f"Привет, пользователь {user_id}"}
