
from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer

from application.response_builder import ResponseBuilder
from domain.dtos.carrier_product_dtos import *
from domain.services.carrier_product_srv import *
from infrastructure.repositories.carrier_product_repo import CarrierProductRepository
from aws_lambda_powertools.event_handler.api_gateway import Router


tracer = Tracer()
logger = Logger()
router = Router()
repo = CarrierProductRepository()
service = CarrierProductService(repo)

@router.post("/")
@tracer.capture_method
def create():
    parsed_payload: CarrierProductSetDto = parse(event=router.current_event.body, model=CarrierProductSetDto)
    service.create(parsed_payload)
    return ResponseBuilder.build(parsed_payload.product)

@router.put("/")
@tracer.capture_method
def create():
    parsed_payload: CarrierProductSetDto = parse(event=router.current_event.body, model=CarrierProductSetDto)
    service.set(parsed_payload)
    return ResponseBuilder.build(parsed_payload.product)

@router.get("/<carrier>")
@tracer.capture_method
def get_all( carrier: str):
    dtos = service.get_all(carrier)
    return ResponseBuilder.build(dtos)

@router.get("/<carrier>/<product>")
@tracer.capture_method
def get_by_carrier_product(carrier: str, product: str):
    dto = service.get(carrier, product)
    return   ResponseBuilder.build(dto)
    

