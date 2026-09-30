from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy.orm import Session

from app import service
from app.database import get_db
from app.schemas import UnitResponse, ConvertResponse

#요청한 사용자 확인
def get_optional_user_id(x_user_id: int | None = Header(default=None)) -> int | None:
    return x_user_id

#
unit_router = APIRouter(prefix="/units", tags=["Unit"])


@unit_router.get("/convert", response_model=ConvertResponse)
def convert_unit( #변환 API #요청을 받아 service의 convert로 값을 전달
    from_unit_id: int = Query(..., description="변환할 단위 ID"),
    to_unit_id: int = Query(..., description="목표 단위 ID"),
    value: float = Query(..., description="변환할 값"),
    user_id: int | None = Depends(get_optional_user_id), #Depends 함수를 실행하여 결과를 user_id에 넣음
    db: Session = Depends(get_db), #Depends 함수를 실행하여 결과를 db에 넣음
):
    return service.convert(db, user_id, from_unit_id, to_unit_id, value)


@unit_router.get("", response_model=list[UnitResponse])
def list_units( #단위 목록 API #요청을 받아 service의 list_units로 값을 전달
    category_id: int | None = Query(None, description="분야 ID로 필터링"),
    user_id: int | None = Depends(get_optional_user_id),
    db: Session = Depends(get_db),
):
    return service.list_units(db, user_id, category_id)