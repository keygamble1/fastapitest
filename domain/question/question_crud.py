from datetime import datetime

from domain.question.question_schema import QuestionCreate, QuestionUpdate
from models import Answer, Question, User
from sqlalchemy import and_
from sqlalchemy.orm import Session


def delete_question(db:Session,db_question: Question):
    db.delete(db_question)
    db.commit()
def update_question(db: Session,db_question: Question,
                    question_update:QuestionUpdate):

    db_question.subject = question_update.subject
    db_question.content = question_update.content
    db_question.modify_date=datetime.now()
    db.add(db_question)
    db.commit()

# all get이 crud라고보면됨 create upde delete  read
def get_question_list(db:Session,skip:int=0,limit:int=10,keyword:str=''):
    question_list=db.query(Question)
    if keyword:
        search='%%{}%%'.format(keyword)
        sub_query=db.query(Answer.question_id,Answer.content,User.username) \
            .outerjoin(User, and_(Answer.user_id==User.id)).subquery()
        question_list=question_list \
            .outerjoin(User) \
            .outerjoin(sub_query,and_(sub_query.c.question_id==Question.id)) \
            .filter(Question.subject.ilike(search) |
                    Question.content.ilike(search) |
                    User.username.ilike(search) |
                    sub_query.c.content.ilike(search) |
                    sub_query.c.username.ilike(search)
                    
                    )  

    total=question_list.count()
    question_list=question_list \
        .order_by(Question.create_date.desc()).offset(skip).limit(limit).all()
    return total,question_list
def vote_quesiton(db: Session,db_question:Question,db_user:User):
    db_question.voter.append(db_user)
    db.commit()

def get_question(db: Session,question_id:int):
    question=db.query(Question).get(question_id)
    return question

def create_question(db: Session,question_create:QuestionCreate,user:User):
    # 유효성검사와동시에 값이 quesiton_create로 전달될것
    db_question=Question(subject=question_create.subject,
                         content=question_create.content,
                         create_date=datetime.now(),
                         user=user)
    db.add(db_question)
    db.commit()
    # fromtend 에서 javascript다운=npm install javascript라이브러리다운하는거
    # 그리고나서 db에 add하고 변경점 저장
    # 계속 실시간 업뎃하면 자료가너무많이쌓여서 commit()으로 저장함
    
    
