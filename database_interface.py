import sqlite3
from sqlalchemy.orm import sessionmaker
from Table import engine
from Table import Membership

SessionFactory = sessionmaker(bind=engine)
session = SessionFactory()


def insert_contact(memberid, firstname, lastname, address, postnumber, postaddress, membershipfee):
    contact = Membership(memberid=memberid, firstname=firstname, lastname=lastname, address=address,
                         postnumber=postnumber,
                         postaddress=postaddress, membershipfee=membershipfee)
    session.add(contact)
    session.commit()


def delete_contact(memberid):
    contact = session.query(Membership).filter_by(memberid=memberid).first()
    if contact:
        session.delete(contact)
        session.commit()
        return True
    return False


def get_all_rows():
    with sqlite3.connect('contact_information.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CONTACT_INFORMATION")
        rows = cursor.fetchall()
    return rows


def update_contact(memberid, firstname, lastname, address, postnumber, postaddress, membershipfee):
    contact = session.query(Membership).filter_by(memberid=memberid).first()
    if contact:
        contact.firstname = firstname
        contact.lastname = lastname
        contact.address = address
        contact.postnumber = postnumber
        contact.postaddress = postaddress
        contact.membershipfee = membershipfee
        session.commit()
        return True
    return False


def edit_phone_number_by_name(name, phone_number):
    conn = sqlite3.connect('contact_information.db')
    conn.execute("UPDATE CONTACT_INFORMATION set ADDRESS = ? where NAME = ?", (name, phone_number))
    conn.close()


def retrieve_contacts():
    results = []
    membership = session.query(Membership).all()
    for member in membership:
        results.append(
            [member.memberid, member.firstname, member.lastname, member.address, member.postnumber, member.postaddress,
             member.membershipfee])
    return results
