from botocore import awsrequest, credentials, signers, auth
import requests

import json, copy, datetime


#EXAMPLE: Request that invoke the lambda function `example1` with AWS_IAM authentication.


endpoint_url = "https://lambda.us-east-1.amazonaws.com"


request_dict_body = {"num1": 15, "num2": 20}
request_dict = {
    'method': "POST", 
    'url_path': '/2015-03-31/functions/example1/invocations', 
    'body': json.dumps(request_dict_body),
    'headers': {},
    'query_string': {}
    }

context = {
    'signing': {
        'auth_as': 'header',       #can only have one of two values: "header" or "query"
        'service': 'lambda', 
        'region': 'us-east-1',
        "expires": 86400}
        }


def makeRequestWithAuth(endpoint_url, request_dict, context):

  if context['signing']['auth_as'] not in ['header', 'query']:
      #raise Exception("'auth_as' param can only have one of these values ['header', 'query']")
      error_message = "'auth_as' param can only have one of these values ['header', 'query']"

      return { "statusCode": 400, "body": json.dumps(error_message)}

  awsrequest.prepare_request_dict(request_dict, endpoint_url, context)
  request_object = awsrequest.create_request_object(request_dict)
   
  auth_as = request_object.context['signing']['auth_as']
  region_name = request_object.context['signing']['region']
  service_name = request_object.context['signing']['service']
  expires = request_object.context['signing']['expires']    #Expiration only works for Auth as query string and for some specific services (e.g S3)
                                                                                    
  access_key = "iam-user-access-key"                                                     
  secret_key = "iam-user-secret-key"                        
  _credentials = credentials.Credentials(access_key, secret_key)


  if auth_as == "header":
    sigv4 = auth.SigV4Auth(_credentials, service_name, region_name)
  elif auth_as == "query":
    sigv4 = auth.SigV4QueryAuth(_credentials, service_name, region_name, expires)

  #Add this block of code if you want to see the canonical request, which will be used to create the STRING TO SIGN

  import datetime

  datetime_now = datetime.datetime.utcnow()
  request_object.context['timestamp'] = datetime_now.strftime('%Y%m%dT%H%M%SZ')

  sigv4._modify_request_before_signing(request_object)
  canonical_request = sigv4.canonical_request(request_object)
  print("-----------------CANONICAL REQUEST-----------------\n",canonical_request, sep="")

  #--------------------End of block------------------------

  sigv4.add_auth(request_object)
  print('\n\n-----------------REQUEST WITH AUTH DATA-----------------\n',f'{request_object.method}\n{request_object.url}\n{request_object.params}\n{request_object.headers}\n{request_object.body}', sep="")

  method = request_object.method
  url = request_object.url
  data = request_object.body
  headers = request_object.headers

  print("dataaaaaaaa",request_object.data)
  response = requests.request(method, url, headers=headers, data=data)
  print(f'\n\n-----------------RESPONSE-----------------\n', response.text, sep="")
  return response

makeRequestWithAuth(endpoint_url, request_dict, context)