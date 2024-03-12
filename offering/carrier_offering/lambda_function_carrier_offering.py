from application.response_builder import ResponseBuilder
from carrier_offering_dtos import *
from carrier_offering_srv import *
from carrier_offering_repo import CarrierOfferingRepository
from aws_lambda_powertools.event_handler.api_gateway import Router

repo = CarrierOfferingRepository()
service = CarrierOfferingService(repo)

def lambda_handler(event, context)->any:
    resquest =  event["body"]
    path = event['path']
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']
    
    if http_method == "GET" and path == '/<carrierId>':
        dtos = service.get_by_carrierId(event["queryStringParameters"]["carrierId"])
        return ResponseBuilder.build(dtos)
    else:
        return { "statusCode": 404, "body": "NotFound" }