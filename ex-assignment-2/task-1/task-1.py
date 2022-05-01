from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

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

query_1 = session.query(Customer).filter(Customer.id == 1).one()
query_2 = session.query(Customer).filter(Customer.name.startswith("C")).all()
query_3 = session.query(Customer).filter(
    Customer.address == "2772 Daniel Junction Zacharyberg, IL 19814").all()
query_4 = session.query(Customer).filter(
    func.length(Customer.product_review) > 200).all()

print(f"query_1:\n{query_1}", '\n')
print(f"query_2:\n{query_2}", '\n')
print(f"query_3:\n{query_3}", '\n')
print(f"query_4:\n{query_4}", '\n')
