

from domain.user.user_schema import UserCreate
from models import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# myapi 에서 pip install backend 벡앤드
# npm install은 java 프론트엔드
# crud와 model은 같아야함 valdaitor인 schema는형식일뿐
def create_user(db:Session,user_create:UserCreate):
    db_user=User(username=user_create.username,
                #  없는건 빈공간으로 생각
                # User() 이렇게되어있는건 빈공간에 넣어라
                # User.이 나오는순간 저장되있는거 불러온다
                 password=pwd_context.hash(user_create.password1),
                 email=user_create.email
                 )
    db.add(db_user)
    db.commit()

def get_existing_user(db: Session,user_create: UserCreate):
    return db.query(User).filter(
        # User은 저장된거, user_create는 막입력한거
        (User.username ==user_create.username) |
        (User.email ==user_create.email)
    ).first()
    
def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()