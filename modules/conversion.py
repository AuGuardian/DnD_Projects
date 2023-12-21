def data_to_json(data):

    # Initialize an empty list to hold the formatted data
    formatted_data = []

    # Iterate through each entry in 'data' and create a dictionary for each entry
    for entry in data:
        name, initiative, dex, health, status = entry
        formatted_entry = {
            "name": name,
            "initiative": initiative,
            "dex": dex,
            "health": health,
            "status": status
        }
        formatted_data.append(formatted_entry)

    return formatted_data
