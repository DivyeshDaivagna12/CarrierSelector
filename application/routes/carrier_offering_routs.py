
from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer

from application.response_builder import ResponseBuilder
from domain.dtos.carrier_offering_dtos import *
from domain.services.carrier_offering_srv import *
from infrastructure.repositories.carrier_offering_repo import CarrierOfferingRepository
from aws_lambda_powertools.event_handler.api_gateway import Router


tracer = Tracer()
logger = Logger()
router = Router()
repo = CarrierOfferingRepository()
service = CarrierOfferingService(repo)

@router.get("/<carrierId>")
@tracer.capture_method
def get_by_carrierId(carrierId:str):
    dtos = service.get_by_carrierId(carrierId)
    return   ResponseBuilder.build(dtos)
    

