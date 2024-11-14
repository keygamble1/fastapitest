# create로 일단 틀만듬
from pydantic import BaseModel, EmailStr, field_validator
from pydantic_core.core_schema import FieldValidationInfo


# schema에 저장되고, validator에서 확인,후에 create_user는 crud 함수일뿐db에 아직안넣음
# user_crud 만들고 일곡 업뎃 deleete할뿐임 일단 저장형태로만 사용
# schema 임시저장용이라고보자
class User(BaseModel):
    id: int
    username: str
    email: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
class UserCreate(BaseModel):
    username:str
    password1:str
    password2:str
    email:EmailStr
    
    @field_validator('username','password1','password2','email')
    def not_empty(cls,v):
        if not v or not v.strip():
            raise ValueError('빈값x')
        return v
    
    @field_validator('password2')
    def password_match(cls,v,info:FieldValidationInfo):
        if 'password1' in info.data and v!=info.data['password1']:
            raise ValueError('비밀번호일치x')
        return v
    