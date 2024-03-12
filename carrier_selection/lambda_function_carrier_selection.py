from dataclasses import asdict, is_dataclass
from application.response_builder import ResponseBuilder
from carrier_selection_dtos import *
from carrier_selection_srv import *
from aws_lambda_powertools.event_handler.api_gateway import Router

service = CarrierSelectionService()

def lambda_handler(event, context):
    resquest =  event["body"]
    path = event['path']
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']
    
    if http_method == 'GET':
        parsed_payload: CarrierSelectionSetDto = parse(event=resquest, model=CarrierSelectionSetDto)
        dtos = service.selection(parsed_payload)
        return ResponseBuilder.build(dtos)
    else:
        return ResponseBuilder.build_error("Invalid HTTP Method")