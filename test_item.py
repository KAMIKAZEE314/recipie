import pytest
from main import Item

def test_Item_getters():
	item = Item("OaK plAnk", "mInEcRAft ", 24)
	assert item.get_mod() == "minecraft"
	assert item.get_item() == "oak_plank"
	assert item.get_count() == 24

def test_Item_json():
	item = Item("OaK plAnk", "mInEcRAft ", 24)
	assert item.json_form() == {"item": "oak_plank", "mod": "minecraft", "count": 24}

def test_Item_from_json():
	item = Item("OaK plAnk", "mInEcRAft ", 24)
	json_form = {"item": "oak_plank", "mod": "minecraft", "count": 24}
	assert Item.from_json(json_form) == item
