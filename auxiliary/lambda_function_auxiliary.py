from application.response_builder import ResponseBuilder
from customer_surcharge.customer_surcharge_srv import CustomerSurchargeService
from service.service_srv import ServiceService
from customer_surcharge.customer_surcharge_repo import CustomerSurchargeRepository
from service.service_repo import ServiceRepository
from packaging.packaging_srv import PackagingService
from packaging.packaging_repo import PackagingRepository
from time_definite.time_definite_repo import TimeDefiniteRepository
from time_definite.time_definite_srv import TimeDefinteService

repo = PackagingRepository()
service = PackagingService(repo)

def lambda_handler(event, context)->any:
    
    request =  event["body"]
    path = event['path']
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']
    
    if  http_method == "GET" and path == '/current-user':
        user_email = context.get('current_user',"")
        return ResponseBuilder.build(user_email)
    
    elif  http_method == "GET" and path == '/add-seed-data':
        ServiceService(ServiceRepository()).add_system_services()
        PackagingService(PackagingRepository()).add_system_packaging()
        CustomerSurchargeService(CustomerSurchargeRepository()).add_system_surcharges()
        TimeDefinteService(TimeDefiniteRepository()).add_system_timedefinite()
        return ResponseBuilder.build("Done")
    
    elif  http_method == "GET" and path == 'external/test':
       return ResponseBuilder.build("external test called")
    else:
        return { "statusCode": 404, "body": "NotFound" }
    
