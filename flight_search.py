import requests
from flight_data import FlightData
from notification_manager import NotificationManager
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dotenv import dotenv_values

config = dotenv_values('.env')
notification_manager = NotificationManager()

API_KEY = config['API_KEY']
SEARCH_ENDPOINT = config['SEARCH_ENDPOINT']


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.endpoint = f'{SEARCH_ENDPOINT}/locations/query'
        self.search_endpoint = f'{SEARCH_ENDPOINT}/v2/search'
    
    def get_code(self, city):
        headers = {
            'apikey': API_KEY
        }

        search_params = {
            'term': city
        }

        response = requests.get(self.endpoint, params=search_params, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['locations'][0]['code']

    def search_flight(self, origin_city_code, destination_city_code, lowest_price):
        headers = {
            'apikey': API_KEY
        }

        cur_date = datetime.now()
        departure_from = cur_date + timedelta(days=1)
        departure_to = cur_date + relativedelta(months=6)

        departure_from_format = departure_from.strftime('%d/%m/%Y')
        departure_to_format = departure_to.strftime('%d/%m/%Y')

        search_params = {
            'fly_from': origin_city_code,
            'fly_to': destination_city_code,
            'date_from': departure_from_format,
            'date_to': departure_to_format, 
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }

        response = requests.get(self.search_endpoint,  headers=headers, params=search_params)

        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None
        
        flight_data = FlightData(
            price=data['price'],
            origin_city=data['cityFrom'],
            origin_airport=data['flyFrom'],
            destination_city=data['cityTo'],
            destination_airport=data['flyTo'],
            out_date=data['route'][0]['local_departure'].split('T')[0],
            return_date=data['route'][1]['local_departure'].split('T')[0]
        )
        if flight_data.price < lowest_price:
            message_string = (
                f'Low price alert! Only £{flight_data.price} to fly '
                f'from {flight_data.origin_city}-{flight_data.origin_airport} '
                f'to {flight_data.destination_city}-{flight_data.destination_airport},'
                f'from {flight_data.out_date} to {flight_data.return_date}'
                )
            notification_manager.send_message(message_string)

        print(f'{flight_data.destination_city}: £{flight_data.price}')
        return flight_data
