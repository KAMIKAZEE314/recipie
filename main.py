
debug = True

class Item():
	def __init__(self, mod="minecraft", item, count=1):
		self.mod = mod
		self.item = item
		self.count = count

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

	def get_required_items(self, count=1):
		required_items = []
		for item in self.items:
			required_items.append(Item(item.get_mod(), item.get_item(), item.get_count()*count))

		return required_items

	def output(self):
		message = self.crafting_method.title()
		if self.items != []:
			message += self.items
		else:
			message += self.result

		print(message)
				
def dprint(text, end="\n"):
	if debug:
		print(text, end=end)
	return text

if __name__ == "__main__":
	pass
