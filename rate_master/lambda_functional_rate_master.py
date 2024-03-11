from ast import parse
from application.response_builder import ResponseBuilder
from rate_master.rate_master_dtos import RateMasterSetDto
from rate_master.rate_master_srv import RateMasterService
from rate_master.rate_master_dtos import *
from rate_master_srv import *

rs = RateMasterService()

def lambda_handler(event, context)->any:
     
     request =  event["body"]
     path = event['path']
     http_method = event['requestContext']['http']['method']
     path = event['requestContext']['http']['path']

     if http_method == "GET" and path == '/':
          parsed_payload: RateMasterSetDto = parse(event=request.current_event.body, model=RateMasterSetDto)
          dtos = rs.get_pricing(parsed_payload)
          return ResponseBuilder.build(dtos)
     
     else:
          return { "statusCode": 404, "body": "NotFound" }
