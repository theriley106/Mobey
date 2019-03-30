from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session

app = Flask(__name__, static_url_path='/static')

def genSpeech(speech, stayOpen=True):
	return {
	    'fulfillmentText': speech
	}

@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")

@app.route('/webhook', methods=['GET', 'POST'])
def testPage():
	requestVal = request.get_json()
	sessionID = requestVal.get('session', "INVALID ID")
	print sessionID
	parameters = requestVal.get("queryResult", {}).get('parameters', None)
	#print
	# {u'phone': u'iphone'}
	intent = requestVal['queryResult']['intent']['displayName']
	if intent == 'welcome':
		return jsonify(genSpeech("Welcome to Tmobile One"))
	elif intent == 'buy':
		return jsonify(genSpeech("I see you're trying to buy a {}".format(parameters['phone'])))
	else:
		return jsonify(genSpeech("I'm not sure what intent you called but okay"))


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
