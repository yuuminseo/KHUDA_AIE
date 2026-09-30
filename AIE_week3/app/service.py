from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import repository


#
def _can_access(owner_id: int | None, user_id: int | None) -> bool:
    return owner_id is None or owner_id == user_id

#사용자가 볼 수 있는 단위 목록을 가져옴
def list_units(db: Session, user_id: int | None, category_id: int | None):
    return repository.get_visible_units(db, user_id, category_id)

#DB에서 사용자가 목표로 변환하는 단위 하나를 가져옴
def get_accessible_unit(db: Session, unit_id: int, user_id: int | None):
    unit = repository.get_unit(db, unit_id)
    if unit is None or not _can_access(unit.user_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{unit_id}번 단위를 찾을 수 없습니다.",
        )
    return unit

#두 단위가 같은 분야인지 확인 후, 미터를 거쳐 값 변환 후 반환
def convert(db: Session, user_id: int | None,
            from_unit_id: int, to_unit_id: int, value: float) -> dict:
    src = get_accessible_unit(db, from_unit_id, user_id)
    dst = get_accessible_unit(db, to_unit_id, user_id)

    if src.category_id != dst.category_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="같은 분야의 단위끼리만 변환할 수 있습니다.",
        )

    meters = value * src.to_meter_ratio
    result = meters / dst.to_meter_ratio

    return {
        "from_unit": src.unitname,
        "to_unit": dst.unitname,
        "value": value,
        "result": round(result, 6),
    }