from common_methods.response_builder import ResponseBuilder
from lane_dtos import *
from lane_srv import *
from lane_repo import LaneRepository

repo = LaneRepository()
service = LaneService(repo)

def lambda_handler(event, context)->any:
    resquest =  event["body"]
    path = event['path']
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']

    if http_method == "GET" and path == '/carrier/<carrierId>':
        dtos = service.get_by_carrierId(event["queryStringParameters"]["carrierId"])
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "GET" and path == '/<id>':
        dtos = service.get(event["queryStringParameters"]["id"])
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "PUT" and path == '/':
        dto = LaneSetDto()
        dto.__dict__ = resquest
        service.update(dto)
        return ResponseBuilder.build("Updated successfully")
    
    elif  http_method == "POST" and path == '/':
        dto = LaneSetDto()
        dto.__dict__ = resquest
        service.create(dto)
        return ResponseBuilder.build("Saved successfully")
    else:
        return { "statusCode": 404, "body": "NotFound" }