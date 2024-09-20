import json
import requests
import time
import hashlib
import hmac
from sanic import Sanic
from sanic import response


# Set the Env variable
BASE_URL = "https://api.crypto.com/exchange/v1/"
API_KEY= ""
SECRET_KEY=""
param_str = ""
MAX_LEVEL = 3
METHOD = ""

# Get the Secret and keys from the file
with open('keys.json') as keys :
    information = json.load(keys)
    API_KEY = information['api_key']
    SECRET_KEY = information['api_secret']
# Set up the request
reqForOpenPosition = {
    "id": 1,
    "method": "private/create-order",
    "api_key": API_KEY,
    "params": {
        "instrument_name": "",
        "side": "BUY",
        "type": "MARKET",
        "price": "2450.00",
        "quantity": "0.001"
        #"client_oid": "c5f682ed-7108-4f1c-b755-972fcdca0f02",
        #"exec_inst": ["POST_ONLY"],
        #"time_in_force": "FILL_OR_KILL"
    },
    "nonce": int(time.time() * 1000)
}
reqForClosePosition = {
    "id": 1,
    "method": "private/close-position",
    "api_key": API_KEY,
    "params": {
        "instrument_name": "",
        "type": "MARKET",
    },
    "nonce": int(time.time() * 1000)
}
# Create Sanic object called app
app = Sanic(__name__)
#app.ib = None

#Create root / homepage
@app.route('/')
async def root(request):
    return response.text('online')

#Listen for signals
@app.route('/webhook',methods=["POST"])
async def webhook(request):
    if request.method == 'POST':
        #Parse signal Data
        data = request.json
        print(data)
        if data["AlertMessage"] == "LONG" or data["AlertMessage"] == "SHORT":
            reqForOpenPosition["params"]["instrument_name"] = data["Currency"]
            reqForOpenPosition["params"]["side"] = data["OrderAction"].upper()
            #req["params"]["price"] = data["OrderPrice"]
            reqForOpenPosition["params"]["quantity"] = data["OrderSize"]
            print(reqForOpenPosition)
            signedRequest = signRequest(reqForOpenPosition)
            print(reqForOpenPosition)
            result = make_request("private/create-order",signedRequest)

        if data["AlertMessage"] == "TP" or data["AlertMessage"] == "SL":
            reqForClosePosition["params"]["instrument_name"] = data["Currency"]
            print(reqForClosePosition)
            signedRequest = signRequest(reqForClosePosition)
            print(reqForClosePosition)
            result = make_request("private/close-position",signedRequest)
        
        print(result)
        return response.text('Posted')



#run app
if __name__ == '__main__':
    app.run(port=5000)




#set the params property in the request to string
def params_to_str(obj, level):
    if level >= MAX_LEVEL:
        return str(obj)

    return_str = ""
    for key in sorted(obj):
        return_str += key
        if obj[key] is None:
            return_str += 'null'
        elif isinstance(obj[key], list):
            for subObj in obj[key]:
                return_str += params_to_str(subObj, level + 1)
        else:
            return_str += str(obj[key])
    return return_str



def signRequest(request):
    if "params" in request:
        param_str = params_to_str(request['params'], 0)
    # Set the payload that will be sent to the api
    payload_str = request['method'] + str(request['id']) + request['api_key'] + param_str + str(request['nonce'])
    # Set up the security signature because we are using private end points, and it requiring signature to authentificate
    request['sig'] = hmac.new(
        bytes(str(SECRET_KEY), 'utf-8'),
        msg=bytes(payload_str, 'utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()
    return request

# Send the request 
def make_request(endpoint, requestdata, method='POST'):
    url = f'https://api.crypto.com/exchange/v1/{endpoint}'
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.request(method, url, headers=headers, json=requestdata)
    return response.json()


def get_method(input):
    if(input == "LONG" or input== "SHORT"):
        return "private/create-order"
    
    if(input =="TP" or input == "SL"):
        return "private/close-position"

# Example API call to get account balance
#result = make_request('private/cancel-order')
#print(result)