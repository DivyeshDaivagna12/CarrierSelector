
from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer

from application.response_builder import ResponseBuilder
from domain.dtos.carrier_selection_dtos import *
from domain.services.carrier_selection_srv import *
from aws_lambda_powertools.event_handler.api_gateway import Router


tracer = Tracer()
logger = Logger()
router = Router()
service = CarrierSelectionService()



@router.get("/")
@tracer.capture_method
def get_final_carrier():
    parsed_payload: CarrierSelectionSetDto = parse(event=router.current_event.body, model=CarrierSelectionSetDto)
    dtos = service.selection(parsed_payload)
    return ResponseBuilder.build(dtos)
    

