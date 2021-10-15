from sqlalchemy import create_engine, func, Integer, String, Column, DateTime, desc, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, backref, relationship
from sqlalchemy.sql.schema import ForeignKey

base = declarative_base()

engine = create_engine("mysql+pymysql://husam:@localhost/sailors?host=localhost")#, echo=True)
session = Session(engine)

class sailors(base):
    __tablename__ = "sailors"
    sid = Column(Integer, primary_key=True)
    sname = Column(String)
    rating = Column(Integer)
    age = Column(Integer)

    def __repr__(self): 
        return "<Sailor(id='%s', name='%s', rating='%s')>" %(self.sid, self.sname, self.age)


tmp = sailors(sid=98, sname='joe', rating=7, age=25)
print(tmp)

# session.add(tmp)
# session.commit()

class reserves(base):
    __tablename__ = "reserves"
    sid = Column(Integer, ForeignKey('sailors.sid'))
    bid = Column(Integer, ForeignKey('boats.bid'))
    day = Column(DateTime, primary_key=True)

    sailor = relationship('sailor')

    def __repr__(self):
        return "<Reservation(sailor id='%s', boat id='%s', date='%s')>" % (self.sid, self.bid, self.day)


class boats(base):
    __tablename__ = "boats"
    bid = Column(Integer, primary_key=True)
    bname = Column(String)
    color = Column(String)
    length = Column(Integer)

    reservations = relationship('reservation', backref=backref('boat', cascade='delete'))

    def __repr__(self):
        return "<Boat(boat id='%s', bname id='%s', bcolor='%s')>" % (self.bid, self.bname, self.color)





####        Part 3 Content         ####

#Inventory repair and costs 

class broken(base):
    __tablename__ = "broken"
    br_id = Column(Integer, primary_key=True)
    bid = Column(Integer, primary_key=True)         #Id of broken boat
    sid = Column(Integer, primary_key=True)       #sailor who broke it 
    fixed = Column(Integer)

    boats = relationship('boats')

    def __repr__(self):
        return "<Broken(boat bid='%s', sailor responsible = '%s', fixed = '%s')>" % (self.bid, self.sid, self.fixed)


class costs(base):
    __tablename__ = "costs"
    br_id = Column(Integer, primary_key=True)
    bid = Column(Integer, primary_key=True)
    cost = Column(Integer)                                 #Cost of repairs
    beginRepair = Column(DateTime)                         #Begin date
    dateBroke = Column(DateTime)                           #Broken date
    expected = Column(DateTime)                            #Expected return date

    costs = relationship('costs', backref=backref('costs', cascade='delete'))

    def __repr__(self):
        return "<Costs(broken boat id='%s', cost='%s', expected return = '%s')>" % (self.bid, self.cost, self.expected)

base.metadata.create_all(engine)


####        Test Queries from part 1            ####

connection = engine.connect()
## Question 1
def test_Q1():
    result = connection.execute("select b.bid, b.bname, count(*) as reservations from boats b, reserves r where b.bid = r.bid group by b.bid order by count(*) desc;").fetchall()
    
    #Get count of number of times boat has been reserved
    q = session.query(boats.bid, boats.bname, func.count(boats.bid).label('countr')).filter(reserves.bid==boats.bid).group_by(boats.bid).order_by(desc('countr')).all()

    assert result == q

def test_Q2():    
    result = connection.execute("select sid, sname from (select s.sid, s.sname, count(distinct b.bid) as count_r from sailors s, reserves r, boats b where s.sid = r.sid and b.bid = r.bid and b.color = 'red' group by s.sid)x where x.count_r = (select count(*) from (select distinct b.bid from boats b where b.color = 'red')t);").fetchall()

    #Get count of distinct boat bids with color red
    subqOne = session.query(func.count(boats.bid)).filter(boats.color == 'red').distinct().scalar()

    #Get counts of sailors who reserved distinct red boats
    subqTwo = session.query(sailors.sid, sailors.sname, func.count(boats.bid.distinct()).label('count_r')).join(reserves, reserves.bid == boats.bid).join(sailors, sailors.sid == reserves.sid).filter(boats.color == 'red').group_by(sailors.sid).subquery()

    #Filter out sailors who don't have the same count of reserved distinct red boats as the number of distinct red boats
    q = session.query(subqTwo.c.sid, subqTwo.c.sname).filter(subqTwo.c.count_r == subqOne).all()

    assert q == result


def test_Q3():
    result = connection.execute("select distinct s1.sname, s1.sid from sailors s1, reserves r1, boats b1 where s1.sid = r1.sid and r1.bid = b1.bid and b1.color = 'red' and s1.sid not in (select s2.sid from sailors s2, reserves r2, boats b2 where s2.sid=r2.sid and r2.bid=b2.bid and b2.color != 'red');").fetchall()

    #Get Sailors who reserved a non red boat
    subq = session.query(sailors.sid).join(reserves, reserves.sid==sailors.sid).join(boats, boats.bid==reserves.bid).filter(boats.color!='red')

    #Get sailors who reserved a red boat and have not reserved a non red boat
    q = session.query(sailors.sname, sailors.sid).join(reserves, reserves.sid == sailors.sid).join(boats, boats.bid == reserves.bid).filter(boats.color == 'red').filter(~sailors.sid.in_(subq)).distinct().all()

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

# Test queries for part 3

def test_P3_1(): 
    result = connection.execute("select s.sname, b.bid, b.bname from sailors s, boats b, broken br where s.sid = br.sid and b.bid = br.bid;").fetchall()

    q = session.query(sailors.sname, boats.bid, boats.bname).join(broken, broken.sid==sailors.sid).filter(boats.bid==broken.bid).all()

    assert q == result


def test_P3_2(): 
    result = connection.execute("select b.bid, c.cost, c.expected from boats b, costs c where c.bid = b.bid;").fetchall()

    q = session.query(boats.bid, costs.cost, costs.expected).filter(costs.bid == boats.bid).all()

    assert q == result

def test_P3_3(): 
    result = connection.execute("select s.sname, s.sid, b.bid, c.cost from boats b, sailors s, costs c, broken br where b.bid = br.bid and s.sid = br.sid and c.br_id = br.br_id and c.cost>1000;").fetchall()
    
    q = session.query(sailors.sname, sailors.sid, boats.bid, costs.cost).join(broken, boats.bid == broken.bid).filter(costs.cost>1000, broken.bid == boats.bid, sailors.sid == broken.sid, costs.br_id==broken.br_id).all()

    assert q == result

