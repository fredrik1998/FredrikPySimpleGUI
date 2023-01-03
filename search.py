import PySimpleGUI as sg


def search(search_query, contact_records_array):
    results = []
    for row in contact_records_array:
        row = [str(x) for x in row]  # convert all values in row to strings
        search_query = str(search_query)  # convert search query to string
        if search_query in row:
            results.append(row)
    if not results:
        sg.popup('No records found')
    return results
