
from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer

from application.response_builder import ResponseBuilder
from domain.dtos.shipment_history_dtos import *
from domain.services.shipment_history_srv import *
from infrastructure.repositories.shipment_history_repo import ShipmentHistoryRepository
from aws_lambda_powertools.event_handler.api_gateway import Router


tracer = Tracer()
logger = Logger()
router = Router()
repo = ShipmentHistoryRepository()
service = ShipmentHistoryService(repo)

@router.put("/")
@tracer.capture_method
def create():
    parsed_payload: ShipmentHistorySetDto = parse(event=router.current_event.body, model=ShipmentHistorySetDto)
    service.set(parsed_payload)
    return ResponseBuilder.build("Success")

# @router.get("/customer/<customerId>")
# @tracer.capture_method
# def get_by_customer(customerId: str):
#     dtos = service.get_by_customer(customerId)
#     return ResponseBuilder.build(dtos)

@router.get("/customer/<customerId>/shipment_date/<shipment_date>")
@tracer.capture_method
def get_by_shipment_date_and_customer(customerId:str, shipment_date: str):
    dto = service.get_by_shipment_date_and_customer(int(shipment_date), customerId)
    return   ResponseBuilder.build(dto)


@router.get("/shipment_date/<shipment_date>")
@tracer.capture_method
def get_by_shipment_date(shipment_date: str):
    dto = service.get_by_shipment_date(int(shipment_date))
    return   ResponseBuilder.build(dto)
    

