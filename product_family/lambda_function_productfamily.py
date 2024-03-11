from product_family_dtos import *
from product_family_srv import *
from product_family_repo import *
from application.response_builder import ResponseBuilder

repo = ProductFamilyRepository()
service = ProductFamilyService(repo)

def lambda_handler(event, context)->any:
    
    resquest =  event["body"]
    path = event['path']
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']
    
    if http_method == "PUT" and path == '':
        parsed_payload: ProductFamilySetDto = parse(event=resquest, model=ProductFamilySetDto)
        service.set(parsed_payload)
        return ResponseBuilder.build(parsed_payload.id)
    
    elif  http_method == "GET" and path == '':
        dtos = service.get_all()
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "GET" and path == '/<id>':
        dto = service.get(event["rawQueryString"])
        return   ResponseBuilder.build(dto)
    
    else:
        return { "statusCode": 404, "body": "NotFound" }