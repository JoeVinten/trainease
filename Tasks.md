## Flow

- User provides a list of origin stations
  - We validate these station names, first directly
  - if a station name is ambagious we give the option
  - We then fuzzy search if we've not found the exact match 
- User provides a list of destination stations
  - We validate these station names, first directly
  - if a station name is ambagious we give the option
  - We then fuzzy search if we've not found the exact match 
- Application finds all the valid combinations of journeys between these origin and destination stations
  - We use RDM APIs to get the journeys between these stations
- Application displays these with live train times


## Features to add
- Search by code
- Nearby stations
