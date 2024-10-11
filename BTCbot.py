import cryptodotcomapi
import helper_function
from sanic import Sanic
from sanic import response

TEST_SYMBOL = "TIAUSD-PERP"

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


#symbol_list = cryptodotcomapi.public_get_instrumets()
#symbol = helper_function.search_object(symbol_list, "symbol", TEST_SYMBOL)
#print(helper_function.round_dynamic(1254.8945, symbol["quantity_decimals"]))