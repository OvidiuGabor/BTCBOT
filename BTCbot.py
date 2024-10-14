import json
import cryptodotcomapi
import helper_function
from sanic import Sanic
from sanic import response

TEST_SYMBOL = "TIAUSD-PERP"
SIGNAL_EXAMPLE = {
"PositionSize": "1.235",
"OrderAction": "buy",
"OrderSize": "1.235",
"OrderPrice": "23.02",
"OrderID": "LONG",
"OrderComment": "LONG",
"AlertMessage": "LONG",
"StrategyMarketPosition": "LONG",
"StrategyMarketPositionSize": "1.235",
"Currency": "PIXELUSD-PERP"
}

# Create Sanic object called app
app = Sanic(__name__)
#run app
if __name__ == '__main__':
    app.run(port=5000)



#Create root / homepage
@app.route('/')
async def root(request):
    return response.text('online')

#Listen for signals
@app.route('/webhook',methods=["POST"])
async def webhook(request):
   return ""



def create_order(signaldata):
    #determine what kind of order it is. Open Position or Close Position
    #determine the type of Open Position, it is a LONG or a SHORT
    order = generate_order_template(signaldata)
    #currently we are working only with market, don't need to worry about LIMIT kind of orders
    #decide the number of decimals we will need
    #get the API_KEY Value from the db
    #create the order template
    #signt the order before submiting it, otherwise won't work, we will get authentification error.
    #submit the order
    #log the submitted order
    #log the result of the order
    print(order)
    return order



def generate_order_template(signaldata):
    order_template = get_order_json(signaldata["AlertMessage"])
    order_template["params"]["quantity"] = get_order_size(signaldata["Currency"], signaldata["OrderSize"])
    
    
    
    return order_template



#For now we are using the json file, but changes to a record in the database
def get_order_json(signaltype):
    if(signaltype == "LONG" or signaltype== "SHORT"):
        with open('open_market_position_template.json') as template :
            order_template = json.load(template)
        return order_template

    if(signaltype =="TP" or signaltype == "SL"):
        with open('close_market_position.json') as template :
            order_template = json.load(template)
        return order_template
#calculate number of decimals the symbol can have, based on the data from cryp.com api
def get_order_size(simbol, ordersize):
    symbol_list = cryptodotcomapi.public_get_instrumets()
    symbol = helper_function.search_object(symbol_list, "symbol", simbol)
    order_size = helper_function.round_dynamic(ordersize, symbol["quantity_decimals"])
    return order_size

create_order(SIGNAL_EXAMPLE)