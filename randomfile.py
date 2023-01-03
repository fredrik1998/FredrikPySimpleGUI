import PySimpleGUI as sg
import database_interface
from database_interface import delete_contact, update_contact
import validation
from sqlite3 import IntegrityError


class ContactManager:
    def __init__(self):
        self.values = {}
        self.contact_records_array = []
        self.headings = ['MemberID', 'First Name', 'Last Name', 'Address', 'Postnumber', 'Postaddress',
                         'Membership Fee']
        self.contact_information_window_layout = [
            [[sg.Text('Enter search:'), sg.InputText()],
             [sg.Button('Search')]],
            [sg.Button("Reset", key="reset")],
            [sg.Table(values=self.contact_records_array, headings=self.headings, max_col_width=35,
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

        self.contact_information_window = sg.Window("Membership List Menu",
                                                    self.contact_information_window_layout, modal=True)
        self.table = self.contact_information_window['-TABLE-']

    def display_table(self):
        rows = database_interface.get_all_rows()
        self.table.update(rows)

    def delete_row(self,row_index):

        self.contact_records_array.pop(row_index)

        self.table.update(self.contact_records_array)

    @staticmethod
    def search(search_query, contact_records_array):
        results = []
        for row in contact_records_array:
            row = [str(x) for x in row]  # convert all values in row to strings
            print(f'row: {row}')  # print row
            search_query = str(search_query)  # convert search query to string
            if search_query in row:
                results.append(row)
        if not results:
            sg.popup('No records found')
        return results

    def run(self):
        while True:
            event, values = self.contact_information_window.read()
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
                        database_interface.insert_contact(values['-MemberID-'], values['-FIRSTNAME-'],
                                                          values['-LASTNAME-'],
                                                          values['-ADDRESS-'],
                                                          values['-POSTNUMBER-'], values['-POSTADDRESS-'],
                                                          membership_fee)
                    except IntegrityError:
                        sg.popup("A member with that ID already exists")
                    else:
                        sg.popup("Member added")
                        self.display_table()
                else:
                    error_message = validation.generate_error_message(validation_result["values_invalid"])
                    sg.popup(error_message)

            elif event == 'Delete':
                if not values['-TABLE-']:
                    sg.popup('No Row Selected')
                else:
                    memberid = values['-TABLE-'][0]
                    if delete_contact(memberid):
                        self.delete_row(memberid)
                        # Remove the row from the table
                        sg.popup('Contact deleted successfully')
                        self.display_table()
                    else:
                        sg.popup('Error deleting contact')

            elif event == 'Update':
                if not values['-TABLE-']:
                    sg.popup('No Row Selected')
                else:
                    selected_row = self.table.get()
                    if selected_row:
                        memberid = int(selected_row[0][0])
                        firstname = selected_row[0][1]
                        lastname = selected_row[0][2]
                        address = selected_row[0][3]
                        postnumber = selected_row[0][4]
                        postaddress = selected_row[0][5]
                        membershipfee = selected_row[0][6]
                        if update_contact(memberid, firstname, lastname, address, postnumber, postaddress,
                                          membershipfee):
                            sg.popup('Contact updated successfully')
                            self.table.update(self.contact_records_array)
                        else:
                            sg.popup('Error deleting contact')

            elif event == 'Search':
                search_query = values[0]
                print(f'search_query: {search_query}')  # print search_query
                results = self.search(search_query, self.contact_records_array)
                self.table.update(results)

            elif event == 'reset':
                self.display_table()

        self.contact_information_window.close()
