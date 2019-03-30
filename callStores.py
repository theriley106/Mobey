import json

if __name__ == '__main__':
	print("""
		[1] Ayush
		[2] Chris
		[3] Nathan
		""")
	personVal = raw_input("Who is this (1,2,3)? ")
	g = {'1': "ayush", '2': 'chris', '3': 'nathan'}
	a = json.load(open(g[personVal] + ".json"))
	try:
		finished = json.load(open(g[personVal] + "_done.json"))
	except:
		finished = []
	toRemove = []
	for val in finished:
		for v in a:
			if val['id'] == v['id']:
				toRemove.append(v)
	print(toRemove)
	for v in toRemove:
		try:
			a.remove(v)
		except:
			pass
	for val in a:
		print("Call: {}".format(val['telephone']))
		raw_input("Click Enter When Done")
		correctVal = False
		timeVal = raw_input("Call Time (Seconds): ")
		while raw_input("Is {} seconds Correct? (Y/N) ".format(timeVal)).lower() != "y":
			timeVal = raw_input("Call Time (Seconds): ")
		try:
			val['seconds'] = int(timeVal)
		except:
			val['seconds'] = 0
		finished.append(val)
		with open(g[personVal] + "_done.json", 'w') as outfile:
			json.dump(finished, outfile, indent=4)


