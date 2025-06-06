import requests
import os
import json
from dotenv import load_dotenv


class LiveDepartureData:
    def __init__(self, station_code, station_name):
        self.station_code = station_code
        self.station_name = station_name
        load_dotenv()

    def get_departures_data(self, dest_code):
        time_window = 30
        req_url = f"https://api1.raildata.org.uk/1010-live-departure-board-dep1_2/LDBWS/api/20220120/GetDepBoardWithDetails/{self.station_code}?timeWindow={time_window}&filterCrs={dest_code}"
        api_key = os.getenv("LIVE_DEPARTURES_API_KEY")

        if not api_key:
            raise RuntimeError(
                "LIVE_DEPARTURES_API_KEY environment variable is missing"
            )

        headers = {
            "User-Agent": "trainease/1.0",
            "x-apikey": api_key,
        }

        try:
            response = requests.get(req_url, headers=headers, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            print(f"Raw response: {response.text}")
            return None

    def find_trains_to_destinations(self, dest_stations):
        matching_trains = {}

        for dest_station in dest_stations:
            dest_code = dest_station.code
            dest_name = dest_station.name
            print(f"🔍 Searching for trains from {self.station_name} to {dest_name}...")

            dept_data = self.get_departures_data(dest_code)

            if dept_data is None:
                print(f"❌ Failed to get data for {dest_code}")
                matching_trains[dest_code] = []
                continue

            if not dept_data.get("areServicesAvailable", True):
                print(f"❌ No trains available from {dest_code}")
                matching_trains[dest_code] = []
                continue

            train_services = dept_data.get("trainServices", [])
            destination_trains = []

            for service in train_services:
                dest_info = None

                calling_points = service.get("subsequentCallingPoints", [])
                for calling_point_group in calling_points:
                    calling_points_list = calling_point_group.get("callingPoint", [])
                    for calling_point in calling_points_list:
                        if calling_point.get("crs") == dest_code:
                            dest_info = calling_point
                            break
                    if dest_info:
                        break

                if dest_info is None:
                    continue

                arrival = (
                    dest_info.get("et")
                    if dest_info.get("et") != "On time"
                    else dest_info.get("st")
                )

                journey_info = {
                    "departure_station_code": self.station_code,
                    "departure_station_name": self.station_name,
                    "destination_location_name": dest_info.get("locationName"),
                    "scheduled_departure": service.get("std"),
                    "estimated_departure": service.get("etd"),
                    "arrival": arrival,
                    "platform": service.get("platform"),
                    "is_cancelled": service.get("isCancelled"),
                }

                destination_trains.append(journey_info)

            matching_trains[dest_code] = destination_trains
            print(f"✅ Found {len(destination_trains)} trains to {dest_code}")

        return matching_trains
