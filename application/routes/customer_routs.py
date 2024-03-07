
from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer

from application.response_builder import ResponseBuilder
from domain.dtos.customer_dtos import *
from domain.services.customer_srv import *
from domain.services.customer_surcharge_srv import CustomerSurchargeService
from infrastructure.repositories.customer_repo import CustomerRepository
from aws_lambda_powertools.event_handler.api_gateway import Router

from infrastructure.repositories.customer_surcharge_repo import CustomerSurchargeRepository


tracer = Tracer()
logger = Logger()
router = Router()
repo = CustomerRepository()
service = CustomerService(repo)

@router.post("/")
@tracer.capture_method
def add():
    parsed_payload: CustomerSetDto = parse(event=router.current_event.body, model=CustomerSetDto)
    service.create(parsed_payload)
    return ResponseBuilder.build(parsed_payload.id)

@router.put("/")
@tracer.capture_method
def update():
    parsed_payload: CustomerSetDto = parse(event=router.current_event.body, model=CustomerSetDto)
    service.update(parsed_payload)
    return ResponseBuilder.build(parsed_payload.id)

@router.get("/")
@tracer.capture_method
def get_all():
    dtos = service.get_all()
    return ResponseBuilder.build(dtos)

@router.get("/<id>")
@tracer.capture_method
def get_by_id(id:str):
    dto = service.get(id)
    return   ResponseBuilder.build(dto)
    

