import PySimpleGUI as sg
import database_interface


def get_contact_records():
    contact_records = database_interface.retrieve_contacts()
    return contact_records


def create():
    contact_records_array = get_contact_records()
    headings = ['MemberID', 'First Name', 'Last Name', 'Address', 'Postnumber', 'Postaddress']
    contact_information_window_layout = [
        [sg.Table(values=contact_records_array, headings=headings, max_col_width=35,
                  auto_size_columns=True,
                  justification='right',
                  alternating_row_color='lightblue',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35,
                  tooltip='Reservations Table')],
        [sg.Button('Delete')],
        [sg.Button('Exit')], [[sg.Text('Enter search query:'), sg.InputText()],
          [sg.Button('Search')]]
    ]

    contact_information_window = sg.Window("Membership List Menu",
                                           contact_information_window_layout, modal=True)
    table = contact_information_window['-TABLE-']

    while True:
        event, values = contact_information_window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

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

    contact_information_window.close()
