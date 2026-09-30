from fastapi import FastAPI

from app.database import init_db

init_db() #서버 시작 -> 테이블 생성 및 데이터 입력

app = FastAPI(
    title="AIE Week3 - Unit Converter",
    description="ERD 기반 3계층(Router-Service-Repository) 단위 변환 API",
)


@app.get("/")
def root():
    return {"message": "AIE week3 server is running"}