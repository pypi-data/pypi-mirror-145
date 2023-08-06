import base64
import json

def convert(event):
    raw_str = event['body']
    if '{' in raw_str:
        return json.loads(raw_str)
    b64_bytes = base64.b64decode(raw_str)
    json_str = b64_bytes.decode('utf-8')
    req_body = json.loads(json_str)
    return req_body

