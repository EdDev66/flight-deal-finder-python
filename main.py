#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = 'LON'

data_manager = DataManager()
flight_search = FlightSearch()


sheet_data = data_manager.fetch_data()
notification_manager = NotificationManager()


for item in sheet_data:
    if item['iataCode'] != '':
        flight = flight_search.search_flight(ORIGIN_CITY_IATA, item['iataCode'], item['lowestPrice'])

        message_string = (
                    f'Low price alert! Only £{flight.price} to fly '
                    f'from {flight.origin_city}-{flight.origin_airport} '
                    f'to {flight.destination_city}-{flight.destination_airport},'
                    f'from {flight.out_date} to {flight.return_date}'
                    )

        if flight.price < item['lowestPrice']:
            if flight.stop_overs[0] > 0:
                message_string += f'\nFlight has {flight.stop_overs} stop overs, via {flight.via_city}'
        
            notification_manager.send_message(message_string)

    if flight is None:
        continue
    else:
        iata_code = flight_search.get_code(item['city'])
        item['iataCode'] = iata_code
        data_manager.update_data(item['id'], iata_code)
