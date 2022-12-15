import PySimpleGUI as sg
import database_interface
import validation


def get_contact_records():
    contact_records = database_interface.retrieve_contacts()
    return contact_records

def display_table_rows(rows):
    pass


def create():
    contact_records_array = get_contact_records()
    headings = ['MemberID', 'First Name', 'Last Name', 'Address', 'Postnumber', 'Postaddress']
    contact_information_window_layout = [
        [[sg.Text('Enter search query:'), sg.InputText()],
         [sg.Button('Search')]],
        [sg.Button("Reset", key="reset")],
        [sg.Table(values=contact_records_array, headings=headings, max_col_width=35,
                  auto_size_columns=True,
                  justification='right',
                  alternating_row_color='lightblue',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35,
                  tooltip='Reservations Table')]
        , [sg.Text("Enter First name:"), sg.Input(key='-FIRSTNAME-', do_not_clear=True, size=(20, 1))],
        [sg.Text("Enter Last name:"), sg.Input(key='-LASTNAME-', do_not_clear=True, size=(10, 1))],
        [sg.Text("Enter Address:"), sg.Input(key='-ADDRESS-', do_not_clear=True, size=(10, 1))],
        [sg.Text("Enter Postnumber:"), sg.Input(key='-POSTNUMBER-', do_not_clear=True, size=(10, 1))],
        [sg.Text("Enter Postaddress:"), sg.Input(key='-POSTADDRESS-', do_not_clear=True, size=(10, 1))],
        [sg.Button('Delete')],
        [sg.Button('Exit')],
        [sg.Button('Insert New Member')],

    ]

    contact_information_window = sg.Window("Membership List Menu",
                                           contact_information_window_layout, modal=True)
    table = contact_information_window['-TABLE-']

    while True:
        event, values = contact_information_window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        elif event == 'Insert New Member':
            validation_result = validation.validate(values)
            if validation_result["is_valid"]:
                database_interface.insert_contact(values['-FIRSTNAME-'], values['-LASTNAME-'], values['-ADDRESS-'],
                                                  values['-POSTNUMBER-'], values['-POSTADDRESS-'])
                sg.popup("Contact Information submitted!")
                table.update(values=contact_records_array)
            else:
                error_message = validation.generate_error_message(validation_result["values_invalid"])
                sg.popup(error_message)

        elif event == 'Delete':
            if not values['-TABLE-']:
                sg.popup('No Row Selected')
            else:
                if sg.popup_ok_cancel('Can not undo Delete: Continue?') == 'OK':
                    indexes = values['-TABLE-']
                    if indexes:
                        for index in indexes:
                            print([index])
                        for index in sorted(indexes, reverse=True):
                            del contact_records_array[index]
                            table.update(contact_records_array)

        elif event == 'Search':
            search_query = values[0]
            results = []

            for row in contact_records_array:
                if search_query in row:
                    results.append(row)
                    print(results)
                    table.update(results)

        elif event == 'reset':
            table.update(contact_records_array)

    contact_information_window.close()
