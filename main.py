from math import *
import json
import os

debug = True

class Item():
	def __init__(self, item, mod="minecraft", count=1):
		self.mod = mod.lower().replace(" ", "")
		self.item = item.lower().replace(" ", "_")
		self.count = count
	
	@classmethod
	def from_json(self, json):
		return Item(json["item"], json["mod"], int(json["count"]))

	def __eq__(self, other):
		if not isinstance(other, Item):
			return False
		return self.mod == other.mod and self.item == other.item and self.count == other.count	

	def get_mod(self): return self.mod
	def get_item(self): return self.item
	def get_count(self): return self.count

	def json_form(self):
		return {"mod": self.mod, "item": self.item, "count": str(self.count)}

class Recipie():
	def __init__(self, items, result, dependencies=[], crafting_method="gather", is_end_recipie=False):
		self.crafting_method = crafting_method
		self.dependencies = dependencies
		self.items = items
		self.result = result
		self.is_end_recipie = is_end_recipier11t27

	@classmethod
	def from_json(self, json):
		return Recipie(list(map(Item.from_json, json["items"])), Item.from_json(json["result"]), json["dependencies"], json["crafting_method"])

	def __eq__(self, other):
		if not isinstance(other, Recipie):
			return False
		return self.crafting_method == other.crafting_method and self.result == other.result and self.dependencies == other.dependencies and self.items == other.items

	def get_required_items(self, count=1):
		if not self.is_end_recipie:
			required_items = []
			for item in self.items:
				required_items.append(Item(item.get_mod(), item.get_item(), item.get_count()*ceil(count/self.result.get_count())))
		
			return required_items
		else:
			return []

	def output_form(self, count=1):
		message = self.crafting_method.title() + " "
		message += str(self.result.get_count()*ceil(count/self.result.get_count())) + " "
		message += self.result.get_item().replace("_", " ").title()

		return message

	def json_form(self):
		items = []
		for item in self.items:
			items.append(item.json_form())
		
		return {"crafting_method": self.crafting_method, "result": self.result.json_form(), "dependencies": self.dependencies, "items": items}
				
def dprint(text, end="\n"):
	if debug:
		print(f"\033[36m{text}\033[0m", end=end)
	return text

if __name__ == "__main__":
	# choose modpack
	print("Modpacks: ")
	with open("modpacks.json", "r") as file:
		modpacks = json.load(file)
		for modpack in modpacks:
			print(modpack)
	print()

	modpack = input("Which modpack: ").lower().replace(" ", "_")

	if not modpack in modpacks:
		mods = list(map(lambda x: x.lower().replace(" ", "_"), input(f"What mods are in the modpack \"{modpack}\", that add crafting recipies(seperated by comma and if not sure list it): ").split(", ")))
		dprint(mods)

		with open("modpacks.json", "w") as file:
			json.dump(modpacks, file)
	
	mods = modpacks[modpack]
	mods.append("minecraft")

	# load recipies
	json_recipies = [] # List to collect all recipies
	
	for mod in mods:
		if not os.path.exists(mod):
			os.mkdir(mod)

			with open(f"{mod}/recipies.json", "w") as file:
				json.dump({}, file)

		with open(f"{mod}/recipies.json", "r") as file:
			dprint(json.load(file))
	"""
	for mod in mods:
		if not os.path.exists(mod):
			os.mkdir(mod)
			with open(f"{mod}/recipies.json", "w") as file:
				json.dump({}, file)

		with open(f"{mod}/recipies.json", "r") as file:
			if json.load(file) != {}:
				file.seek(0)
				json_recipies.append(json.load(file))
	"""

	# convert recipie json to recipie class objects
	"""
	recipies = {}
	for recipie in json_recipies:
		dprint("recipie")
		if not recipie["result"]["mod"] in recipies.keys():
			recipies[recipie["result"]["mod"]] = {}
		recipies[recipie["result"]["mod"]][recipie["result"]["item"]] = Recipie.from_json(recipie)
	
	dprint(recipies)
	"""	

	# main logic
	"""
	target_mod = input("From which mod is the item: ").lower().replace(" ", "_")
	if not target_mod in mods:
		print(f"The mod \"{target_mod}\" isn't in your selected modpack")

	required_items = []
	crafting_steps = []
	depth_list = [(target_mod, input("Which item do you want to craft: "))]
	depth = 0
	while depth_list != []:
		index = 0
		while index < len(depth_list):
			mod, item = depth_list[index]
	"""		
	
