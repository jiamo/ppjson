import simplejson as json
from ppjson import ppjson



def test_array_null():
    assert json.loads('[null, 1, "1"]') == ppjson.loads('[null, 1, "1"]')

def test_array_null_empty():
    assert json.loads('[null, 1, "1", {}]') == ppjson.loads('[null, 1, "1", {}]')



