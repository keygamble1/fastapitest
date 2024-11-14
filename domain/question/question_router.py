
from database import get_db
from domain.question import question_crud, question_schema
from domain.question.question_schema import QuestionCreate
from domain.user.user_router import get_current_user
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from models import Question, User
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter(
    prefix="/api/question",
)

# Depends(get_db) Depends=의존성주입처리함수, get_db함수의 반환값으로 db변수로 주입한다는 의미 
# return형은  Session 형의 db라는뜻 
# 즉 get_db는 Session형으로 반환후 db에 넣어버린다는뜻
# response_model=return 값 _question_list는 Questoion스키마로구성된 리스트이다
# 만약 Question스키마에서 content제거시 api출력항목에서 content도 제거됨
@router.delete("/delete",status_code=status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete:question_schema.QuestionDelete,
                    db: Session=Depends(get_db),
                    current_user:User=Depends(get_current_user)):
    db_question=question_crud.get_question(db,question_id=_question_delete.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터x")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제권한x")
    question_crud.delete_question(db=db,db_question=db_question)

@router.put('/update',status_code=status.HTTP_204_NO_CONTENT)
def question_update(_question_updade:question_schema.QuestionUpdate,
                    db: Session=Depends(get_db),
                    current_user:User=Depends(get_current_user)):
    db_question=question_crud.get_question(db,question_id=_question_updade.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터x")
    if current_user.id!=db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정권한x")
    question_crud.update_question(db=db,db_question=db_question,
                                  question_update=_question_updade)
    
@router.get("/list", response_model=question_schema.QuestionList)
def question_list(db:Session=Depends(get_db),
                  page:int=0,size:int=10,keyword:str=''):
    # db:Session이런건 Depneds이라 예외 page,size,keyword가 url에 담겨있음
    total,_question_list=question_crud.get_question_list(
        db,skip=page*size,limit=size,keyword=keyword
    )
    # response_model은 엔드포인트의 리턴값과 동일해야함
    # 기본+추가 속성url로써 서버에서 클라로전달하는걸 엔드포인트라함
    return {
        'total':total,
        'question_list':_question_list
    }
    
    # 메서드처럼쓰는걸 어노테이션으로 묶어서 공용해서 쓰는거
    # with을쓰면 계속 get_dbv를 써야하지만 한번만 의존성주입하면 그걸끝까지쓰는게가능
    # 수동주입안하도됨


    

@router.get('/detail/{question_id}',response_model=question_schema.Question)
def question_detail(question_id:int,db: Session=Depends(get_db)):
    question=question_crud.get_question(db,question_id=question_id)
    return question
    # 스키마를 안에 넣어야 fastapi에서 requestbody쉽게 판별가능
    
@router.post('/create',status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create:QuestionCreate,
                    db: Session=Depends(get_db),
                    current_user:User=Depends(get_current_user)):
    
    question_crud.create_question(db=db,question_create=_question_create
                                    ,user=current_user)
@router.post("/vote",status_code=status.HTTP_204_NO_CONTENT)
def quesiton_vote(_question_vote:question_schema.QuestionVote,
                  db: Session=Depends(get_db),
                  current_user:User=Depends(get_current_user)):
    db_question=question_crud.get_question(db,_question_vote.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터x")
    question_crud.vote_quesiton(db,db_question=db_question,db_user=current_user)
