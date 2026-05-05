from math import *
import json
import os

debug = True

class Item():
	def __init__(self, item, mod="minecraft", count=1):
		self.mod = mod.lower().replace(" ", "")
		self.item = item.lower().replace(" ", "_")
		self.count = int(count)
	
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

	def output_form(self):
		return str(self.count) + "x " + self.item.replace("_", " ").title()

	def json_form(self):
		return {"mod": self.mod, "item": self.item, "count": str(self.count)}

class Recipie():
	def __init__(self, items, result, crafting_method="gather"):
		self.crafting_method = crafting_method
		self.items = items
		self.result = result

	@classmethod
	def from_json(self, json):
		return Recipie(list(map(Item.from_json, json["items"])), Item.from_json(json["result"]), json["crafting_method"])

	def __eq__(self, other):
		if not isinstance(other, Recipie):
			return False
		return self.crafting_method == other.crafting_method and self.result == other.result and self.items == other.items

	def get_required_items(self, count=1):
		required_items = []
		for item in self.items:
			required_items.append(Item(item.get_item(), item.get_mod(), item.get_count()*ceil(count/self.result.get_count())))
		
		return (required_items, ceil(count/self.result.get_count()))

	def output_form(self, craft_count=1):
		message = self.crafting_method.title() + " "
		if len(self.items) > 0:
			for item in self.items:
				message += str(item.get_count()*craft_count) + " " + item.get_item().replace("_", " ").title() + ", "
			message = message[:-2]
			message += " to "
		message += str(self.result.get_count()*craft_count) + " "
		message += self.result.get_item().replace("_", " ").title()

		return message

	def json_form(self):
		items = []
		for item in self.items:
			items.append(item.json_form())
		
		return {"crafting_method": self.crafting_method, "result": self.result.json_form(), "items": items}
				
def dprint(text, end="\n"):
	if debug:
		print(f"\033[36m{text}\033[0m", end=end)
	return text

def ddump(dic):
	if debug:
		with open("debug.txt", "a") as file:
			json.dump(dic, file)

def make_new_recipie(item):
	item_output_form = item.get_item().replace("_", " ").title()
	while True:
		print()
		print("We are gonna guide you through recipie creation")
		crafting_method = input(f"Which method do you use to make \"{item_output_form}\"(e.g smelt, craft, gather): ").lower().replace(" ", "_")
		if crafting_method in ["quit", "exit", "cancel"]:
			return None
		text_items = input(f"What Items are needed to make (seperated by commas)[pattern: count itemname mod]: ").split(",")
		dprint(text_items)
		item_objects = []
		for text_item in text_items:
			split = text_item.strip().split()
			dprint(split)
			if len(split) == 3:
				item_objects.append(Item(split[1].lower().replace(" ", "_"), split[2].lower().replace(" ", "_"), int(split[0])))
			else:
				break
		
		while True:
			try:
				count = int(input(f"How many of \"{item_output_form}\" do you get with this recipie: "))
				break
			except ValueError:
				print("You must input only numbers!")
		
		mod = input("Which mod implements this recipie: ").lower().replace(" ", "_")
							
		new_recipie = Recipie(item_objects, Item(item.get_item(), item.get_mod(), count), crafting_method)

		if not os.path.exists(mod):
			os.mkdir(mod)
			with open(f"{mod}/recipies.json", "w") as file:
				json.dump({}, file)

		content = None
		with open(f"{mod}/recipies.json", "r") as file:
			content = json.load(file)
		with open(f"{mod}/recipies.json", "w") as file:
			if not mod in content.keys():
				content[mod] = {}
			if not new_recipie.result.get_item() in content[mod].keys():
				content[mod][new_recipie.result.get_item()] = []
						
			content[mod][new_recipie.result.get_item()].append(new_recipie.json_form())

			json.dump(content, file, indent=4)

		if not mod in mods:
			print("Your new recipie is in a mod, that's not in this modpack. We still saved it")
			continue
		else:
			if not mod in recipies.keys():
				recipies[mod] = {}
			if not new_recipie.result.get_item() in recipies[mod].keys():
				recipies[mod][new_recipie.result.get_item()] = []
			recipies[mod][new_recipie.result.get_item()].append(new_recipie)

		if input(f"Do you want to add another relevant recipie for \"{item_output_form}\"[y, n]: ") == "n": break
	
def get_nodes_at_depth(depth, tree, current_path=[]):
	nodes = []
	if depth != 0:
		for base_node_key in tree:
			base_node = tree[base_node_key]
			if "children" in base_node.keys():
				nodes.extend(get_nodes_at_depth(depth-1, base_node["children"], current_path + [base_node_key]))
	else:
		for base_node_key in tree:
			base_node = tree[base_node_key]
			nodes.append((base_node_key, current_path, base_node))
	return nodes

if __name__ == "__main__":
	# choose modpack
	print("Modpacks: ")
	with open("modpacks.json", "r") as file:
		modpacks = json.load(file)
		for modpack in modpacks:
			print(modpack.replace("_", " ").title())
	print()

	modpack = input("Which modpack: ").lower().replace(" ", "_")

	if not modpack in modpacks:
		mods = list(map(lambda x: x.lower().replace(" ", "_"), input(f"What mods are in the modpack \"{modpack}\", that add crafting recipies(seperated by comma and if not sure list it): ").split(", ")))
		dprint(mods)
		modpacks[modpack] = mods

		with open("modpacks.json", "w") as file:
			json.dump(modpacks, file)
	
	mods = modpacks[modpack]
	mods.append("minecraft")

	# load recipies
	json_recipies = {}
	
	for mod in mods:
		if not os.path.exists(mod):
			os.mkdir(mod)

			with open(f"{mod}/recipies.json", "w") as file:
				json.dump({}, file)

		with open(f"{mod}/recipies.json", "r") as file:
			content = json.load(file)
			for key in content.keys():
				if not key in json_recipies.keys():
					json_recipies[key] = content[key]
				else:
					for key2 in json_recipies[key].keys():
						if key2 in content[key].keys():
							content[key][key2].extend(json_recipies[key][key2])

					json_recipies[key] |= content[key]

	with open("debug.txt", "w") as file:
		json.dump(json_recipies, file, indent=4)
	dprint(json_recipies)

	# convert recipie json to recipie class objects
	recipies = {}
	for mod_key in json_recipies:
		mod = json_recipies[mod_key]
		for item_key in mod:
			item = mod[item_key]
			new_item = []
			for recipie in item:
				dprint(recipie)
				new_item.append(Recipie.from_json(recipie))
			if not mod_key in recipies.keys():
				recipies[mod_key] = {}

			recipies[mod_key][item_key] = new_item

	dprint(recipies)

	# main logic
	target_mod = input("From which mod is the item: ").lower().replace(" ", "_")
	if not target_mod in mods:
		print(f"The mod \"{target_mod}\" isn't in your selected modpack")
		quit()

	target_item = input("Which Item: ").lower().replace(" ", "_")

	target_count = input("How much: ").lower().replace(" ", "_")
	
	crafting_steps = []
	crafting_tree = {
		f"{target_mod}:{target_item}": {}
	}
	isnt_expanded = True
	path = []
	depth = 0
	#while isnt_expanded:
		

	"""
	crafting_steps = []
	depth_list = [Item(target_item, target_mod, target_count)]
	while depth_list != []:
		# expand recipies once
		index = 0
		while index < len(depth_list):
			item = depth_list[index]
			item_output_form = item.get_item().replace("_", " ").title()
			# get valid recipies
			if not item.get_mod() in recipies.keys():
				recipies[item.get_mod()] = {}
			
			valid_recipies = []
			for mod_key in recipies:
				mod = recipies[mod_key]
				if item.get_item() in mod.keys():
					valid_recipies.extend(mod[item.get_item()])
			chosen_recipie = None
			if len(valid_recipies) > 1:
				print(f"\nWhat is your preferred recipie for \"{item_output_form}\": ")
				for i, recipie in enumerate(valid_recipies):
					print(f"{i}: \"{recipie.output_form()}\"")
				print(f"{len(valid_recipies)}: Create new recipie")
				
				while True:
					try:
						chosen_num = int(input("Which option: "))
					except ValueError:
						print("You must enter only numbers!\n")
						continue
				
					if chosen_num >= 0 and chosen_num <= len(valid_recipies):
						if chosen_num == len(valid_recipies):
							make_new_recipie(item)
						else:
							chosen_recipie = valid_recipies[chosen_num]
						break
					else:
						print("Number is out of range!\n")
						continue

				if not chosen_recipie:
					continue
				
			elif len(valid_recipies) == 1:
				chosen_recipie = valid_recipies[0]
				if input(f"Is the recipie \"{chosen_recipie.output_form()}\" good, if not then give us a new one[y, n]: ") == "n":
					make_new_recipie(item)
					continue
			elif len(valid_recipies) == 0:
				print(f"There is no recipie for the item \"{item_output_form}\"")
				make_new_recipie(item)
				continue
			dprint(chosen_recipie.output_form())
			
			# expand recipie
			recipie_items, result_count_multiplier = chosen_recipie.get_required_items(item.get_count())
			dprint(recipie_items)
			dprint(result_count_multiplier)
			for recipie_item in recipie_items:
				dprint(recipie_item.output_form())
			dprint(chosen_recipie.output_form(result_count_multiplier))
			
			crafting_steps.append((chosen_recipie, result_count_multiplier))
			depth_list.extend(recipie_items)			

			del depth_list[index]
			index += len(recipie_items)
	
	crafting_steps.reverse()
	dprint(f"crafting_steps pre: {crafting_steps}")

	# merge same steps in crafting_steps
	index = 0
	while index < len(crafting_steps):
		recipie, multiplier = crafting_steps[index]
		index2 = 0
		while index2 < len(crafting_steps):
			recipie2, multiplier2 = crafting_steps[index2]
			if index != index2 and recipie == recipie2:
				crafting_steps[index] = (recipie, multiplier+multiplier2)
				crafting_steps.remove((recipie2, multiplier2))
			else:
				index2 += 1
		index += 1

	dprint(f"crafting_steps post: {crafting_steps}")

	print("\nCrafting steps: \n")

	for recipie, multiplier in crafting_steps:
		print(recipie.output_form(multiplier))
	"""
