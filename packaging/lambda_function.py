from packaging.packaging_repo import *
from packaging.packaging_srv import *
from packaging.packaging_dtos import *
from packaging.packaging_ent import *
from common_methods.response_builder import ResponseBuilder

repo = PackagingRepository()
service = PackagingService(repo)

def lambda_handler(event, context)->any:
    
    request =  event["body"]
    path = event['path']
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']
    
    if  http_method == "PUT" and path == '':
        parsed_payload: PackagingSetDto = parse(event=request, model=PackagingSetDto)
        service.set(parsed_payload)
        return ResponseBuilder.build(parsed_payload.id)
    
    elif  http_method == "GET" and path == '/':
        dtos = service.get_all()
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "GET" and path == '/<id>':
        dto = service.get((event["queryStringParameters"]["id"]))
        return   ResponseBuilder.build(dto)
    else:
        return { "statusCode": 404, "body": "NotFound" }
    
