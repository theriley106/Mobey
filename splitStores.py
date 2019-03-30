import json
import random

a = json.load(open("data.json"))

if __name__ == '__main__':
	random.shuffle(a)
	for person in ['ayush', 'nathan', 'chris']:
		e = []
		for i in range(15):
			e.append(a.pop(0))
		with open('{}.json'.format(person), 'w') as outfile:
			json.dump(e, outfile, indent=4)
