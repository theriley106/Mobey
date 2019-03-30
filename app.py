from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
from keys import *
import requests
import search

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
	CALL_LIST.append(callerInfo)
	print("CLOSEST TMOBILE STORE: {}".format(search.store_by_zip(callerInfo['FromZip'])['location']['address']))
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
	#print
	# {u'phone': u'iphone'}
	intent = requestVal['queryResult']['intent']['displayName']
	if intent == 'welcome':
		return jsonify(genSpeech("Welcome to Tmobile One"))
	elif intent == "closestStore":
		return jsonify(genSpeech('Your closest store is ' + search.store_by_zip(CALL_LOG[sessionID]['FromZip'])['name']))
	elif intent == 'buy':
		return jsonify(genSpeech("I see you're trying to buy a {}".format(parameters['phone'])))
	else:
		return jsonify(genSpeech("I'm not sure what intent you called but okay"))


if __name__ == '__main__':
	#print long_lat_to_address("-84.3880", "33.7490")
	#print address_to_long_lat("94030")
	app.run(host='0.0.0.0', port=5000, debug=True)
