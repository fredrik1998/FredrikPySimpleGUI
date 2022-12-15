class DatabaseInterface:
    def __init__(self):
        # Initialize database connection and cursor
        self.conn = sqlite3.connect('contacts.db')
        self.cursor = self.conn.cursor()

    def get_all_contacts(self):
        # Execute a SELECT query to get all rows from the contacts table
        self.cursor.execute('SELECT * FROM contacts')

        # Return the rows as a list of lists
        return self.cursor.fetchall()

    def insert_contact(self, firstname, lastname, address, postnumber, postaddress):
        # Execute an INSERT query to add a new contact to the database
        self.cursor.execute(
            'INSERT INTO contacts (firstname, lastname, address, postnumber, postaddress) VALUES (?, ?, ?, ?, ?)',
            (firstname, lastname, address, postnumber, postaddress))
        self.conn.commit()


database_interface = DatabaseInterface()

# Use the get_all_contacts() method to get all rows from the contacts table
rows = database_interface.get_all_contacts()

# Use the insert_contact() method to add a new contact to the database
database_interface.insert_contact(values['-FIRSTNAME-'], values['-LASTNAME-'], values['-ADDRESS-'],
                                  values['-POSTNUMBER-'], values['-POSTADDRESS-'])
