import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://doadmin:86x5SI41gUp072fC@tradingbotdb-39d2c47b.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=tradingbotdb")
db = cluster["TradingbotDb"]


#gets the api key data and respose as a json
def get_api_data():
    collection = db["Cryptodotcom-Api-key"]
    api_key = collection.find_one({"_id" : "API_KEY"})
    api_secret = collection.find_one({"_id" : "API_SECRET"})
    return({"api_key": api_key["value"], "api_secret": api_secret["value"]})

#write Trading view alert to db
def write_tradingview_to_db(data):
    return

#write the output of the api call to the db
def write_api_output_to_db(output):
    return
