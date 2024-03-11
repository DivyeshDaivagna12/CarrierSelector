
from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer

from application.response_builder import ResponseBuilder
from domain.dtos.skid_spacing_dtos import *
from domain.services.skid_spacing_srv import *
from infrastructure.repositories.skid_spacing_repo import SkidSpacingRepository
from aws_lambda_powertools.event_handler.api_gateway import Router


tracer = Tracer()
logger = Logger()
router = Router()
repo = SkidSpacingRepository()
service = SkidSpacingService(repo)

@router.put("/")
@tracer.capture_method
def create():
    parsed_payload: SkidSpacingSetDto = parse(event=router.current_event.body, model=SkidSpacingSetDto)
    service.set(parsed_payload)
    return ResponseBuilder.build(parsed_payload.skid_space)

@router.get("/")
@tracer.capture_method
def get_all():
    dtos = service.get_all()
    return ResponseBuilder.build(dtos)

@router.get("/<id>")
@tracer.capture_method
def get_by_id(id:str):
    dto = service.get(id)
    return   ResponseBuilder.build(dto)
    
