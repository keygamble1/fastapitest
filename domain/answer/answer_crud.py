

from datetime import datetime

from domain.answer.answer_schema import AnswerCreate, AnswerUpdate
from models import Answer, Question, User
from sqlalchemy.orm import Session


def vote_answer(db: Session,db_answer:Answer,db_user:User):
    db_answer.voter.append(db_user)
    db.commit()
def delete_answer(db: Session,db_answer:Answer):
    db.delete(db_answer)
    db.commit()

def update_answer(db: Session,db_answer:Answer,
                  answer_update:AnswerUpdate):
    db_answer.content=answer_update.content
    db_answer.modify_date=datetime.now()
    db.add(db_answer)
    db.commit()
def get_answer(db: Session,answer_id:int):
    return db.query(Answer).get(answer_id)
# 이건다 받는입장임

def create_answer(db:Session,question:Question,answer_create:AnswerCreate,user:User):
    db_answer=Answer(question=question,
                     content=answer_create.content,
                     create_date=datetime.now(),
                     user=user)
    db.add(db_answer)
    db.commit()