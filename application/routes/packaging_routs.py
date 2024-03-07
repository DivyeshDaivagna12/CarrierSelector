
from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer

from application.response_builder import ResponseBuilder
from domain.dtos.packaging_dtos import *
from domain.services.packaging_srv import *
from infrastructure.repositories.packaging_repo import PackagingRepository
from aws_lambda_powertools.event_handler.api_gateway import Router


tracer = Tracer()
logger = Logger()
router = Router()
repo = PackagingRepository()
service = PackagingService(repo)

@router.put("/")
@tracer.capture_method
def create():
    parsed_payload: PackagingSetDto = parse(event=router.current_event.body, model=PackagingSetDto)
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
    

