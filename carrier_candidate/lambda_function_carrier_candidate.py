from dataclasses import asdict, is_dataclass
from application.response_builder import ResponseBuilder
from domain.dtos.carrier_candidate_dtos import *
from domain.services.carrier_candidate_srv import *
from aws_lambda_powertools.event_handler.api_gateway import Router

service = CarrierCandidateService()

def lambda_handler(event, context)->any:
    resquest =  event["body"]
    path = event['path']
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']

    if http_method == "GET" and path == '/':
        dtos = service.get_all()
        return ResponseBuilder.build(dtos)