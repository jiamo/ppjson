import simplejson as json
from ppjson import ppjson



def test_empty_dict():
    assert json.loads('{}') == ppjson.loads('{}')



