from database import Base
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Table,
                        Text)
from sqlalchemy.orm import relationship

question_voter=Table(
    'question_voter',
    Base.metadata,
    Column('user_id',Integer,ForeignKey('user.id'),primary_key=True),
    Column('question_id',Integer,ForeignKey('question.id'),primary_key=True)
    # 이렇게함으로써 usre는 question_id에 한번만 저장을할수가있다.
    # question은 user의 고유의아이디를 하나씩가지고있고,
    # 그 user만 추천을할수있음 대신 question_id에 user_id가 두명이있을순없다고 primary에 제약조건명시
)

class Question(Base):
    __tablename__="question"
    id=Column(Integer,primary_key=True)
    subject=Column(String,nullable=False)
    content=Column(Text,nullable=False)
    create_date=Column(DateTime,nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="question_users")
    # question_users라고해서 question의 user를 가져오는게아닌 
    # 속성이포함된 question객체들을 가져오는거임
    modify_date=Column(DateTime,nullable=True)
    voter=relationship('User',secondary=question_voter,backref='question_voters')
    # secondary에 쓴 테이블에 데이터가 저장되며 User에서 backref한다고해도 qusetion이아닌

    # many에서 1과 연결하고 1에서 backref를 하게 역참조하게 만든다
    #  secondary에있는 quesiton_voter를 가져오며 question_voter를통해 question을
    # 가져오고싶으면 쿼리를만들어서 그곳을통해 역참조해줘야함 
    # 일단 여기서는 question_voter의 레코드들만 가져온다
    # Question모델통해 생성되면 테이블명은 question이 되어버림

answer_voter=Table(
    'answer_voter',
    Base.metadata,
    Column('user_id',Integer,ForeignKey('user.id'),primary_key=True),
    Column('answer_id',Integer,ForeignKey('answer.id'),primary_key=True)
)
class Answer(Base):
    __tablename__ ="answer"
    id=Column(Integer,primary_key=True)
    content=Column(String,nullable=False)
    create_date=Column(DateTime,nullable=False)
    question_id=Column(Integer,ForeignKey('question.id'))
    question=relationship("Question",backref="answers")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="answer_users")
    voter=relationship("User",secondary=answer_voter,backref="answer_voters")
    # realationship 첫번째인수에 외래키를 넣어버린다라는뜻
    # 없고 secodary라면 다대다로 테이블따로둬서 1:다 를 두개로 묶어버리겠다는뜻임
    
    modify_date=Column(DateTime,nullable=True)

class User(Base):
    __tablename__ ="user"
    id=Column(Integer,primary_key=True)
    username=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    email=Column(String,unique=True,nullable=False)
    