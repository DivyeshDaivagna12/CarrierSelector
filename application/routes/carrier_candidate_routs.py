
from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer

from application.response_builder import ResponseBuilder
from domain.dtos.carrier_candidate_dtos import *
from domain.services.carrier_candidate_srv import *
from aws_lambda_powertools.event_handler.api_gateway import Router


tracer = Tracer()
logger = Logger()
router = Router()
service = CarrierCandidateService()

@router.get("/")
@tracer.capture_method
def get():
    parsed_payload: CarrierCandidateSetDto = parse(event=router.current_event.body, model=CarrierCandidateSetDto)
    dto = service.get_candidates(parsed_payload)
    return ResponseBuilder.build(dto)

    

