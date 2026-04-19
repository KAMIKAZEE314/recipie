from math import *

debug = True

class Item():
	def __init__(self, item, mod="minecraft", count=1):
		self.mod = mod.lower().replace(" ", "")
		self.item = item.lower().replace(" ", "_")
		self.count = count

	def __eq__(self, other):
		if not isinstance(other, Item):
			return False
		return self.mod == other.mod and self.item == other.item and self.count == other.count	

	def get_mod(self): return self.mod
	def get_item(self): return self.item
	def get_count(self): return self.count

class Recipie():
	def __init__(self, items, result, dependencies=None, crafting_method="gather"):
		self.crafting_method = crafting_method
		self.result = result
		self.dependencies = dependencies
		if self.result.get_count() != 1:
			self.items = []
			for item in items:
				self.items.append(Item(item.get_mod(), item.get_item(), item.get_count()/self.result.get_count()))
		else:
			self.items = items

	def __eq__(self, other):
		if not isinstance(other, Recipie):
			return False
		return self.crafting_method == other.crafting_method and self.result == other.result and self.dependencies == other.dependencies and self.items == other.items

	def get_required_items(self, count=1):
		required_items = []
		for item in self.items:
			required_items.append(Item(item.get_mod(), item.get_item(), item.get_count()*ceil(count/self.result.get_count())))

		return required_items

	def output_form(self, count=1):
		message = self.crafting_method.title() + " "
		message += str(self.result.get_count()*ceil(count/self.result.get_count())) + " "
		message += self.result.get_item().replace("_", " ").title()

		return message
				
def dprint(text, end="\n"):
	if debug:
		print(text, end=end)
	return text

if __name__ == "__main__":
	pass
