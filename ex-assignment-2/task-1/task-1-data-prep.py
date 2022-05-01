from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from faker import Faker

Base = declarative_base()
engine = create_engine(
    'postgresql://postgres:postgres@localhost:5432/db_assignment',
    # echo=True,
    pool_pre_ping=True)
session = Session(engine)
fake = Faker()


class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    product_review = Column(String)

    def __repr__(self):
        return f"Customer(id={self.id}, name={self.name}, address={self.address}, product_review={self.product_review})"


Base.metadata.create_all(engine)

for i in range(1000000):
    session.add(
        Customer(name=fake.name(),
                 address=fake.address(),
                 product_review=fake.text()))

    if i % 50 == 0:
        session.commit()
        print(f"Added {i}/1000000 customers")