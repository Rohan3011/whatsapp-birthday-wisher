
from datetime import datetime
import os
from dotenv import load_dotenv

import pandas as pd
from twilio.rest import Client
import numpy as np


load_dotenv()  # take environment variables from .env.


account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')

client = Client(account_sid, auth_token)

def send_birthday_wish(client: Client, recipient_number:str, recipient_name:str):
    """Send a birthday wish to a recipient using their WhatsApp number.

    Args:
        client (object): An instantiation of the Twilio API's Client object
        recipient_number (str): The number associated with the recipient's WhatsApp account,
            including the country code, and prepended with '+'. For example, '+14155238886'.
        recipient_name (str): The recipient's name

    Returns:
        True if successful, otherwise returns False
    """

    birthday_wish = """
        Hey {}, this is Rohan's personal birthday wisher.
        Happy Birthday to you! I wish you all the happiness that you deserve.
        """.format(recipient_name)

    try:
        message = client.messages.create(
            body=birthday_wish,
            from_='whatsapp:+14155238886',  # This is the Twilio Sandbox number. Don't change it.
            to='whatsapp:' + recipient_number
        )

        print("Birthday wish sent to", recipient_name, "on WhatsApp number", recipient_number)
        return True

    except Exception as e:
        print("Something went wrong. Birthday message not sent.")
        print(repr(e))
        return False

def create_birthdays_dataframe():
    """Create a pandas dataframe containing birth date information from a CSV file.

    Returns:
        A dataframe if successful, otherwise returns None.
    """

    try:
        birthdays_df = pd.read_csv(
            "birth_dates.csv",
            parse_dates=['Birth Date'],
            date_format="%m-%d-%Y",
        )
        return birthdays_df

    except Exception as e:
        print("Something went wrong. Birthdays dataframe not created.")
        print(repr(e))
        return None

def check_for_birthdays():
    """Calls the send_birthday_wish() function if today is someone's birthday.

    Returns:
        True if successful, otherwise returns False.
    """
    try:
        # Read the CSV file, specifying the date format
        birthdays_df = create_birthdays_dataframe()
        if birthdays_df is None:
            return False

        today = datetime.now()
        birthdays_df["day"] = birthdays_df["Birth Date"].dt.day
        birthdays_df["month"] = birthdays_df["Birth Date"].dt.month
        for i in range(birthdays_df.shape[0]):
            birthday_day = birthdays_df.loc[i, "day"]
            birthday_month = birthdays_df.loc[i, "month"]
            if today.day == birthday_day and today.month == birthday_month:
                send_birthday_wish(client, str(birthdays_df.loc[i, "WhatsApp Number"]), str(birthdays_df.loc[i, "Name"]))
        return True

    except Exception as e:
        print("Something went wrong. Birthday check not successful.")
        print(repr(e))
        return False