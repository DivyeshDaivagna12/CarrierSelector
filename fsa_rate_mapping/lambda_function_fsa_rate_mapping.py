# Standard library imports
from ast import parse

# Local application imports
from fsa_rate_mapping.response_builder import ResponseBuilder
from fsa_rate_mapping_dtos import *
from fsa_rate_mapping_srv import *
from fsa_rate_mapping_repo import FsaRateMappingRepository

repo = FsaRateMappingRepository()
service = FsaRateMappingService(repo)

def lambda_handler(event, context)->any:
    request =  event["body"]
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']

    if  http_method == "POST" and path == '/':
        parsed_payload: FsaRateMappingSetDto = parse(event=request, model=FsaRateMappingSetDto)
        service.create(parsed_payload)
        return ResponseBuilder.build(parsed_payload.destination_fsa)
        
    elif  http_method == "PUT" and path == '/':
        parsed_payload: FsaRateMappingSetDto = parse(event=request, model=FsaRateMappingSetDto)
        service.set(parsed_payload)
        return ResponseBuilder.build(parsed_payload.destination_fsa)
    
    elif  http_method == "GET" and path == '/':
          dtos = service.get_all()
          return ResponseBuilder.build(dtos)

    
    elif  http_method == "GET" and path == '/destination_fsa/<destination_fsa>/origin_zone/<origin_zone>':
          destination_fsa = event["queryStringParameters"]["destination_fsa"]
          origin_zone = event["queryStringParameters"]["origin_zone"]
          dto = service.get(destination_fsa,origin_zone)
          return ResponseBuilder.build(dto)
    
    else:
        return { "statusCode": 404, "body": "NotFound" }
    
