
from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer

from application.response_builder import ResponseBuilder
from domain.dtos.customer_surcharge_discount_dtos import *
from domain.services.customer_surcharge_discount_srv import *
from infrastructure.repositories.customer_surcharge_discount_repo import CustomerSurchargeDiscountRepository
from aws_lambda_powertools.event_handler.api_gateway import Router


tracer = Tracer()
logger = Logger()
router = Router()
repo = CustomerSurchargeDiscountRepository()
service = CustomerSurchargeDiscountService(repo)

@router.put("/")
@tracer.capture_method
def update():
    parsed_payload: CustomerSurchargeDiscountSetDto = parse(event=router.current_event.body, model=CustomerSurchargeDiscountSetDto)
    service.set(parsed_payload)
    return ResponseBuilder.build(parsed_payload.customer)

@router.post("/")
@tracer.capture_method
def create():
    parsed_payload: CustomerSurchargeDiscountSetDto = parse(event=router.current_event.body, model=CustomerSurchargeDiscountSetDto)
    service.create(parsed_payload)
    return ResponseBuilder.build(parsed_payload.customer)

@router.get("/")
@tracer.capture_method
def get_all():
    dtos = service.get_all()
    return ResponseBuilder.build(dtos)

@router.get("/customer/<customerId>/surcharge/<surchargeId>")
@tracer.capture_method
def get(customerId: str,surchargeId:str):
    dto = service.get(customerId,surchargeId)
    return   ResponseBuilder.build(dto)
    

