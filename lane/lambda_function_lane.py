from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer

from application.response_builder import ResponseBuilder
from lane.lane_dtos import *
from domain.services.lane_srv import *
from infrastructure.repositories.lane_repo import LaneRepository
from aws_lambda_powertools.event_handler.api_gateway import Router

repo = LaneRepository()
service = LaneService(repo)

def lambda_handler(event, context)->any:
    resquest =  event["body"]
    path = event['path']
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']

    if http_method == "GET" and path == '/carrier/<carrierId>':
        dtos = service.get_by_carrierId(event["rawQueryString"])
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "GET" and path == '/<id>':
        dtos = service.get(event["rawQueryString"])
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