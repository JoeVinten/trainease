import csv
from thefuzz import fuzz

from models.train_station import TrainStation


class StationValidator:
    def __init__(self):
        self.stations = self._load_all_stations()

    def _load_all_stations(self):
        stations = []
        try:
            with open(
                "./data/UK_Railway_Stations.csv", mode="r", newline="", encoding="utf-8"
            ) as f:
                reader = csv.reader(f)
                header = next(reader, None)

                for row in reader:
                    if not row:
                        continue

                    try:
                        stations.append(TrainStation(name=row[0], code=row[-2]))
                    except IndexError:
                        print(f"Skipping due to malformed row: {row}")
                        continue

            print(f"✅ Loaded {len(stations)} stations")

            return stations

        except FileNotFoundError:
            raise FileNotFoundError(
                "❌ Error: The file 'UK_Railway_Stations.csv' was not found."
            )
        except Exception as e:
            raise Exception(f"❌ Error: An error occurred while reading the CSV: {e}")

    def find_matching_stations(self, station_input):
        clean_user_input = station_input.strip().lower()
        matches = []
        for station in self.stations:
            clean_station_name = station.name.strip().lower()

            if clean_station_name == clean_user_input:
                matches.append(station)
                continue

            score = fuzz.partial_ratio(clean_station_name, clean_user_input)

            if score > 90:
                matches.append(station)

        if len(matches) == 1:
            selected_station = matches[0]
            print(
                f"✅ Station found: {selected_station.name} ({selected_station.code})"
            )
            return selected_station

        if len(matches) < 1:
            print(f"❌ No matches found for {station_input}")
            # TODO: should add some sort of retry function to just be able to reenter the one that doesn't work
            return None

        if len(matches) > 1:
            return self.handle_multiple_matches(station_input, matches)

    def handle_multiple_matches(self, station_input, matches):
        print(
            f"\nMultiple potential matches found for '{station_input}'. Please choose one:"
        )

        for i, train_station_obj in enumerate(matches):
            print(f" {i + 1}. {train_station_obj.name} ({train_station_obj.code})")

        while True:
            try:
                choice_str = input(f"Enter number (1-{len(matches)}): ")
                choice_num = int(choice_str)
                if 1 <= choice_num <= len(matches):
                    return matches[choice_num - 1]
                else:
                    print("Invalid input. Please enter a number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                print("\nSelection cancelled.")
                return None
