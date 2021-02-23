import dataScrape as d
import analysis as a
from time import sleep
import robin_stocks as r
from datetime import datetime

# defines starting variables

d.login()

owned = False

ticker = "BTC"

amountInAsset = round(30/d.price(ticker), 5)

print(amountInAsset)

api = 0

headers = a.setHeaders()

cycles = int(input("How many cycles? "))

sleep(30)

# iterates a certain amount of times
for i in range (cycles):
	print('\n')

	# displays the time
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	print("Current Time =", current_time)

	# gets the data
	try:
		indicators = d.dataPoints(ticker, 0, api)
	except:
		print("Datapoint scraping failed - redirecting api")
	
		if (api == 1):
			api = 0
		else:
			api = 1
	
		indicators = d.dataPoints(ticker, 0, api)

	# adds the predict data to a csv file
	a.append_list_as_row('predict.csv', headers, 'w')

	a.append_list_as_row("predict.csv", indicators, 'a')

	a.showIndicators(indicators)

	# creates the model and the prediction
	model = a.strat(indicators, verbose = False)
	predict = model[0]

	# gets the price
	try:
		price = d.price(ticker)
	except:
		d.login()
		price = d.price(ticker)

	print(predict)
	# chekcs to see if the bot should buy
	if (predict and not owned):
		purchasePrice = price
		owned = True
		d.buy(ticker, amountInAsset)

	# checks to see if the bot should take profits
	elif (predict and owned):
		if (((price - purchasePrice) / purchasePrice)*100 >= .75):
			owned = False
			d.sell(ticker, amountInAsset)
			print("Sold Asset (Taking gains)")
	
	# checks to see if the bot should sell
	elif (not predict and owned):
		owned = False
		d.sell(ticker, amountInAsset)

	sleep(600)

# sells all assets at the end
if (owned):
    r.order_sell_crypto_by_quantity(ticker, amountInAsset)
    print("Sold all assets - closed out")


print("Complete")