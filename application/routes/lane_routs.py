
from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer

from application.response_builder import ResponseBuilder
from domain.dtos.lane_dtos import *
from domain.services.lane_srv import *
from infrastructure.repositories.lane_repo import LaneRepository
from aws_lambda_powertools.event_handler.api_gateway import Router


tracer = Tracer()
logger = Logger()
router = Router()
repo = LaneRepository()
service = LaneService(repo)

@router.post("/")
@tracer.capture_method
def create():
    parsed_payload: LaneSetDto = parse(event=router.current_event.body, model=LaneSetDto)
    service.create(parsed_payload)
    return ResponseBuilder.build(parsed_payload.id)

@router.put("/")
@tracer.capture_method
def update():
    parsed_payload: LaneSetDto = parse(event=router.current_event.body, model=LaneSetDto)
    service.update(parsed_payload)
    return ResponseBuilder.build(parsed_payload.id)

@router.get("/carrier/<carrierId>")
@tracer.capture_method
def get_by_carrierId(carrierId: str):
    dtos = service.get_by_carrierId(carrierId)
    return ResponseBuilder.build(dtos)

@router.get("/<id>")
@tracer.capture_method
def get_by_id(id:str):
    dto = service.get(id)
    return   ResponseBuilder.build(dto)
    

