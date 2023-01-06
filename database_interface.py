import sqlite3
from sqlalchemy.orm import sessionmaker
from Table import engine
from Table import Membership
import PySimpleGUI as sg
from sqlalchemy import func

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


def generate_new_member_id():
    # Retrieve the current maximum member ID from the database
    current_max_id = session.query(func.max(Membership.memberid)).scalar()
    if current_max_id is None:
        # If no members exist in the database, start the counter at 1
        new_id = 1
    else:
        # Increment the current maximum member ID by 1 to get the new ID
        new_id = current_max_id + 1
    return new_id


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
    try:
        # check if the memberid being updated is the same as the original memberid
        original_member = session.query(Membership).filter(Membership.memberid == memberid).one()
        if original_member.memberid != memberid:
            raise ValueError("Cannot update MemberID")

        # update all fields except memberid
        original_member.firstname = firstname
        original_member.lastname = lastname
        original_member.address = address
        original_member.postnumber = postnumber
        original_member.postaddress = postaddress
        original_member.membershipfee = membershipfee

        session.commit()
    except Exception as e:
        print(e)
        sg.popup(str(e))  # display the error message
    finally:
        session.rollback()
        session.close()


def retrieve_member():
    results = []
    membership = session.query(Membership).all()
    for member in membership:
        results.append(
            [member.memberid, member.firstname, member.lastname, member.address, member.postnumber, member.postaddress,
             member.membershipfee])
    return results
