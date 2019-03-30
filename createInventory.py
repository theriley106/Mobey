
import json
import re

a = json.load(open("inventory.json"))

def get_sku_by_mem_phone(phone, memory=None):
	for val in a['values']['products']:
		if val["familyName"].encode('ascii',errors='ignore').lower().replace("+", " plus") == phone or val["productName"].encode('ascii',errors='ignore').lower().replace("+", " plus") == phone:
			if memory == None:
				return val['skuCode'].split("|")[0]
			allVals = re.findall("\d+", val["deviceMemorySKU"])
			print allVals
			if str(memory) in allVals:
				memoryIndex = allVals.index(memory)
			else:
				memoryIndex = 0
			sku = val['skuCode'].split("|")[memoryIndex]
			return sku

def get_phone_info_with_sku(skuNumber):
	for val in a['values']['products']:
		if str(skuNumber) in str(val):
			return val["productDisplayName"]


if __name__ == '__main__':
	#print get_sku_by_mem_phone("lg stylo 4")
	#raw_input(" ")
	for v in a['values']['products']:
		phone = v["familyName"].encode('ascii',errors='ignore').lower().replace("+", " plus")
		if len(phone) == 0:
			phone = v["productName"].encode('ascii',errors='ignore').lower().replace("+", " plus")
		memory = re.findall("\d+", v["deviceMemorySKU"])
		print("\"{}\", \"{}\"".format(phone, phone))
		"""for val in memory:
									if int(val) == 1:
										print("{} {}".format(val, phone))
										print("{} terabyte {}".format(val, phone))
										print("{} terabyte {}".format(val, phone))
									else:
										print("{} {}".format(val, phone))
										print("{} gigabyte {}".format(val, phone))
										print("{} {} gigabyte".format(phone, val))"""
