import datetime

from domain.user.user_schema import User
from pydantic import BaseModel, field_validator


class AnswerVote(BaseModel):
    answer_id:int
class AnswerCreate(BaseModel):
    content:str
    
    @field_validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
        # raise=중단
# 스키마사용안하고 라우터함수의 매개변수에 content:str을 추가해 값읽을수없음
# get이아닌 post delete put은 pydantic만 ㅣㄺ을수있꼬
# get은 라우터함수의 매개변수로 읽어야함(path parameter,queryparameter 쿼리스트링)
# url파라미터는 get으로, body(payload)값은 pydantic(rquestbody)로 읽음
class Answer(BaseModel):
    id:int
    content:str
    create_date:datetime.datetime
    user: User | None
    question_id:int
    modify_date:datetime.datetime |None=None
    voter:list[User]=[]
    
# 모델명과 스키마의필드명은같아야함
class AnswerUpdate(AnswerCreate):
    answer_id:int

class AnswerDelete(BaseModel):
    answer_id:int
    