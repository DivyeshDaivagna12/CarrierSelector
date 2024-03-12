# Standard library imports
from ast import parse

# Local application imports
from customer_surcharge.common_methods.response_builder import ResponseBuilder
from customer_surcharge_dtos import *
from customer_surcharge_srv import *
from customer_surcharge_repo import CustomerSurchargeRepository

repo = CustomerSurchargeRepository()
service = CustomerSurchargeService(repo)

def lambda_handler(event, context)->any:
    request =  event["body"]
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']

    if  http_method == "POST" and path == '/':
        parsed_payload: CustomerSurchargeSetDto = parse(event=request, model=CustomerSurchargeSetDto)
        service.create(parsed_payload)
        return ResponseBuilder.build(parsed_payload.service)
    
    elif  http_method == "PUT" and path == '/':
        parsed_payload: CustomerSurchargeSetDto = parse(event=request, model=CustomerSurchargeSetDto)
        service.set(parsed_payload)
        return ResponseBuilder.build(parsed_payload.service)
    
    elif  http_method == "GET" and path == '/':
         dtos = service.get_all()
         return ResponseBuilder.build(dtos)
    
    elif  http_method == "GET" and path == '/<serviceId>':
        serviceId =  event["queryStringParameters"]["serviceId"]
        dto = service.get(serviceId)
        return ResponseBuilder.build(dto)
    
    else:
        return { "statusCode": 404, "body": "NotFound" }