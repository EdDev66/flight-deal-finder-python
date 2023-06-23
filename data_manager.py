import requests
from dotenv import dotenv_values

config = dotenv_values('.env')

SHEETY_ENDPOINT = config['SHEETY_ENDPOINT']

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.endpoint = SHEETY_ENDPOINT
        

    def fetch_data(self):
        response = requests.get(self.endpoint)
        response.raise_for_status()
        data = response.json()
        return data['prices']
    
    def update_data(self, id, code):
        update_params = {
            'price': {
                'iataCode': code
            }
        }

        response = requests.put(f'{self.endpoint}/{id}', json=update_params)
        response.raise_for_status()
        print(response.text)
        return