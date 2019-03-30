
import json
import re

a = json.load(open("inventory.json"))

def get_sku_by_mem_phone(phone, memory):
	for val in a['values']['products']:
		if val["familyName"].encode('ascii',errors='ignore').lower().replace("+", " plus") == phone or val["productName"].encode('ascii',errors='ignore').lower().replace("+", " plus") == phone:
			memoryIndex = re.findall("\d+", val["deviceMemorySKU"]).index(memory)
			sku = val['skuCode'].split("|")[memoryIndex]
			return sku

if __name__ == '__main__':
	print get_sku_by_mem_phone("lg stylo 4", "32")
	raw_input(" ")
	for v in a['values']['products']:
		phone = v["familyName"].encode('ascii',errors='ignore').lower().replace("+", " plus")
		if len(phone) == 0:
			phone = v["productName"].encode('ascii',errors='ignore').lower().replace("+", " plus")
		memory = re.findall("\d+", v["deviceMemorySKU"])
		for val in memory:
			if int(val) == 1:
				print("{} {}".format(val, phone))
				print("{} terabyte {}".format(val, phone))
				print("{} terabyte {}".format(val, phone))
			else:
				print("{} {}".format(val, phone))
				print("{} gigabyte {}".format(val, phone))
				print("{} {} gigabyte".format(phone, val))
