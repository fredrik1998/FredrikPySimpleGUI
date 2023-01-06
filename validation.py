
def validate(values):
    is_valid = True
    values_invalid = []

    # Validates values so they cannot be empty
    if len(values['-MemberID-']) == 0:
        values_invalid.append('Medlems id måste fyllas i')
        is_valid = False

    if len(values['-FIRSTNAME-']) == 0:
        values_invalid.append('Förnamn måste fyllas i')
        is_valid = False

    if len(values['-LASTNAME-']) == 0:
        values_invalid.append('Efternamn måste fyllas i')
        is_valid = False

    if len(values['-ADDRESS-']) == 0:
        values_invalid.append('Address måste fyllas i')
        is_valid = False

    if len(values['-POSTNUMBER-']) == 0:
        values_invalid.append('Postnummer måste fyllas i')
        is_valid = False

    if len(values['-POSTADDRESS-']) == 0:
        values_invalid.append('Postaddress måste fyllas i')
        is_valid = False

    result = {"is_valid": is_valid, "values_invalid": values_invalid}
    return result


# Generates error message if any field is empty
def generate_error_message(values_invalid):
    error_message = ''
    for value_invalid in values_invalid:
        error_message += ('\n' + '' + value_invalid)

    return error_message
