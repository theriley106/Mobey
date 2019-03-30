import requests
import bs4
from keys import *
import json

def long_lat_to_address(longVal, lat):
	res = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key={}".format(lat, longVal, google))
	return res.json()['results'][0]['formatted_address']

def address_to_long_lat(address):
	address = address.replace(" ", "+")
	res = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(address, google))
	return res.json()['results'][0]['geometry']['location']

def find_stores(longLatDict):
	res = requests.get("https://onmyj41p3c.execute-api.us-west-2.amazonaws.com/prod/getStoresByCoordinates?latitude={}&longitude={}&count=50&radius=20&ignoreLoadingBar=false".format(longLatDict['lat'], longLatDict['lng']))
	return res.json()

def store_by_zip(zipCode):
	print(zipCode)
	a = address_to_long_lat(zipCode)
	return find_stores(a)

def get_info_store(zipCode, storeNum):
	a = store_by_zip(str(zipCode))
	for val in a:
		if val['id'] == str(storeNum):
			return "The store on {} in {} {}".format(val['name'], val['location']['address']["addressLocality"], val['location']['address']["addressRegion"])

def check_stock(itemNum, locations):
	headers = {
	'Origin': 'https://www.t-mobile.com',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'en-US,en;q=0.9,es-US;q=0.8,es;q=0.7,ru-BY;q=0.6,ru;q=0.5',
	'Authorization': 'Bearer 831f6f6f-c779-4f66-9f82-7038c2ca82fb',
	'interactionid': 'getInventoryAvailabilityByProductAndLocation',
	'channelid': 'web',
	'Connection': 'keep-alive',
	'applicationid': 'frontend',
	'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
	'activityid': 'ae8fcfc4-da53-4cbb-be05-8b7927723e54',
	'Accept': 'application/json, text/plain, */*',
	'timestamp': '2019-03-27T19:27:49.758Z',
	'Referer': 'https://www.t-mobile.com/cell-phone/apple-iphone-xs?color=gold&memory=64gb',
	'Content-Type': 'application/json;charset=UTF-8',
	}
	#print "{}".format([str(x) for x in locations])
	data = '{"products":["' + itemNum + '"],"locations":' + "{}".format(json.dumps([str(x) for x in locations])) + '}'
	response = requests.post('https://core.saas.api.t-mobile.com/supplychain/inventoryavailability/v1/inventory/search/inventory-details-view', headers=headers, data=data)
	#print response.text
	return response.json()


def search_query(query):
	res = requests.get("https://sp10050ebc.guided.ss-omtrdc.net/?category=device&count=20&do=redesign&i=1&is_auth=0&mlay=Grid&page=1&q={}&rank=device_rank".format(query.replace(" ", "+")))
	y = res.json()
	a = []
	g = []
	for val in y.get("suggestions", []):
		a.append(val['suggestion'])
	for val in y['resultsets']:
		for v in val['results']:
			g.append(v['OM_SKU'])
	return g

def get_suggestions(query):
	res = requests.get("https://sp10050ebc.guided.ss-omtrdc.net/?category=device&count=20&do=redesign&i=1&is_auth=0&mlay=Grid&page=1&q={}&rank=device_rank".format(query.replace(" ", "+")))
	y = res.json()
	a = []
	for val in y.get("suggestions", []):
		a.append(val['suggestion'])
	return a

def search(query):
	y = []
	a = [query] + get_suggestions(query)
	for val in a:
		y += search_query(val)
		if len(y) > 0:
			return y

if __name__ == '__main__':
	stores = [x['id'] for x in store_by_zip('29680')]
	for store in stores:
		raw_input(get_info_store('29680', store))
	stockInfo = check_stock("190198451972", stores)
	for val in stockInfo.get('result', {}).get('inventoryAvailabilityList', []):
		try:
			s = val['storeId']
			q = val['skuDetails'][0]['quantity']['availableQuantity']
			print("Store ID: {} | Availability: {}".format(s, q))
		except:
			pass
	raw_input(" ")
	for val in store_by_zip("29680"):
		print val['id']
	query = raw_input("Query: ")
	val = search(query)
	raw_input(val)
	if len(val) > 0:
		print check_stock(val[0])

#x = get_suggestions("ihpone xs")
#print search("ihpne xs")
#print x
#print x
