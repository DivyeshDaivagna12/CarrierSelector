from service_dtos import *
from service_srv import *
from service_repo import *
from common_methods.response_builder import ResponseBuilder

repo = ServiceRepository()
service = ServiceService(repo)

def lambda_handler(event, context)->any:
    resquest =  event["body"]
    path = event['path']
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']

    if http_method == "GET" and path == '/':
        dtos = service.get_all()
        return ResponseBuilder.build(dtos)  
    
    elif  http_method == "GET" and path == '/<id>':
        dtos = service.get(event["queryStringParameters"]["id"])
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "PUT" and path == '/':
        dto = ServiceSetDto()
        dto.__dict__ = resquest
        service.set(dto)
        return ResponseBuilder.build("Updated successfully")
    
    elif  http_method == "POST" and path == '/':
        dto = ServiceSetDto()
        dto.__dict__ = resquest
        service.add_system_services(dto)
        return ResponseBuilder.build("Saved successfully")
    
    else:
        return { "statusCode": 404, "body": "NotFound" }

