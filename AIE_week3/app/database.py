import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import create_engine, select, String, Double, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

#연결 설정
load_dotenv()  #환경변수 등록
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise RuntimeError(".env 파일에 DATABASE_URL이 없습니다.")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    pass

#세션 제공
def get_db():
    db = SessionLocal()
    try:
        yield db #라우터에 세션을 제공하여 요청마다 세션을 열고, 응답이 끝나면 닫음
    finally:
        db.close()

#ERD
class User(Base):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)  # 해시값 저장
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)


class Category(Base):
    __tablename__ = "category"

    category_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    categoryname: Mapped[str] = mapped_column(String(50), nullable=False)
    # NULL = 기본 분야(모두에게 공개), 값 있음 = 해당 사용자 전용
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("user.user_id", ondelete="CASCADE"), nullable=True
    )


class Unit(Base):
    __tablename__ = "unit"

    unit_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    unitname: Mapped[str] = mapped_column(String(50), nullable=False)
    to_meter_ratio: Mapped[float] = mapped_column(Double, nullable=False)  # 1단위 = 몇 m
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("user.user_id", ondelete="CASCADE"), nullable=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.category_id", ondelete="CASCADE"), nullable=False
    )


class Favorite(Base):
    __tablename__ = "favorite"

    favorite_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False
    )
    from_unit_id: Mapped[int] = mapped_column(
        ForeignKey("unit.unit_id", ondelete="CASCADE"), nullable=False
    )
    to_unit_id: Mapped[int] = mapped_column(
        ForeignKey("unit.unit_id", ondelete="CASCADE"), nullable=False
    )

#기본 데이터 및 테이블 생성
DEFAULT_LENGTH_UNITS = { #기본 데이터
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
    "inch": 0.0254,
    "ft": 0.3048,
    "yard": 0.9144,
    "mile": 1609.344,
}


def init_db():
    Base.metadata.create_all(bind=engine) #테이블이 없으면 생성

    with SessionLocal() as db:
        exists = db.scalar(select(Category).where(Category.user_id.is_(None)))
        if exists:
            return

        length = Category(categoryname="길이", user_id=None) #분야 추가
        db.add(length)
        db.flush()

        for name, ratio in DEFAULT_LENGTH_UNITS.items(): #단위 추가
            db.add(Unit(unitname=name, to_meter_ratio=ratio,
                        user_id=None, category_id=length.category_id))
        db.commit()