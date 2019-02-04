import json


def read_google_creds():
    with open('./credentials/googlekey.json', 'r') as credfile:
        key = credfile.read()
        serialized = json.dumps(json.loads(key))
    return serialized
