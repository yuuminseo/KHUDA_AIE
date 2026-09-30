from pydantic import BaseModel, ConfigDict


class UnitResponse(BaseModel): #단위 조회
    model_config = ConfigDict(from_attributes=True)

    unit_id: int
    unitname: str
    to_meter_ratio: float
    category_id: int
    user_id: int | None  #None이면 기본 단위


class ConvertResponse(BaseModel): #단위 변환
    from_unit: str
    to_unit: str
    value: float
    result: float