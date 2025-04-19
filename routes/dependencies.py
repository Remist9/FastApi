from fastapi import Header, HTTPException
from utils.jwt_handler import verify_token
from utils.redis_cache import get_user_id_from_token


async def get_current_user(token: str = Header(...)):
    try:
        payload = verify_token(token)
        user_id = await get_user_id_from_token(token)
        if not user_id:
            raise HTTPException(
                status_code=401, detail="Token expired or not found")
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
