from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from faker import Faker
import random

Base = declarative_base()
engine = create_engine(
    'postgresql://postgres:postgres@localhost:5432/db_assignment',
    echo=True,
    pool_pre_ping=True)
session = Session(engine)
fake = Faker()


class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    product_review = Column(String)
    purchases = relationship("Purchase",
                             back_populates="customer",
                             cascade="all, delete-orphan")

    def __repr__(self):
        return f"Customer(id={self.id}, name={self.name}, address={self.address}, product_review={self.product_review})"


class Purchase(Base):
    __tablename__ = "purchase"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    customer = relationship("Customer", back_populates="purchases")
    purchases_products_list = relationship("Purchases_products_list",
                                           back_populates="purchase",
                                           cascade="all, delete-orphan")

    def __repr__(self):
        return f"Purchase(id={self.id}, customer_id={self.customer_id})"


class Purchases_products_list(Base):
    __tablename__ = "purchases_products_list"
    id = Column(Integer, primary_key=True)

    purchase_id = Column(Integer, ForeignKey("purchase.id"), nullable=False)
    purchase = relationship("Purchase",
                            back_populates="purchases_products_list")

    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product = relationship("Product", back_populates="purchases_products_list")

    def __repr__(self):
        return f"Purchases_products_list(id={self.id}, id={self.purchase_id}, id={self.product_id})"


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    details = Column(String)
    price = Column(Float)
    type = Column(String)

    purchases_products_list = relationship("Purchases_products_list",
                                           back_populates="product",
                                           cascade="all, delete-orphan")

    def __repr__(self):
        return f"Product(id={self.id}, name={self.name}, details={self.details}, price={self.price}, type={self.type})"


class Sale(Base):
    __tablename__ = "sale"
    id = Column(Integer, primary_key=True)
    type = 
    discount = Column(Float)

    def __repr__(self):
        return f"Sale(id={self.id}, type={self.type}, discount={self.discount})"


Base.metadata.create_all(engine)

for i in range(1000):
    session.add(
        Product(name=fake.name(),
                details=fake.text(),
                price=random.randint(1, 1000),
                type=["a", "b", "c", "d", "e"][random.randint(0, 4)]))

    session.add(Purchase(customer_id=random.randint(1, 1000000)))

    session.add(
        Purchases_products_list(purchase_id=random.randint(1, 1000),
                                product_id=random.randint(1, 1000)))

    if i % 50 == 0:
        session.commit()
        print(f"Added {i}/1000")

session.add(Sale(type="a", discount=1))
session.add(Sale(type="b", discount=2))
session.add(Sale(type="c", discount=3))
session.add(Sale(type="d", discount=4))
session.add(Sale(type="e", discount=5))
session.commit()
