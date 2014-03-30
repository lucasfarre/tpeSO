import json
from collections import namedtuple
from flight import *


def toJson(o):
    return json.dumps(o, sort_keys=True, indent=4, separators=(',', ':'))

def fromJson(j):
    return json.loads(j)
# def test(o):
# #     lambda o: o.__dict__
#     if isinstance(o, tuple):
#         return o._asdict()
#     return o.__dict__
# 
# def toJson(o):
#     return json.dumps(o, sort_keys=True, indent=4, separators=(',', ':'), default=lambda o: o.__dict__)
# 
# def json_object_hook(d):
#     return namedtuple('JsonObject', d.keys())(*d.values())
# 
# def fromJson(data):
#     return json.loads(data, object_hook=json_object_hook)
# 
# def jsonObjectAsDict(obj):
#     if isinstance(obj, list):
#         l = []
#         for e in obj:
#             l.append(jsonObjectAsDict(e))
#         return l
#     if isinstance(obj, tuple):
#         d = dict() 
#         for key in obj._fields:
#             value = getattr(obj, key)
#             if isinstance(value, tuple) or isinstance(value, list):
#                 d[key] = jsonObjectAsDict(value)
#             else:
#                 d[key] = value
#         return d

# TYPES = { 'Flight': Flight,
#           'Aircraft': Aircraft,
#           'Seat' : Seat,
#           'Passenger' : Passenger }


# class CustomTypeEncoder(json.JSONEncoder):
#     """A custom JSONEncoder class that knows how to encode core custom
#     objects.
# 
#     Custom objects are encoded as JSON object literals (ie, dicts) with
#     one key, '__TypeName__' where 'TypeName' is the actual name of the
#     type to which the object belongs.  That single key maps to another
#     object literal which is just the __dict__ of the object encoded."""
# 
#     def default(self, obj):
#         if isinstance(obj, TYPES.values()):
#             key = '__%s__' % obj.__class__.__name__
#             return { key: obj.__dict__ }
#         return json.JSONEncoder.default(self, obj)


# def CustomTypeDecoder(dct):
#     if len(dct) == 1:
#         type_name, value = dct.items()[0]
#         type_name = type_name.strip('_')
#         if type_name in TYPES:
#             return TYPES[type_name].from_dict(value)
#     return dct


# class MyDecoder(json.JSONDecoder):
#     
#     def __init__(self):
#         json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)
# 
#     def dict_to_object(self, d):
#         if '__class__' in d:
#             class_name = d.pop('__class__')
#             module_name = d.pop('__module__')
#             module = __import__(module_name)
#             print 'MODULE:', module
#             class_ = getattr(module, class_name)
#             print 'CLASS:', class_
#             args = dict( (key.encode('ascii'), value) for key, value in d.items())
#             print 'INSTANCE ARGS:', args
#             inst = class_(**args)
#         else:
#             inst = d
#         return inst

 
# def fromJson(data):
#     return CustomTypeDecoder().decode(data)
