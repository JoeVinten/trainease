from services.station_validator import StationValidator


def get_stations_from_user(prompt, validator):
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


def main():
    print("🚂 Welcome to TrainEase!")

    validator = StationValidator()

    origin_stations = get_stations_from_user(
        "Enter origin stations (comma-separated):", validator
    )

    destination_stations = get_stations_from_user(
        "Enter destination stations (comma-separated):", validator
    )

    if origin_stations and destination_stations:
        print("Ready to proceed with finding your journey... CHOO CHOO")


if __name__ == "__main__":
    main()
