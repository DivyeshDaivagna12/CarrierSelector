
from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer

from application.response_builder import ResponseBuilder
from domain.dtos.carrier_dtos import *
from domain.services.carrier_product_srv import CarrierProductService
from domain.services.carrier_srv import *
from infrastructure.repositories.carrier_repo import CarrierRepository
from infrastructure.repositories.carrier_product_repo import CarrierProductRepository
from aws_lambda_powertools.event_handler.api_gateway import Router
from domain.dtos.costing_dtos import *
from domain.services.costing_srv import *

tracer = Tracer()
logger = Logger()
router = Router()
repo = CarrierRepository()
service = CarrierService(repo)
product_service = CostingService()


@router.post("/")
@tracer.capture_method
def create():
    parsed_payload: CarrierSetDto = parse(event=router.current_event.body, model=CarrierSetDto)
    service.create(parsed_payload)
    CarrierProductService(CarrierProductRepository()).add_system_products(parsed_payload.id)
    return ResponseBuilder.build(parsed_payload.id)

@router.put("/")
@tracer.capture_method
def update():
    parsed_payload: CarrierSetDto = parse(event=router.current_event.body, model=CarrierSetDto)
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


@router.get("/carrier-cost")
@tracer.capture_method
def get_cost():
    parsed_payload: CostingDto = parse(event=router.current_event.body, model=CostingDto)
    response  = product_service.get_details(parsed_payload)
    return ResponseBuilder.build(response)
    


