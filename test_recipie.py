import pytest
from main import Recipie, Item

def test_Recipie_output():
	recipie = Recipie([Item("coal"), Item("stick")], Item("torch", count=4), crafting_method="craft")
	assert recipie.output_form(5) == "Craft 8 Torch"

def test_Recipie_required_items():
	recipie = Recipie([Item("coal"), Item("stick")], Item("torch", count=4), crafting_method="craft")

	required_items = recipie.get_required_items(5)
	passed = True
	for item1 in required_items:
		broken = False
		for item2 in required_items:
			if item1 == item2:
				broken = True
				break
		if not broken:
			passed = False
			break
	assert passed

def test_Recipie_json():
	recipie = Recipie([Item("coal"), Item("stick")], Item("torch", count=4), crafting_method="craft")
	json_form = recipie.json_form()
	assert json_form == {"crafting_method": "craft", "result": Item("torch", count=1).json_form(), "dependencies": None, "items": [Item("coal", count=0.25).json_form(), Item("stick", count=0.25).json_form()]}
