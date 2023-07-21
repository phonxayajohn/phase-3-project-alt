from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint, ForeignKey

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine("sqlite:///db/beer_inventory.db")

Base = declarative_base()


class Store(Base):
    __tablename__ = "stores"
    __table_args__ = (PrimaryKeyConstraint("id"),)

    id = Column(Integer())
    name = Column(String())

    def __repr__(self):
        return f"Store ID: {self.id}," \
            + f"Store Name: {self.name}"


class Beer(Base):
    __tablename__ = "beers"
    __table_args__ = (PrimaryKeyConstraint("id"),)

    id = Column(Integer())
    name = Column(String())
    brand = Column(String())
    style = Column(String())

    def __repr__(self):
        return f"Name: {self.name}," \
            + f"Brand: {self.brand}," \
            + f"Style: {self.style}"


class Inventory(Base):
    __tablename__ = "inventory"
    __table_args__ = (PrimaryKeyConstraint('id'),)

    id = Column(Integer(), primary_key=True)
    beer_id = Column(Integer, ForeignKey("beers.id"))
    store_id = Column(Integer, ForeignKey("stores.id"))

    beer = relationship('Beer', backref=backref('beers.id'))
    store = relationship('Store', backref=backref('stores.id'))

    def __repr__(self):
        return f"ID: {self.id}," \
            + f"Beer ID: {self.beer_id}," \
            + f"Store ID: {self.store_id}"
