import PySimpleGUI as sg

# Create the search input
search_input = sg.Text()

# Create the search results Listbox
search_results = sg.Listbox(values=[], size=(30, 6))

# Create the layout
layout = [[sg.Text('Search:')],
          [search_input],
          [search_results],
          [sg.Button('Search')]]

# Create the window
window = sg.Window('Search Bar').Layout(layout)

# Event loop
while True:
    event, values = window.Read()

    # If the user clicks the search button
    if event == 'Search':
        search_term = values[0]

        # Search for items matching the search term
        search_results_items = []
        for item in search_results_items:
            if search_term in item:
                search_results_items.append(item)

        # Update the search results Listbox with the new items
        window.FindElement('search_results').Update(search_results_items)

    # If the window is closed, break out of the loop
    if event is None:
        break

# Clean up
