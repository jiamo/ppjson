import json
from ppjson import ppjson


def test_number():
    assert json.loads("1") == 1 == ppjson.loads("1")
    assert json.loads('1') == 1 == ppjson.loads('1')
    assert json.loads('1.1') == 1.1 == ppjson.loads('1.1')
    assert ppjson.loads("1337.1337") == 1337.1337


def test_dict():
    assert json.loads('{"1": 1}') == {"1": 1} == ppjson.loads('{"1": 1}')
    assert json.loads('{"1": {"1": 1}}') == {"1": {"1": 1}} \
           == ppjson.loads('{"1": {"1": 1}}')
    assert json.loads('{"1": {"1": [1]}}') == {"1": {"1": [1]}} == ppjson.loads(
        '{"1": {"1": [1]}}')



