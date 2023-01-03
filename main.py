import PySimpleGUI as sg
import membership_window
from randomfile import ContactManager

layout = [[sg.Button('Show Membership List'), sg.Exit()]]

window = sg.Window("Membership List", layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Show Membership List':
        membership_window.create()


