from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Membership(Base):
    __tablename__ = 'CONTACT_INFORMATION'
    memberid = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    address = Column(String)
    postnumber = Column(String)
    postaddress = Column(String)
    membershipfee = Column(Integer)

    def __init__(self, memberid, firstname, lastname, address, postnumber, postaddress, membershipfee):
        super().__init__()
        self.memberid = memberid
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.postnumber = postnumber
        self.postaddress = postaddress
        self.membershipfee = membershipfee


engine = create_engine('sqlite:///contact_information.db')

Base.metadata.create_all(engine)
