import PySimpleGUI as sg
import database_interface

#Search function that allows user to search based of memberid
def search(search_query, member_records, table):
    results = []
    for row in member_records:
        search_query = str(search_query)  # convert search query to string
        if search_query in str(row[0]):  # check if search query is a substring of member id
            results.append(row)
            break  # exit the loop once a match has been found
    if not results:
        # If search query is a member object, add it to the results
        if isinstance(search_query, database_interface.Membership):
            results.append(
                [search_query.memberid, search_query.firstname, search_query.lastname, search_query.address,
                 search_query.postnumber, search_query.postaddress, search_query.membershipfee])
        else:
            sg.popup('Ingen medlem hittad')
    table.update(results)  # update table with search results
    return results
