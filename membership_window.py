from sqlite3 import IntegrityError
import sqlite3
import PySimpleGUI as sg
import database_interface
import validation


def get_contact_records():
    contact_records = database_interface.retrieve_contacts()
    return contact_records


def create():
    contact_records_array = get_contact_records()
    headings = ['MemberID', 'First Name', 'Last Name', 'Address', 'Postnumber', 'Postaddress', 'Membership Fee']
    contact_information_window_layout = [
        [[sg.Text('Enter search:'), sg.InputText()],
         [sg.Button('Search')]],
        [sg.Button("Reset", key="reset")],
        [sg.Table(values=contact_records_array, headings=headings, max_col_width=35,
                  auto_size_columns=True,
                  justification='right',
                  alternating_row_color='lightblue',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35,
                  tooltip='Reservations Table')],
        [sg.Text("Enter MemberID:"), sg.Input(key='-MemberID-', do_not_clear=True, size=(20, 1))],
        [sg.Text("Enter First name:"), sg.Input(key='-FIRSTNAME-', do_not_clear=True, size=(20, 1))],
        [sg.Text("Enter Last name:"), sg.Input(key='-LASTNAME-', do_not_clear=True, size=(10, 1))],
        [sg.Text("Enter Address:"), sg.Input(key='-ADDRESS-', do_not_clear=True, size=(10, 1))],
        [sg.Text("Enter Postnumber:"), sg.Input(key='-POSTNUMBER-', do_not_clear=True, size=(10, 1))],
        [sg.Text("Enter Postaddress:"),
         sg.Input(key='-POSTADDRESS-', do_not_clear=True, size=(10, 1))],
        [sg.Text("Select an option:")],
        [sg.Radio("Payed", "OPTIONS", default=True, key='-MEMBERSHIP-', enable_events=True),
         sg.Radio("Not Payed", "OPTIONS", key='-MEMBERSHIP-', enable_events=True)],
        [sg.Button('Insert New Member')],
        [sg.Button('Delete')],
        [sg.Button('Exit')],
        [sg.Button('Update')]

    ]

    contact_information_window = sg.Window("Membership List Menu",
                                           contact_information_window_layout, modal=True)
    table = contact_information_window['-TABLE-']

    def delete_row(row_index):

        contact_records_array.pop(row_index)

        table.update(contact_records_array)

    def update_row(row_index, new_values):
        contact_records_array[row_index] = new_values
        table.update(contact_records_array)

    def display_table():
        rows = database_interface.get_all_rows()
        table.update(rows)

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

    while True:
        event, values = contact_information_window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        elif event == 'Insert New Member':
            validation_result = validation.validate(values)
            if validation_result["is_valid"]:
                if values['-MEMBERSHIP-'] == 1:
                    membership_fee = "Payed"
                else:
                    membership_fee = "Not Payed"
                try:
                    database_interface.insert_contact(values['-MemberID-'], values['-FIRSTNAME-'], values['-LASTNAME-'],
                                                      values['-ADDRESS-'],
                                                      values['-POSTNUMBER-'], values['-POSTADDRESS-'],
                                                      membership_fee)
                except IntegrityError:
                    sg.popup("A member with that ID already exists")
                else:
                    sg.popup("Member added")
                    display_table()
            else:
                error_message = validation.generate_error_message(validation_result["values_invalid"])
                sg.popup(error_message)

        elif event == 'Delete':
            if not values['-TABLE-']:
                sg.popup('No Row Selected')
            else:
                if sg.popup_ok_cancel('Can not undo Delete: Continue?') == 'OK':
                    delete_row(values['-TABLE-'][0])

        elif event == 'Update':
            if not values['-TABLE-']:
                sg.popup('No Row Selected')
            else:
                validation_result = validation.validate(values)
                if validation_result["is_valid"]:
                    if values['-MEMBERSHIP-'] == 1:
                        membership_fee = "Payed"
                    else:
                        membership_fee = "Not Payed"
                    try:
                        row_index = values['-TABLE-'][0]
                        new_values = [values['-MemberID-'], values['-FIRSTNAME-'], values['-LASTNAME-'],
                                      values['-ADDRESS-'],
                                      values['-POSTNUMBER-'],
                                      values['-POSTADDRESS-'],
                                      membership_fee]
                        update_row(row_index, new_values)
                    except IntegrityError:
                        sg.popup("A member with that ID already exists")
                    else:
                        sg.popup('Updated row')

                else:
                    error_message = validation.generate_error_message(validation_result["values_invalid"])
                    sg.popup(error_message)

        if event == 'Search':
            search_query = values[0]
            results = search(search_query, contact_records_array)
            table.update(results)

        elif event == 'reset':
            display_table()

    contact_information_window.close()
