from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from app.database import Unit


def get_unit(db: Session, unit_id: int) -> Unit | None:
    return db.get(Unit, unit_id) #user id로 단위 조회


def get_visible_units(db: Session, user_id: int | None,
                      category_id: int | None = None) -> list[Unit]:

    stmt = select(Unit).where(
        or_(Unit.user_id.is_(None), Unit.user_id == user_id)
    )
    if category_id is not None:
        stmt = stmt.where(Unit.category_id == category_id)
    return list(db.scalars(stmt.order_by(Unit.unit_id)))