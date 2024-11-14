from database import SessionLocal
from models import Answer, Question, User

db=SessionLocal()
db.query(Question).count()
db.query(Answer).count()
db.query(Question).join(Answer).count()
# 위는 질문과 답변이 모두 1을포함한것
# 하지만 질문은없는데 답변만 1인걸찾고싶을때는? outerjoin
# 
user = db.query(User).filter(User.username=='홍길동').first()
db.query(Question).filter(Question.user_id==user.id)
# 위아 아래는 같다
# query는 filter로하고 subquery는 안에서 filter가가능
db.query(Question).outerjoin(Answer).count()
# 하지만 이럴경우 
# Qustion 1 Answer 1 /Questoin 1 Answer 2
# 같이 Question이 중복되서 쿼리가된다
# 내가원하는건 Question1 에서 Answer중 1이 여러개여도 
# Question1과 Answer1만 찾고싶은거임
db.query(Question).outerjoin(Answer).distinct().count()
# Question도 들어가는대신 Answer은 다포함하게 만들어버린것
# 내가원하는건 Question임 Answer의 내용이포함한 Question1개
db.query(Question).outerjoin(Answer).filter(
    Question.content.ilike('%파이썬%') |
    Answer.content.ilike("%파이썬%")).distinct().count()
# 답변작성자도 포함하고싶음 Question이 주니까 Question.userid는있을거
# 하지만 Answer은 content만 조회하는데 여기에 더추가하는건 변수가 더추가되야해서 추천x
# 서브쿼리에 들어갈게 Answer.content와 Answer의 User가 추가되면좋을듯
# 아예 답변과 질문을 분리시키는거임
sub_query=db.query(Answer.question_id,Answer.content,User.username) \
    .outerjoin(User,Answer.user_id==User.id).subquery()

db.query(Question).outerjoin(sub_query,sub_query.c.question_id==Question.id) \
  .filter(sub_query.c.content.ilike('%파이썬%') |
          sub_query.c.username.ilike('%파이썬%')
          ).distinct().count()