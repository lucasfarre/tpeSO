import json
from collections import namedtuple

def toJson(o):
    return json.dumps(o, sort_keys=True, separators=(',', ':'))

def toPrettyJson(o):
    return json.dumps(o, sort_keys=True, indent=4, separators=(',', ':'))

def fromJson(j):
    return json.loads(j)

def jsonPrettifier(j):
	return toPrettyJson(fromJson(j))
