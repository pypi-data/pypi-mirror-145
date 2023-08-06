from pickle import loads, dump, dumps

def encode(object: any):
    if type(object) == str:
        return dumps(object)
    else:
        return dumps(object)

def decode(data: bytes):
    return loads(data)