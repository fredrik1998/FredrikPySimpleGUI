import sqlite3

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()
# engine = create_engine('sqlite:///contact_information.db', echo=True)


conn = sqlite3.connect('contact_information.db')
query = (''' CREATE TABLE CONTACT_INFORMATION
            (MemberID INTEGER PRIMARY KEY AUTOINCREMENT,
            FIRSTNAME          TEXT    NOT NULL,
            LASTNAME       TEXT NOT NULL,
            ADDRESS    CHAR(50),
            POSTNUMBER INT,
            POSTADDRESS CHAR(50)
            );''')
conn.execute(query)
conn.close()

# class Membership(Base):
#     __tablename__ = 'membership'
#     memberid = Column(Integer, primary_key=True)
#     firstname = Column(String)
#     lastname = Column(String)
#     address = Column(String)
#     postnumber = Column(Integer)
#     postaddress = Column(String)
#
#
# Base.metadata.create_all(engine)
