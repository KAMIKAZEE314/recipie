import pytest
from main import get_nodes_at_depth, get_node_at_path

def test_get_nodes_at_depth():
	node_tree = {
		"a0": {"children": {
				"a1": {},
				"b1": {"children":{
						"a2": {},
						"b2": {}
					}
				},
				"c1": {"children": {
						"c2": {"children": {
								"a3": {}
							}
						}	
					}
				}
			}
		}
	}

	assert get_nodes_at_depth(4, node_tree) == []
	assert get_nodes_at_depth(3, node_tree) == [("a3", ["a0", "c1", "c2"], {})]
	assert get_nodes_at_depth(2, node_tree) == [("a2", ["a0", "b1"], {}), ("b2", ["a0", "b1"], {}), ("c2", ["a0", "c1"], {"children": {"a3": {}}})]
	assert get_nodes_at_depth(1, node_tree) == [("a1", ["a0"], {}), ("b1", ["a0"], {"children":{"a2": {}, "b2": {}}}), ("c1", ["a0"], {"children": {"c2": {"children":{"a3":{}}}}})]
	assert get_nodes_at_depth(0, node_tree) == [("a0", [], node_tree["a0"])]
	assert get_nodes_at_depth(-1, node_tree) == []

def test_get_node_at_depth():
	node_tree = {
		"a0": {"children": {
				"a1": {},
				"b1": {"children":{
						"a2": {},
						"b2": {}
					}
				},
				"c1": {"children": {
						"c2": {"children": {
								"a3": {}
							}
						}	
					}
				}
			}
		}
	}

	assert get_node_at_path(node_tree, ["a0", "b1"]) == {"children":{"a2":{}, "b2":{}}}
