
from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer

from application.response_builder import ResponseBuilder
from domain.dtos.time_definite_dtos import *
from domain.services.time_definite_srv import *
from infrastructure.repositories.time_definite_repo import TimeDefiniteRepository
from aws_lambda_powertools.event_handler.api_gateway import Router


tracer = Tracer()
logger = Logger()
router = Router()
repo = TimeDefiniteRepository()
service = TimeDefinteService(repo)

@router.put("/")
@tracer.capture_method
def create():
    parsed_payload: TimeDefiniteSetDto = parse(event=router.current_event.body, model=TimeDefiniteSetDto)
    service.set(parsed_payload)
    return ResponseBuilder.build(parsed_payload.id)

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
    

