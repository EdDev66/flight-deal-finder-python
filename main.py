#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch

ORIGIN_CITY_IATA = 'LON'

data_manager = DataManager()
flight_search = FlightSearch()


sheet_data = data_manager.fetch_data()


for item in sheet_data:
    if item['iataCode'] != '':
        flight_search.search_flight(ORIGIN_CITY_IATA, item['iataCode'], item['lowestPrice'])
    else:
        iata_code = flight_search.get_code(item['city'])
        item['iataCode'] = iata_code
        data_manager.update_data(item['id'], iata_code)
