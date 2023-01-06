import PySimpleGUI as sg
import membership_window


layout = [[sg.Button('Medlemsregister'), sg.Exit('Avsluta')]]

window = sg.Window("Membership List", layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Avsluta'):
        break
    elif event == 'Medlemsregister':
        membership_window.run()





