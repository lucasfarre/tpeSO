import json

def toJson(o):
    return json.dumps(o, sort_keys=True, indent=4, separators=(',', ':'), default=lambda o: o.__dict__)

def fromJson(j):
    return json.loads(j)