

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./myapi.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base.metadata=MetaData(naming_convention=naming_convention)
# 원래는 default값되어있음
# include extends blcok과같은기능?
# with을 쓰기위한것 with은 contextlib.contermanswer를 안쓰면안됨 그리고
# with은 __enter__과 __exit__을 같이써야 가능하며
# 데코레이터안쓸씨 class def __enter__(self):
#   self.db=SessionLocal() return self.db
# def __exit__(self,exc_type,exc_val,exc_db): self.db.close를 써야함
# @contextlib.contextmanager
def get_db():
    # get_dbb를 contextmanager로 변환함
    db=SessionLocal()
    try:
        yield db
        # yield는 with구문에 db를 넘겨주라는 뜻임
    finally:
        # finally는 오류가발생해도 무조건시행 안써도되긴하는데 쓰는게안전
        db.close()
        