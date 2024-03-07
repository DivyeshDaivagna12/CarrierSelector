
from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from application.response_builder import ResponseBuilder
from domain.dtos.zone_dtos import *
from domain.services.zone_srv import *
from infrastructure.repositories.zone_repo import *
from aws_lambda_powertools.event_handler.api_gateway import Router


tracer = Tracer()
logger = Logger()
router = Router()
repo = ZoneRepository()
zs = ZoneService(repo)

@router.get("/")
@tracer.capture_method
def get_all_zones():
    dtos = zs.get_all_zones()
    return ResponseBuilder.build(dtos)

@router.get("/address/<address>")
@tracer.capture_method
def get_zones_for_address(address:str):
    dtos = zs.get_zones_for_address(address)
    return ResponseBuilder.build(dtos)

@router.get("/status")
@tracer.capture_method
def get_zones_status():
    dtos = zs.get_zones_status()
    return ResponseBuilder.build(dtos)
    

@router.put("/update")
@tracer.capture_method
def update_operation():
    zs.update_operation()
    return ResponseBuilder.build("Updated successfully")
    

@router.get("/qgis-screen")
@tracer.capture_method
def get_stream_url():
    user_email = router.context.get('current_user',"")
    dtos = zs.get_stream_url(user_email)
    return ResponseBuilder.build(dtos)