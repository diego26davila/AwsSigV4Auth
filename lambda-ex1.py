import json, base64
from urllib.parse import parse_qs

def lambda_handler(event, context):
    
    print(json.dumps(event))
    
    body = event.get("body")
    query_string = event.get("queryStringParameters")

    if body is not None:
        
        if event['isBase64Encoded']:
            payload = json.loads(base64.b64decode(event['body']))
        else:
            payload = json.loads(event['body'])
            
        a = payload['num1']
        b = payload['num2']
    
    elif query_string is not None:
        
        a = int(query_string['num1'])
        b = int(query_string['num2'])
        
    else:
        
        if not hasattr(event, "items"):
            _event = parse_qs(event)
            
            a = _event['num1'][0]
            a = _event['num1'][0]
            
        a = event['num1']
        b = event['num2']
        
    response = {
        "sum": a + b,
        "product": a * b
    }
    
    return {
        'statusCode': 200,
        'body': response
    }