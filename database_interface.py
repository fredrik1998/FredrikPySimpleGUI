import sqlite3
from sqlalchemy.orm import sessionmaker
from Table import engine
from Table import Membership

SessionFactory = sessionmaker(bind=engine)
session = SessionFactory()


def insert_member(memberid, firstname, lastname, address, postnumber, postaddress, membershipfee, member_records):
    try:
        member = Membership(memberid=memberid, firstname=firstname, lastname=lastname, address=address,
                            postnumber=postnumber,
                            postaddress=postaddress, membershipfee=membershipfee)
        session.add(member)
        session.commit()
        member_records.append(
            [member.memberid, member.firstname, member.lastname, member.address, member.postnumber, member.postaddress,
             member.membershipfee])
    except Exception as e:
        print(e)
        return None
    finally:
        # Remove the return None statement from the finally block
        session.rollback()
        session.close()
    return member  # Return the member object after the insert has been committed successfully


def delete_member(memberid):
    try:
        member = session.query(Membership).filter(Membership.memberid == memberid).one()
        session.delete(member)
        session.commit()
    except Exception as e:
        print(e)
    finally:
        session.rollback()
        session.close()


def get_all_rows():
    with sqlite3.connect('Membership.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Membership")
        rows = cursor.fetchall()
    return rows


def update_member(memberid, firstname, lastname, address, postnumber, postaddress, membershipfee):
    # Initialize the member variable with a default value of None
    member = None
    try:
        # Assign the member variable the value returned by the query
        member = session.query(Membership).filter(Membership.memberid == memberid).one()
        # Check if there is already a member with the new memberid value
        existing_member = session.query(Membership).filter(Membership.memberid == memberid).one_or_none()
        if existing_member is not None and existing_member.id != member.id:
            # If there is already a member with the new memberid value, return None
            return None
        # Update the member values
        member.firstname = firstname
        member.lastname = lastname
        member.address = address
        member.postnumber = postnumber
        member.postaddress = postaddress
        member.membershipfee = membershipfee

        session.commit()
    except Exception as e:
        print(e)
    finally:
        session.rollback()
        session.close()
    return member



def retrieve_member():
    results = []
    membership = session.query(Membership).all()
    for member in membership:
        results.append(
            [member.memberid, member.firstname, member.lastname, member.address, member.postnumber, member.postaddress,
             member.membershipfee])
    return results
