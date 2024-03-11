from dataclasses import asdict, is_dataclass
import json
from application.response_builder import ResponseBuilder
from carrier_offering.carrier_offering_dtos import *
from domain.services.carrier_offering_srv import *
from infrastructure.repositories.carrier_offering_repo import CarrierOfferingRepository
from aws_lambda_powertools.event_handler.api_gateway import Router

repo = CarrierOfferingRepository()
service = CarrierOfferingService(repo)

def lambda_handler(event, context)->any:
    resquest =  event["body"]
    path = event['path']
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']
    
    if http_method == "GET" and path == '/<carrierId>':
        dtos = service.get_by_carrierId(event["rawQueryString"])
        return ResponseBuilder.build(dtos)
    else:
        return { "statusCode": 404, "body": "NotFound" }