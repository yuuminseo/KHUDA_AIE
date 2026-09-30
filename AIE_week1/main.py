from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="AIE Week1 - Length Converter")

UNITS = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
    "inch": 0.0254,
    "ft": 0.3048,
    "yard": 0.9144,
    "mile": 1609.344,
}


@app.get("/")
def root():
    return {"message": "AIE week1 length converter is running"}


@app.get("/units")
def list_units():
    return {"units": list(UNITS.keys())}


@app.get("/convert")
def convert(
    value: float = Query(..., description="변환할 값"),
    from_unit: str = Query(..., description="변환할 단위 (예: km)"),
    to_unit: str = Query(..., description="목표 단위 (예: m)"),
):
    if from_unit not in UNITS or to_unit not in UNITS:
        raise HTTPException(
            status_code=400,
            detail=f"지원하지 않는 단위입니다. 사용 가능한 단위: {', '.join(UNITS)}",
        )

    result = value * UNITS[from_unit] / UNITS[to_unit]

    return {
        "from_unit": from_unit,
        "to_unit": to_unit,
        "value": value,
        "result": round(result, 6),
    }