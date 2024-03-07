
from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer

from application.response_builder import ResponseBuilder
from domain.dtos.customer_pricing_dtos import *
from domain.services.customer_pricing_srv import *
from infrastructure.repositories.customer_pricing_repo import CustomerPricingRepository
from aws_lambda_powertools.event_handler.api_gateway import Router


tracer = Tracer()
logger = Logger()
router = Router()
repo = CustomerPricingRepository()
service = CustomerPricingService(repo)

@router.put("/")
@tracer.capture_method
def create():
    parsed_payload: CustomerPricingSetDto = parse(event=router.current_event.body, model=CustomerPricingSetDto)
    service.set(parsed_payload)
    return ResponseBuilder.build(parsed_payload.product)

@router.get("/<productId>")
@tracer.capture_method
def get_all(productId:str):
    dtos = service.get_all(productId)
    return ResponseBuilder.build(dtos)

@router.get("/rate-code/<rateCode>/product/<productId>")
@tracer.capture_method
def get_by_productId(rateCode:str,productId:str):
    dto = service.get(rateCode,productId)
    return   ResponseBuilder.build(dto)
    

