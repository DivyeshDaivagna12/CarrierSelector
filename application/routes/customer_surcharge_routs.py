
from aws_lambda_powertools import Logger, Tracer
from application.response_builder import ResponseBuilder
from domain.dtos.customer_surcharge_dtos import *
from domain.services.customer_surcharge_srv import *
from infrastructure.repositories.customer_surcharge_repo import CustomerSurchargeRepository
from aws_lambda_powertools.event_handler.api_gateway import Router


tracer = Tracer()
logger = Logger()
router = Router()
repo = CustomerSurchargeRepository()
service = CustomerSurchargeService(repo)

@router.post("/")
@tracer.capture_method
def create():
    parsed_payload: CustomerSurchargeSetDto = parse(event=router.current_event.body, model=CustomerSurchargeSetDto)
    service.create(parsed_payload)
    return ResponseBuilder.build(parsed_payload.service)

@router.put("/")
@tracer.capture_method
def create():
    parsed_payload: CustomerSurchargeSetDto = parse(event=router.current_event.body, model=CustomerSurchargeSetDto)
    service.set(parsed_payload)
    return ResponseBuilder.build(parsed_payload.service)

@router.get("/")
@tracer.capture_method
def get_all():
    dtos = service.get_all()
    return ResponseBuilder.build(dtos)

@router.get("/<serviceId>")
@tracer.capture_method
def get_by_service(serviceId:str):
    dto = service.get(serviceId)
    return ResponseBuilder.build(dto)
    

