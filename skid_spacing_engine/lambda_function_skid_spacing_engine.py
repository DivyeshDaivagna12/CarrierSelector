from skid_spacing_engine_dtos import *
from skid_spacing_engine_srv import *
from application.response_builder import ResponseBuilder

ss = SkidSpacingEngineService()

def lambda_handler(event, context)->any:
     
     request =  event["body"]
     path = event['path']
     http_method = event['requestContext']['http']['method']
     path = event['requestContext']['http']['path']

     if http_method == "GET" and path == '/':
          parsed_payload: SkidSpacingEngineRequestDto = parse(event=request.current_event.body, model=SkidSpacingEngineRequestDto)
          dtos = ss.get_skids_count(parsed_payload)
          return ResponseBuilder.build(dtos)
     
     else:
          return { "statusCode": 404, "body": "NotFound" }
