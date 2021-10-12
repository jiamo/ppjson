import simplejson as json
from ppjson import ppjson


# def test_array_null_empty():
#     assert json.loads('[null, 1, "1", {}]') == ppjson.loads('[null, 1, "1", {}]')

def test_array_true():
    assert json.loads('[true]') == ppjson.loads('[true]')

def test_array():
    assert json.loads('[1]') == ppjson.loads('[1]')

def test_dict():
    assert json.loads('{"1":1}') == ppjson.loads('{"1":1}')

def test_empty_dict():
    assert json.loads('{ }') == ppjson.loads('{ }')

def test_number():
    assert json.loads("1") == 1 == ppjson.loads("1")
    assert json.loads('1') == 1 == ppjson.loads('1')
    assert json.loads('1.1') == 1.1 == ppjson.loads('1.1')



