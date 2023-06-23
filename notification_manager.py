import os
from twilio.rest import Client
from dotenv import dotenv_values

config = dotenv_values('.env')

AUTH_TOKEN = config['AUTH_TOKEN']
ACC_SID= config['ACC_SID']
PHONE_NUMBER = config['PHONE_NUMBER']
SENDER_PHONE_NUMBER = config['SENDER_PHONE_NUMBER']

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(ACC_SID, AUTH_TOKEN)

    def send_message(self, message):
        message = self.client.messages.create(
            from_=SENDER_PHONE_NUMBER,
            to=PHONE_NUMBER,
            body=message
        )
        print(message.sid)