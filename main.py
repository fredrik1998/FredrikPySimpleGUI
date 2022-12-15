import PySimpleGUI as sg
import contact_information_window
import database_interface
import validation

layout = [[sg.Text("Enter First name:"), sg.Input(key='-FIRSTNAME-', do_not_clear=True, size=(20, 1))],
          [sg.Text("Enter Last name:"), sg.Input(key='-LASTNAME-', do_not_clear=True, size=(10, 1))],
          [sg.Text("Enter Address:"), sg.Input(key='-ADDRESS-', do_not_clear=True, size=(10, 1))],
          [sg.Text("Enter Postnumber:"), sg.Input(key='-POSTNUMBER-', do_not_clear=True, size=(10, 1))],
          [sg.Text("Enter Postaddress:"), sg.Input(key='-POSTADDRESS-', do_not_clear=True, size=(10, 1))],
          [sg.Button('Insert New Member'), sg.Button('Show Membership List'), sg.Exit()],]

window = sg.Window("Membership List", layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Insert New Member':
        validation_result = validation.validate(values)
        if validation_result["is_valid"]:
            database_interface.insert_contact(values['-FIRSTNAME-'], values['-LASTNAME-'], values['-ADDRESS-'], values['-POSTNUMBER-'], values['-POSTADDRESS-'])
            sg.popup("Contact Information submitted!")
        else:
            error_message = validation.generate_error_message(validation_result["values_invalid"])
            sg.popup(error_message)
    elif event == 'Show Membership List':
        contact_information_window.create()
