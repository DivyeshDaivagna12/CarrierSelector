
from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer

from application.response_builder import ResponseBuilder
from domain.dtos.customer_product_discount_dtos import *
from domain.services.customer_product_discount_srv import *
from infrastructure.repositories.customer_product_discount_repo import CustomerProductDiscountRepository
from aws_lambda_powertools.event_handler.api_gateway import Router


tracer = Tracer()
logger = Logger()
router = Router()
repo = CustomerProductDiscountRepository()
service = CustomerProductDiscountService(repo)

@router.put("/")
@tracer.capture_method
def update():
    parsed_payload: CustomerProductDiscountSetDto = parse(event=router.current_event.body, model=CustomerProductDiscountSetDto)
    service.set(parsed_payload)
    return ResponseBuilder.build(parsed_payload.product)

@router.post("/")
@tracer.capture_method
def create():
    parsed_payload: CustomerProductDiscountSetDto = parse(event=router.current_event.body, model=CustomerProductDiscountSetDto)
    service.create(parsed_payload)
    return ResponseBuilder.build(parsed_payload.product)

@router.get("/")
@tracer.capture_method
def get_all():
    dtos = service.get_all()
    return ResponseBuilder.build(dtos)

@router.get("/customer/<customerId>/product/<productId>")
@tracer.capture_method
def get_by_id(customerId: str,productId:str):
    dto = service.get(customerId,productId,None)
    return   ResponseBuilder.build(dto)

@router.get("/customer/<customerId>/product/<productId>/rateCode/<rateCode>")
@tracer.capture_method
def get_by_id(customerId: str,productId:str,rateCode:List[str]):
    dto = service.get(customerId,productId,rateCode)
    return   ResponseBuilder.build(dto)



