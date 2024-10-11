import workingwithdb
import helper_function
import json
import requests
# Set the Env variable
BASE_URL = "https://api.crypto.com/exchange/v1/"


def get_api_key():
    return workingwithdb.get_api_data()
#with this function we can get a list of all instrumets, then based on the instrument we can calculate the decimals for the order quantity, and for the price.
#with this data, we can calculate automatically all orders for all symbols
#it returns an array of symols
def public_get_instrumets():
    url = f'{BASE_URL}{"public/get-instruments"}'
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()["result"]["data"]

def private_post_order():
    return 

def private_close_order():
    return