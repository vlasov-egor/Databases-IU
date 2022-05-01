from textwrap import fill
from types import NoneType
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from faker import Faker
import random

Base = declarative_base()
engine = create_engine(
    'postgresql://postgres:postgres@localhost:5432/db_assignment',
    # echo=True,
    pool_pre_ping=True)
session = Session(engine)
fake = Faker()


class Mac(Base):
    __tablename__ = "mac"
    id = Column(Integer, primary_key=True)
    mac_add = Column(String)
    ip = Column(String)
    country = Column(String)
    date = Column(Date)

    def __repr__(self):
        return f"Mac(id={self.id}, mac_add={self.mac_add}, ip={self.ip}, country={self.country}, date={self.date})"


def fill_db():
    for i in range(10000):
        session.add(
            Mac(mac_add="02:00:00:%02x:%02x:%02x" % (random.randint(
                0, 255), random.randint(0, 255), random.randint(0, 255)),
                ip=
                f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
                country=["Russia", "Germany", "Ukraine", "Egypt",
                         "France"][random.randint(0, 4)],
                date=fake.date_between(start_date='today', end_date='+30y')))

        if i % 50 == 0:
            session.commit()
            print(f"Added {i}/10000")


def get_next_available_id() -> int:
    return session.query(func.max(Mac.id)).one()[0] + 1 if session.query(
        func.max(Mac.id)).one() else "Empty db"


def ip_transform(ip: str) -> str:
    return ".".join(map(str,
                        ["{0:08b}".format(int(x)) for x in ip.split(".")]))


def ip_transform_for_certain_country(country: str) -> str:
    entities = session.query(Mac).filter(Mac.country == country).all()

    if entities:
        for index, entity in enumerate(entities):
            print(index)
            entity.ip = ip_transform(entity.ip)
            
            if index % 50 == 0:
                session.commit()
            
        return "Completed"

    else:
        return "There are no such country"


Base.metadata.create_all(engine)
fill_db()
print(get_next_available_id())
print(ip_transform_for_certain_country("Germany"))