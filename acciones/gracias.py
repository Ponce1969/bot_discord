from sqlalchemy.orm import Session

from base.database import User


def dar_gracias(db: Session, discord_id: str, username: str) -> int:
    user = db.query(User).filter(User.discord_id == discord_id).first()
    if not user:
        user = User(discord_id=discord_id, username=username, thanks_count=0)
        db.add(user)

    if user.thanks_count is None:
        user.thanks_count = 0

    user.thanks_count += 1
    db.commit()
    return user.thanks_count
