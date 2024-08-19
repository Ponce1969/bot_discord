# acciones/registrarse.py

from sqlalchemy.orm import Session
from base.database import get_db, User


async def register(discord_id: str, username: str) -> User:
    db = next(get_db())
    user = User(discord_id=discord_id, username=username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
