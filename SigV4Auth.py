from botocore import signers, awsrequest, credentials, hooks, model
import requests

import json, datetime, copy

#Define the request to be signed with the endpoint_url, request_dict, context (sig. version, region, service name)

endpoint_url = "https://dvf7otbp6ofm5yrz6obimom7cq0rdhsq.lambda-url.sa-east-1.on.aws/"

request_dict = {
    'method': "POST", 
    'url_path': '/', 
    'body': {'num1': 10, 'num2': 11},
    'headers': {},
    'query_string': {}
    }

context = {
    'signing': {
        'signature_version': 'v4-query', #"v4" for sending the authorization as request headers or "v4-query" for sending it as query params in the URL
        'signing_name': 'lambda', 
        'region': 'sa-east-1'}
        }

#Instantiate the AWSRequest class with `create_request_object` method

awsrequest.prepare_request_dict(request_dict, endpoint_url, context)
request_object = awsrequest.create_request_object(request_dict)

#Read some values from the request context

region_name = request_object.context['signing']['region']
signing_name = request_object.context['signing']['signing_name']
service_id = model.ServiceId(signing_name)
signature_version = request_object.context['signing']['signature_version']

#Add the IAM user credentials. If a IAM role is used instead, you must add the `session_token`.
access_key = "AKIAT2PB64KJXH353H73"                                                        
secret_key = "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"                                    
_credentials = credentials.Credentials(access_key, secret_key)

#You must use this as a param in the next instance creation.
event_emitter = hooks.HierarchicalEmitter()

signer = signers.RequestSigner(service_id, region_name, signing_name, signature_version, _credentials, event_emitter)
signerv4 = signer.get_auth_instance(signing_name, region_name)


#If you want to get the canonical request to be signed, do the following
request_object_copy = copy.deepcopy(request_object)

datetime_now = datetime.datetime.utcnow()
request_object_copy.context['timestamp'] = datetime_now.strftime('%Y%m%dT%H%M%SZ')

signerv4._modify_request_before_signing(request_object_copy)
print(signerv4.canonical_request(request_object_copy))

#Sign the request
signerv4.add_auth(request_object)

#Show the updated request with the authentication data
print(f'{request_object.method}\n{request_object.url}\n{request_object.params}\n{request_object.headers}\n{request_object.data}')

method = request_object.method
url = request_object.url
data = request_object.data
headers = request_object.headers

#Make the call with the signature added
response = requests.request(method, url, headers=headers, data=data)
print(response.text)