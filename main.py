import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import faker, random

engine = create_engine("postgresql+psycopg2://postgres:96560517bd@localhost/baza")

Base = declarative_base()

fake = faker.Faker("ru_RU")

class Users(Base):
    __tablename__ = 'users'
    ID = Column(Integer, primary_key=True, nullable=False)
    Name = Column(String(250), nullable=False)
    Hp = Column(Integer, default=100)
    Dmg = Column(Integer, default=20)

class Cats(Base):
    __tablename__ = "cats"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(250))
    color = Column(String(250))
    Base.metadata.create_all(engine)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
s = Session()

# for i in range(400):
#     a = random.randrange(1000, 9999)
#     imya = fake.first_name()
#     usr = Users(ID=a, Name=imya)
#     s.merge(usr)
#     s.commit()
#
# data = s.query(Users).all()
# print(data)
# for n in data:
#     print(n.Name)
#
# data = s.query(Users).filter(Users.Name.endswith('в'))
# for m in data:
#     print(m.ID, m.Name)

data = s.query(Users).filter(Users.ID > 1500)
for m in data:
    print(m.ID, m.Name)
# print(data)

s.query(Users).filter(Users.ID == 1000).update({'Name': 'Ненонна'})
us = Users(ID=1002, Name = 'Некифор')
s.add(us)
s.commit()