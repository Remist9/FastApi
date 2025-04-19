from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.hash import bcrypt
from datetime import datetime
from configs.database import async_session
from models.user import User
from routes.dependencies import get_current_user
from schemas.user import UserCreate, UserRead, UserUpdate
from utils.jwt_handler import create_access_token
from utils.redis_cache import cache_token, delete_token

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

    # Обновляем время последней авторизации
    user.last_auth_time = datetime.utcnow()
    await db.commit()

    token = create_access_token({"sub": str(user.id)})
    await cache_token(token, user.id)

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
async def profile(
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user  # FastAPI сам преобразует его в UserRead


@router.post("/logout")
async def logout(token: str = Header(..., convert_underscores=False)):
    await delete_token(token)
    return {"message": "Logged out successfully"}


@router.delete("/delete_me")
async def delete_me(
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    token: str = Header(...)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()

    await delete_token(token)

    return {"message": f"Пользователь {user.login} удалён и разлогинен"}


@router.put("/me/update")
async def update_profile(
    data: UserUpdate,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)

    return {
        "message": "Данные обновлены",
        "user": {
            "firstname": user.firstname,
            "surname": user.surname,
            "location": user.location
        }
    }
