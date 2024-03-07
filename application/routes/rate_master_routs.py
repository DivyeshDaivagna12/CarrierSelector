
from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer

from application.response_builder import ResponseBuilder
from domain.dtos.rate_master_dtos import *
from domain.services.rate_master_srv import *
from aws_lambda_powertools.event_handler.api_gateway import Router


tracer = Tracer()
logger = Logger()
router = Router()
service = RateMasterService()

@router.get("/")
@tracer.capture_method
def get_rate():
    parsed_payload: RateMasterSetDto = parse(event=router.current_event.body, model=RateMasterSetDto)
    dtos = service.get_pricing(parsed_payload)
    return ResponseBuilder.build(dtos)
    


    

