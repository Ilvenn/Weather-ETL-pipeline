import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

#import values used in the process
from config.settings import (
    OPENWEATHER_API_KEY,
    URL,
    TIMEOUT,
    CITIES,
    UNITS
)

#create session to allow multiple data to be fetched seperatly
def _get_http_session() -> requests.Session:
    session = requests.Session()#creaete session
    #Estabilish retry logic
    retries = Retry(
        total = 3,#max
        backoff_factor = 2,#how backoff control will be made
        status_forcelist=[500,502,503,504]#list of error that will trigger retry
    )
    #attach retry adapter to outgoing source to allow backgout work
    session.mount("http://", HTTPAdapter(max_retries=retries))
    return session

def fetch_weather(city: str) -> dict:
    session = _get_http_session()#gets the session
    #defines parameters used in request
    params = {
        "q" : city,
        "appid" : OPENWEATHER_API_KEY,
        "units" : UNITS
    }
    #log information
    logging.info(f"Fetching data from {city}...")

    #requests data from api
    response = session.get(URL,params = params, timeout=TIMEOUT)

    #raises for 4xx http errors to help catch them
    response.raise_for_status()
    
    #converts the data to json format
    return response.json()

#main function for all the weather data
def fetch_all_weather() -> list[dict]:
    raw_payload = []#where data will be store
    #loops through every city
    for city in CITIES:
        try:
            data = fetch_weather(city)#fetches the data
            raw_payload.append(data)#adds the data to the list
        except requests.exceptions.RequestException as err:
            logging.error(f"Error fetching data from {city}: {err}")
            
    return raw_payload