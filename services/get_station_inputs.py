def get_station_inputs(prompt, validator):
    """Get and validate inputs from the user"""

    print(prompt)

    stations = input()

    valid_stations = []
    for station in stations.split(","):
        valid_station = validator.find_matching_stations(station_input=station)
        if valid_station:
            valid_stations.append(valid_station)

    if len(valid_stations) < 1:
        print("❌ No valid stations found")

    return valid_stations
