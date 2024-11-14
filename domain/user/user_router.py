from datetime import datetime, timedelta

from database import get_db
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette import status

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY="9965b2efcb1b41ec9a8747d71cfed87631db66e2218adf51f7433216393b1d49"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")
router=APIRouter(
    prefix='/api/user',
)
@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):

    # check user and password
    user = user_crud.get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }
def get_current_user(token:str=Depends(oauth2_scheme),
                     db: Session=Depends(get_db)):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Colud not validate credentails",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user=user_crud.get_user(db,username=username)
        if user is None:
            raise credentials_exception
        return user

@router.post("/create",status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create:user_schema.UserCreate,db: Session=Depends(get_db)):
    user=user_crud.get_existing_user(db=db,user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='이미 존재하는 사용자.')
    user_crud.create_user(db=db,user_create=_user_create)

