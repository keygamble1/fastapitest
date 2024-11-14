

from datetime import datetime
from sys import prefix

from database import get_db
from domain.answer import answer_crud, answer_schema
from domain.answer.answer_schema import AnswerCreate
from domain.question import question_crud
from domain.user.user_router import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from models import Answer, Question, User
from sqlalchemy.orm import Session
from starlette import status

router=APIRouter(
    prefix='/api/answer',
)
# crud에 전달하는 입장

@router.post("/vote",status_code=status.HTTP_204_NO_CONTENT)
def answer_vote(_answer_vote:answer_schema.AnswerVote,
                db: Session=Depends(get_db),
                current_user:User=Depends(get_current_user)):
    # Depends는 의존성이라서 db를 가져온후 다하면Depend(get_db)가 시작하게됨
    db_answer=answer_crud.get_answer(db,_answer_vote.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터x")
    answer_crud.vote_answer(db,db_answer=db_answer,db_user=current_user)
@router.delete("/delete",status_code=status.HTTP_204_NO_CONTENT)
def answer_delete(_answer_delete:answer_schema.AnswerDelete,
                  db: Session=Depends(get_db),
                  current_user=Depends(get_current_user)):
    db_answer=answer_crud.get_answer(db,_answer_delete.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터x")
    if current_user.id != db_answer.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제권한x")
    answer_crud.delete_answer(db=db,db_answer=db_answer)
@router.put("/update",status_code=status.HTTP_204_NO_CONTENT)
def answer_update(_answer_update:answer_schema.AnswerUpdate,
                  db: Session=Depends(get_db),
                  current_user:User=Depends(get_current_user)):
    db_answer=answer_crud.get_answer(db,answer_id=_answer_update.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    if current_user.id != db_answer.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    answer_crud.update_answer(db,db_answer=db_answer,answer_update=_answer_update)

@router.get('/detail/{answer_id}',response_model=answer_schema.Answer)
def answer_detail(answer_id:int,db: Session=Depends(get_db)):
    answer=answer_crud.get_answer(db,answer_id=answer_id)
    return answer

@router.post("/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_create(question_id: int,
                  _answer_create: answer_schema.AnswerCreate,
                  db: Session = Depends(get_db),
                  current_user:User=Depends(get_current_user)):

    # create answer
    
    question = question_crud.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    answer_crud.create_answer(db, question=question,
                              answer_create=_answer_create,
                              user=current_user)