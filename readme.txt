This should be a script for postig order on different platforms
Currently only works with Crypto.com, maybe in the future will be able to run on multiple platforms

It takes the alert from Trading View Strategy Tester, and then based on the alert type, it creates an order and post it uwing the api.
It can also trigger TP and SL, then will close the order.

It should handle Market Order, but also LIMIT_ORDER type of trade.

For this project i am using SANIC to create an order and handle the incomig Alerts and routing them to the corect end point.
For tunneling i am using ngrok, that will create a link, which will be used in Trading View Alert seeting as a webhook.