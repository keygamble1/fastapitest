import datetime

from domain.answer.answer_schema import Answer
from domain.user.user_schema import User
from pydantic import BaseModel, field_validator


class QuestionVote(BaseModel):
    question_id:int
class QuestionDelete(BaseModel):
    question_id:int
    
class QuestionCreate(BaseModel):
    subject:str
    content:str
    
    @field_validator('subject','content')
    # 빈값도 값임
    def not_empty(cls,v):
        if not v or not v.strip():
            raise ValueError('빈값허용x')
        return v
    
class Question(BaseModel):
    id:int
    subject:str
    content:str
    create_date:datetime.datetime
    answers:list[Answer]=[]
    user: User | None
    modify_date:datetime.datetime |None=None
    voter:list[User]=[]
    
    class Config:
        orm_mode=True

class QuestionList(BaseModel):
    total:int=0
    question_list:list[Question]=[]
    
# class 상속할때도 const let처럼 아래에 써줘야함 전역이아님
class QuestionUpdate(QuestionCreate):
    question_id:int