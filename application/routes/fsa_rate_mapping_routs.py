
from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer

from application.response_builder import ResponseBuilder
from domain.dtos.fsa_rate_mapping_dtos import *
from domain.services.fsa_rate_mapping_srv import *
from infrastructure.repositories.fsa_rate_mapping_repo import FsaRateMappingRepository
from aws_lambda_powertools.event_handler.api_gateway import Router


tracer = Tracer()
logger = Logger()
router = Router()
repo = FsaRateMappingRepository()
service = FsaRateMappingService(repo)

@router.post("/")
@tracer.capture_method
def create():
    parsed_payload: FsaRateMappingSetDto = parse(event=router.current_event.body, model=FsaRateMappingSetDto)
    service.create(parsed_payload)
    return ResponseBuilder.build(parsed_payload.destination_fsa)

@router.put("/")
@tracer.capture_method
def create():
    parsed_payload: FsaRateMappingSetDto = parse(event=router.current_event.body, model=FsaRateMappingSetDto)
    service.set(parsed_payload)
    return ResponseBuilder.build(parsed_payload.destination_fsa)

@router.get("/")
@tracer.capture_method
def get_all():
    dtos = service.get_all()
    return ResponseBuilder.build(dtos)

@router.get("/destination_fsa/<destination_fsa>/origin_zone/<origin_zone>")
@tracer.capture_method
def get_by_origin(destination_fsa:str,origin_zone:str):
    dto = service.get(destination_fsa,origin_zone)
    return ResponseBuilder.build(dto)
    

