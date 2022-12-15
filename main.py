import PySimpleGUI as sg
import contact_information_window
import database_interface
import validation

layout = [[sg.Button('Show Membership List'), sg.Exit()]]

window = sg.Window("Membership List", layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Show Membership List':
        contact_information_window.create()
