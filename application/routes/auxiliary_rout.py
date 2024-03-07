
from aws_lambda_powertools import Logger, Tracer
from application.response_builder import ResponseBuilder
from aws_lambda_powertools.event_handler.api_gateway import Router
from domain.services.customer_surcharge_srv import CustomerSurchargeService
from domain.services.service_srv import ServiceService
from infrastructure.repositories.customer_surcharge_repo import CustomerSurchargeRepository
from infrastructure.repositories.service_repo import ServiceRepository
from domain.services.packaging_srv import PackagingService
from infrastructure.repositories.packaging_repo import PackagingRepository
from infrastructure.repositories.time_definite_repo import TimeDefiniteRepository
from domain.services.time_definite_srv import TimeDefinteService

tracer = Tracer()
router = Router()

@router.get("/current-user")
@tracer.capture_method
def get_current_user():
    user_email = router.context.get('current_user',"")
    return ResponseBuilder.build(user_email)


@router.post("/add-seed-data")
@tracer.capture_method
def add_seed_data():
    ServiceService(ServiceRepository()).add_system_services()
    PackagingService(PackagingRepository()).add_system_packaging()
    CustomerSurchargeService(CustomerSurchargeRepository()).add_system_surcharges()
    TimeDefinteService(TimeDefiniteRepository()).add_system_timedefinite()
    
    return ResponseBuilder.build("Done")

@router.get("/external/test")
@tracer.capture_method
def get_external_test():
    return ResponseBuilder.build("external test called")

    

