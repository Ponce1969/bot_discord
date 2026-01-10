# acciones/registrarse.py

from base.database import User, get_db


async def register(discord_id: str, username: str) -> User:
    db = next(get_db())
    user = User(discord_id=discord_id, username=username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
