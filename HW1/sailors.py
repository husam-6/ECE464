from sqlalchemy import create_engine, func, Integer, String, Column, DateTime, exists, desc, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import rank

base = declarative_base()

engine = create_engine("mysql+pymysql://husam:@localhost/sailors?host=localhost")#, echo=True)
session = Session(engine)

class sailors(base):
    __tablename__ = "sailors"
    sid = Column(Integer, primary_key=True)
    sname = Column(String)
    rating = Column(Integer)
    age = Column(Integer)


tmp = sailors(sid=98, sname='joe mama', rating=7, age=25)
print(tmp.sid, tmp.sname, tmp.rating, tmp.age)

# session.add(tmp)
# session.commit()

class reserves(base):
    __tablename__ = "reserves"
    sid = Column(Integer, primary_key=True)
    bid = Column(Integer, primary_key=True)
    day = Column(DateTime, primary_key=True)

class boats(base):
    __tablename__ = "boats"
    bid = Column(Integer, primary_key=True)
    bname = Column(String)
    color = Column(String)
    length = Column(Integer)

base.metadata.create_all(engine)


####        Test Queries from part 1            ####


connection = engine.connect()
## Question 1
def test_Q1():
    result = connection.execute("select b.bid, b.bname, count(*) as reservations from boats b, reserves r where b.bid = r.bid group by b.bid order by count(*) desc;").fetchall()
    
    #Get count of number of times boat has been reserved
    q = session.query(boats.bid, boats.bname, func.count(boats.bid).label('countr')).filter(reserves.bid==boats.bid).group_by(boats.bid).order_by(desc('countr')).all()

    assert result == q

##double check lol 
def test_Q2():
    result = connection.execute("select s.sname, s.sid from sailors s where not exists (select b.bid from boats b where b.color = 'red' and not exists (select * from reserves r where r.bid = b.bid and r.sid = s.sid));").fetchall()

    #Get all bid's for reserved boats
    subqOne = session.query(reserves.bid).filter(reserves.bid == boats.bid, reserves.sid)

    #Get bid's for the red boats that have not been reserved
    subqTwo = session.query(boats.bid).filter(boats.color=='red', boats.bid.notin_(subqOne))

    #Get sailors who have reserved all red boats
    q = session.query(sailors.sname, sailors.sid, boats.bid).filter(boats.bid.in_(subqTwo)).all()

    assert q == result


def test_Q3():
    result = connection.execute("select distinct s1.sname, s1.sid from sailors s1, reserves r1, boats b1 where s1.sid = r1.sid and r1.bid = b1.bid and b1.color = 'red' and s1.sid not in (select s2.sid from sailors s2, reserves r2, boats b2 where s2.sid=r2.sid and r2.bid=b2.bid and b2.color != 'red');").fetchall()

    #Get Sailors who reserved a non red boat
    subq = session.query(sailors.sid).join(reserves, reserves.sid==sailors.sid).join(boats, boats.bid==reserves.bid).filter(boats.color!='red')

    #Get sailors who reserved a red boat and have not reserved a non red boat
    q = session.query(sailors.sname, sailors.sid).join(reserves, reserves.sid == sailors.sid).join(boats, boats.bid == reserves.bid).filter(boats.color == 'red').filter(~sailors.sid.in_(subq)).distinct(sailors.sid).all()

    assert result == q


def test_Q4(): 
    result = connection.execute("select bid, bname, reservations from (select b.bid, b.bname, count(*) as reservations, rank() over (order by count(*) desc) as rnk from boats b, reserves r where b.bid = r.bid group by b.bid order by count(*) desc)t where rnk=1;").fetchall()

    #Get data and rank based on number of reservations
    subq = session.query(boats.bid, boats.bname, func.count(boats.bid).label('countr'), func.rank().over(order_by=desc(func.count(boats.bid))).label('rank')).join(reserves, reserves.bid==boats.bid).group_by(boats.bid).order_by(desc('countr')).subquery()

    #Get sailors with rank == 1
    q = session.query(subq.c.bid,subq.c.bname,subq.c.countr).filter(subq.c.rank==1).all()

    assert q == result


def test_Q5():
    result = connection.execute("select s.sname, s.sid from sailors s where s.sid not in (select s2.sid from sailors s2, reserves r, boats b where b.bid = r.bid and r.sid = s2.sid and b.color = 'red');").fetchall()

    #Get all sailors who've reserved a red boat
    subq = session.query(sailors.sid).join(reserves, reserves.sid == sailors.sid).join(boats, boats.bid == reserves.bid).filter(boats.color == 'red')
    
    #Get sailors who have not reserved from the subq list
    q = session.query(sailors.sname, sailors.sid).filter(~sailors.sid.in_(subq)).all()

    assert q == result


def test_Q6(): 
    result = connection.execute("select avg(age) from (select s.age as age from sailors s where s.rating = 10)over10;").fetchall()

    #Get average sailor age who have a rating of 10
    q = session.query(func.avg(sailors.age)).filter(sailors.rating == 10).all()

    assert q == result


def test_Q7():
    result = connection.execute("select rating, sid, sname, age from (select s.rating, s.sid, s.sname, s.age, rank() over (partition by s.rating order by s.age) as rnk from sailors s order by s.rating) t where rnk = 1;").fetchall()

    #Get data and rank on age based on rating groupings
    subq = session.query(sailors.rating, sailors.sid, sailors.sname, sailors.age, func.rank().over(order_by=sailors.age, partition_by=sailors.rating).label('rank')).order_by(sailors.rating).subquery()

    #Take rank == 1
    q = session.query(subq.c.rating, subq.c.sid, subq.c.sname, subq.c.age).filter(subq.c.rank == 1).order_by(subq.c.rating).all()
    
    assert q==result


def test_Q8():
    result = connection.execute("select sid, sname, bid, count_r from (select sid, sname, bid, count_r, rank() over (partition by bid order by count_r desc) as rnk from (select s.sid, s.sname, b.bid, count(*) as count_r from sailors s, reserves r, boats b where b.bid = r.bid and s.sid = r.sid group by b.bid, s.sid)t)t2 where rnk =1;").fetchall()

    #Get counts of sailors reserving each boat
    subqOne = session.query(sailors.sname, sailors.sid, boats.bid, func.count(boats.bid).label('countr')).filter(reserves.sid==sailors.sid, reserves.bid == boats.bid).group_by(boats.bid, sailors.sid).subquery()

    #Rank the counts based on bid,sid groupings
    subqTwo = session.query(subqOne.c.sid, subqOne.c.sname, subqOne.c.bid, subqOne.c.countr, func.rank().over(order_by=subqOne.c.countr.desc(), partition_by=subqOne.c.bid).label('rank')).subquery()

    #Take the ranks==1
    q = session.query(subqTwo.c.sid, subqTwo.c.sname, subqTwo.c.bid, subqTwo.c.countr).filter(subqTwo.c.rank==1).all()

    assert q == result

