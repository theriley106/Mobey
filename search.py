import requests
import bs4


def check_stock(itemNum):
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

	data = '{"products":["' + itemNum + '"],"locations":["2021","4164","2994","9282","7783","5787","9120","2008","5218","5453","301E","9008","7648","7782","5725","7763","2450","4296","624E","927D","5274"]}'

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
	query = raw_input("Query: ")
	val = search(query)
	raw_input(val)
	if len(val) > 0:
		print check_stock(val[0])

#x = get_suggestions("ihpone xs")
#print search("ihpne xs")
#print x
#print x
