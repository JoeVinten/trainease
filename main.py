from services.format_responses import format_responses
from services.get_departures_data import LiveDepartureData
from services.get_station_inputs import get_station_inputs
from services.station_validator import StationValidator


def main():
    print(
        "🚂 Welcome to TrainEase! Follow the prompts to get live direct train journeys to and from multiple stations."
    )

    validator = StationValidator()

    origin_stations = get_station_inputs(
        "Enter origin stations (comma-separated):", validator
    )

    destination_stations = get_station_inputs(
        "Enter destination stations (comma-separated):", validator
    )

    if origin_stations and destination_stations:
        print("Ready to proceed with finding your journey... CHOO CHOO")

    valid_journeys = []
    for origin_station in origin_stations:
        departure_board = LiveDepartureData(origin_station.code, origin_station.name)

        valid_journeys.extend(
            departure_board.find_trains_to_destinations(destination_stations)
        )

    format_responses(valid_journeys)


if __name__ == "__main__":
    main()
