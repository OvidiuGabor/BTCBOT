import workingwithdb
import time
import hashlib
import hmac


#GEt object in an array
def search_object(arr, key, value):
    for obj in arr:
        if obj.get(key) == value:
            return obj
    return None
#round the number to specific decimals
def round_dynamic(number, decimals):
    if decimals == 0:
        return int(round(number))
    return round(number, decimals)

#set the params property in the request to string
def params_to_str(obj, level, MAX_LEVEL = 3):
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

#Sign the request for the private action, before sending the request to Crypto.com api
def signRequest(request):
    if "params" in request:
        param_str = params_to_str(request['params'], 0)
    # Set the payload that will be sent to the api
    payload_str = request['method'] + str(request['id']) + request['api_key'] + param_str + str(request['nonce'])
    # Set up the security signature because we are using private end points, and it requiring signature to authentificate
    request['sig'] = hmac.new(
        bytes(str(workingwithdb.get_api_data()["api_secret"]), 'utf-8'),
        msg=bytes(payload_str, 'utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()
    return request