from handler import items
import json
import base64


def b64_to_dict(s: str) -> dict:
    p = base64.b64decode(s).decode()
    return json.loads(p)


def lambda_handler(event, context):
    try:
        req = b64_to_dict(event['body'])
        _items = items(req)
        return {
            "status": 200,
            "data": _items
        }
    except Exception as e:
        return {
            "status": 500,
            "error": str(e)
        }
