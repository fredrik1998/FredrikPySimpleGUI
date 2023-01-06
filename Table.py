from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Membership(Base):
    __tablename__ = 'Membership'
    memberid = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    address = Column(String)
    postnumber = Column(String)
    postaddress = Column(String)
    membershipfee = Column(Integer)


engine = create_engine('sqlite:///Membership.db')

Base.metadata.create_all(engine)
