
from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer

from application.response_builder import ResponseBuilder
from domain.dtos.offering_dtos import *
from domain.services.offering_srv import *
from infrastructure.repositories.offering_repo import OfferingRepository
from aws_lambda_powertools.event_handler.api_gateway import Router


tracer = Tracer()
logger = Logger()
router = Router()
repo = OfferingRepository()
service = OfferingService(repo)

@router.put("/")
@tracer.capture_method
def create():
    parsed_payload: OfferingSetDto = parse(event=router.current_event.body, model=OfferingSetDto)
    service.set(parsed_payload)
    return ResponseBuilder.build(parsed_payload.id)

@router.get("/<id>/filter/<filter>")
@tracer.capture_method
def get_by_id(id:str, filter: str):
    dtos = service.get_by_id(id, filter)
    return   ResponseBuilder.build(dtos)

@router.get("/carrier/<carrierId>")
@tracer.capture_method
def get_by_carrierId(carrierId:str):
    dtos = service.get_by_carrierId(carrierId)
    return   ResponseBuilder.build(dtos)
    

