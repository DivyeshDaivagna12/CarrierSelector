
from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer

from application.response_builder import ResponseBuilder
from domain.dtos.skid_spacing_engine_dtos import *
from domain.services.skid_spacing_engine_srv import *
from aws_lambda_powertools.event_handler.api_gateway import Router


tracer = Tracer()
logger = Logger()
router = Router()
service = SkidSpacingEngineService()

@router.get("/")
@tracer.capture_method
def get_skids_count():
    parsed_payload: SkidSpacingEngineRequestDto = parse(event=router.current_event.body, model=SkidSpacingEngineRequestDto)
    dtos = service.get_skids_count(parsed_payload)
    return ResponseBuilder.build(dtos)

# @router.get("/")
# @tracer.capture_method
# def get_all():
#     dtos = service.get_all()
#     return ResponseBuilder.build(dtos)

# @router.get("/<id>")
# @tracer.capture_method
# def get_by_id(id:str):
#     dto = service.get(id)
#     return   ResponseBuilder.build(dto)
    

