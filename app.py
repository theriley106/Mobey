# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
from keys import *
import requests
import search
import createInventory
import time
import os

CALL_LIST = []
CALL_LOG = {}

app = Flask(__name__, static_url_path='/static')

def genSpeech(speech, stayOpen=True):
	return {
	    'fulfillmentText': speech
	}

@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")

@app.route('/twilio', methods=['GET', 'POST'])
def twilioRedirect():
	callerInfo = request.form.to_dict()
	storeVals = search.store_by_zip(callerInfo['FromZip'])
	callerInfo['closed'] = storeVals[0]['hours'][3]["formattedCloses"]
	CALL_LIST.append(callerInfo)
	print("CLOSEST TMOBILE STORE: {}".format(storeVals[0]['location']['address']))
	resp = VoiceResponse()
	resp.dial('801-406-1288')
	return str(resp)

@app.route('/webhook', methods=['GET', 'POST'])
def testPage():
	requestVal = request.get_json()
	sessionID = requestVal.get('session', "INVALID ID")
	if sessionID not in CALL_LOG:
		if len(CALL_LIST) > 0:
			CALL_LOG[sessionID] = CALL_LIST.pop()
	print CALL_LOG
	parameters = requestVal.get("queryResult", {}).get('parameters', None)
	print parameters
	# {u'phone': u'iphone'}

	#raw_input(CALL_LOG[sessionID]['closed'])
	intent = requestVal['queryResult']['intent']['displayName']
	if intent == 'welcome':
		return jsonify(genSpeech("Thanks for calling Tmobile One.  What can I help you with today?"))
	elif intent == "closestStore":
		return jsonify(genSpeech('Your closest store is ' + search.store_by_zip(CALL_LOG[sessionID]['FromZip'])[0]['name'] + " and they close at {}.  If you ask me a question I'm not able to answer, I will route you directly to this store.  What can I help you with today?".format(CALL_LOG[sessionID]['closed'])))
	elif intent == "hours":
		return jsonify(genSpeech('Your closest store is ' + search.store_by_zip(CALL_LOG[sessionID]['FromZip'])[0]['name'] + " and they close at {}.  Is there anything else I can help you with today?".format(CALL_LOG[sessionID]['closed'])))
	elif intent == 'buy':
		phone = parameters['phone']
		memory = parameters.get("memory", None)
		sku = createInventory.get_sku_by_mem_phone(phone, memory)
		#print CALL_LOG[sessionID]
		#raw_input("WAITING")
		stores = [x['id'] for x in search.store_by_zip(CALL_LOG[sessionID].get('FromZip'))]
		stockInfo = search.check_stock(sku, stores)
		found = False
		returnVal = "Unfortunately, the device is not in stock at any stores near your location."
		for val in stockInfo.get('result', {}).get('inventoryAvailabilityList', []):
			try:
				s = val['storeId']
				q = val['skuDetails'][0]['quantity']['availableQuantity']
				print("Checking Store ID: {} | Availability: {}".format(s, q))
			except:
				pass
			time.sleep(.05)

		for val in stockInfo.get('result', {}).get('inventoryAvailabilityList', []):
			try:
				s = val['storeId']
				q = val['skuDetails'][0]['quantity']['availableQuantity']
				print("Checking Store ID: {} | Availability: {}".format(s, q))
				if int(q) > 0:
					found = True
					print("CLOSEST STORE WITH SKU: {} IN STOCK: Store {}".format(sku, s))
					break
			except:
				pass
		if found:
			fVal = search.get_info_store(CALL_LOG[sessionID].get('FromZip'), s)
			returnVal = "{} has the {} in stock.  Would you like me to transfer you to a representative from the {} store?  ".format(fVal, createInventory.get_phone_info_with_sku(sku), fVal.partition("The store on ")[2].partition(" in ")[0])
		print("customer is looking for SKU: {}".format(sku))
		return jsonify(genSpeech(returnVal))
	elif intent == 'payBill':
		message = """Thank you for paying your bill Using T-Mobile One.  Your payment has been processed and will show up on your account statement within 3-5 business days."""
		os.system("lib messagebird.sms.create --recipient 18646097067 --body {}".format(message))
		return jsonify(genSpeech("Bill has been successfully paid.  We have sent you a text message will your payment receipt.  Note that this message will not count towards your text allowance.  Is there anything else I can help you with today?"))
	else:
		return jsonify(genSpeech("I'm not sure what intent you called but okay"))


if __name__ == '__main__':
	#print long_lat_to_address("-84.3880", "33.7490")
	#print address_to_long_lat("94030")
	app.run(host='0.0.0.0', port=5000, debug=True)
