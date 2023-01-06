import PySimpleGUI as sg
import database_interface
import validation
import search


def get_member_records():
    member_records = database_interface.retrieve_member()
    return member_records


def run():
    member_records = get_member_records()
    headings = ['Medlemsnummer', 'Förnamn', 'Efternamn', 'Adress', 'Postnumber', 'Postadress', 'Medlemskapsavgift']
    membership_list_layout = [
        [[sg.Text('Sök:'), sg.InputText()],
         [sg.Button('Sök')]],
        [sg.Button("Återställa", key="reset")],
        [sg.Table(values=member_records, headings=headings, max_col_width=35,
                  auto_size_columns=True,
                  justification='right',
                  alternating_row_color='lightblue',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35,
                  tooltip='Reservations Table')],
        [sg.Text("Medlemsnummer:"), sg.Input(key='-MemberID-', size=(20, 1))],
        [sg.Text("Förnamn:"), sg.Input(key='-FIRSTNAME-', size=(20, 1))],
        [sg.Text("Efternamn:"), sg.Input(key='-LASTNAME-', size=(10, 1))],
        [sg.Text("Adress:"), sg.Input(key='-ADDRESS-', size=(10, 1))],
        [sg.Text("Postnummer:"), sg.Input(key='-POSTNUMBER-', size=(10, 1))],
        [sg.Text("Postadress:"),
         sg.Input(key='-POSTADDRESS-', size=(10, 1))],
        [sg.Text("Medlemsavgift:")],
        [sg.Radio("Betald", "OPTIONS", default=True, key='-MEMBERSHIP-', enable_events=True),
         sg.Radio("Inte Betald", "OPTIONS", key='-MEMBERSHIP-', enable_events=True)],
        [sg.Button('Lägg till Ny Medlem')],
        [sg.Button('Ta bort medlem')],
        [sg.Button('Tillbaka')],
        [sg.Button('Uppdatera medlem')]

    ]

    membership_list_window = sg.Window("Membership List Menu",
                                       membership_list_layout, modal=True)
    table = membership_list_window['-TABLE-']

    def delete_row(row_index):

        member_records.pop(row_index)

        table.update(member_records)

    def update_row(row_index, new_values):
        member_records[row_index] = new_values
        table.update(member_records)

    def display_table():
        rows = database_interface.get_all_rows()
        table.update(rows)

    while True:
        event, values = membership_list_window.read()
        if event == "Tillbaka" or event == sg.WIN_CLOSED:
            break

        # Add member to database and update table with current members
        elif event == 'Lägg till Ny Medlem':
            validation_result = validation.validate(values)
            if validation_result["is_valid"]:
                if values['-MEMBERSHIP-'] == 1:
                    membership_fee = "Betald"
                else:
                    membership_fee = "Inte Betald"
                # Call the modified insert_member function
                insert_result = database_interface.insert_member(values['-MemberID-'], values['-FIRSTNAME-'],
                                                                 values['-LASTNAME-'],
                                                                 values['-ADDRESS-'],
                                                                 values['-POSTNUMBER-'], values['-POSTADDRESS-'],
                                                                 membership_fee, member_records)
                if insert_result is None:
                    # If the insert_member function returned None, a member with the same ID already exists
                    sg.popup("En medlem med det ID finns redan")
                else:
                    sg.popup("Medlem inlagd i registret")
                    display_table()
            else:
                error_message = validation.generate_error_message(validation_result["values_invalid"])
                sg.popup(error_message)

        # Delete member from database and update table with current members
        elif event == 'Ta bort medlem':
            if not values['-TABLE-']:
                sg.popup('Ingen rad vald')
            else:
                if sg.popup_ok_cancel('Vill du ta bort medlem?:') == 'OK':
                    row_index = values['-TABLE-'][0]
                    selected_row = member_records[row_index]
                    memberid = selected_row[0]
                    delete_row(row_index)
                    database_interface.delete_member(memberid)
                    display_table()

        # Updates database and update table with updates values
        elif event == 'Uppdatera medlem':
            if not values['-TABLE-']:
                sg.popup('Ingen rad vald')
            else:
                validation_result = validation.validate(values)
                if validation_result["is_valid"]:
                    if values['-MEMBERSHIP-'] == 1:
                        membership_fee = "Betald"
                    else:
                        membership_fee = "Inte Betald"
                    row_index = values['-TABLE-'][0]
                    new_values = [values['-MemberID-'], values['-FIRSTNAME-'], values['-LASTNAME-'],
                                  values['-ADDRESS-'],
                                  values['-POSTNUMBER-'],
                                  values['-POSTNUMBER-'],
                                  membership_fee]
                    update_row(row_index, new_values)
                    # Call the modified update_member function
                    update_result = database_interface.update_member(memberid=values['-MemberID-'],
                                                                     firstname=values['-FIRSTNAME-'],
                                                                     lastname=values['-LASTNAME-'],
                                                                     address=values['-ADDRESS-'],
                                                                     postnumber=values['-POSTNUMBER-'],
                                                                     postaddress=values['-POSTADDRESS-'],
                                                                     membershipfee=membership_fee)
                    if update_result is None:
                        # If the update_member function returned None, a member with the same ID already exists
                        sg.popup("A member with that ID already exists")
                    else:
                        sg.popup('Uppdaterad')
                        display_table()
                else:
                    error_message = validation.generate_error_message(validation_result["values_invalid"])
                    sg.popup(error_message)

        if event == "Sök":
            # Search database and update table with results
            search_query = values[0]
            table = membership_list_window['-TABLE-']
            search.search(search_query, member_records, table)
            print("Search query:", search_query)
            print("Member records:", member_records)

        elif event == 'reset':
            display_table()

    membership_list_window.close()
