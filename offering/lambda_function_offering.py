from offering.offering_dtos import *
from offering.offering_srv import *
from offering_repo import OfferingRepository
from application.response_builder import ResponseBuilder

repo = OfferingRepository()
service = OfferingService(repo)

def lambda_handler(event, context)->any:
    resquest =  event["body"]
    path = event['path']
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']

    if http_method == "PUT" and path == '/':
        service.set()
        return ResponseBuilder.build("Updated successfully")
    
    elif  http_method == "GET" and path == '/<id>/filter/<filter>':
        dtos = service.get_by_id(event["queryStringParameters"]["id"], 
                                 event["queryStringParameters"]["filter"])
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "GET" and path == '/carrier/<carrierId>':
        dtos = service.get_by_carrierId(event["queryStringParameters"]["carrierId"])
        return ResponseBuilder.build(dtos)
    else:
        return { "statusCode": 404, "body": "NotFound" }
    