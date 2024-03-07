
from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer
from application.response_builder import ResponseBuilder
from domain.dtos.product_dtos import *
from domain.services.product_srv import *
from infrastructure.repositories.product_repo import ProductRepository
from aws_lambda_powertools.event_handler.api_gateway import Router


tracer = Tracer()
logger = Logger()
router = Router()
repo = ProductRepository()
service = ProductService(repo)

@router.post("/")
@tracer.capture_method
def create():
    parsed_payload: ProductSetDto = parse(event=router.current_event.body, model=ProductSetDto)
    service.create(parsed_payload)
    return ResponseBuilder.build(parsed_payload.id)

@router.put("/")
@tracer.capture_method
def create():
    parsed_payload: ProductSetDto = parse(event=router.current_event.body, model=ProductSetDto)
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
    

