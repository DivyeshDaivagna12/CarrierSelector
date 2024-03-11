# Standard library imports
import json
from ast import parse
from dataclasses import asdict, is_dataclass

# Local application imports
from application.response_builder import ResponseBuilder
from customer_surcharge_dtos import *
from customer_surcharge_srv import *
from customer_surcharge_repo import CustomerSurchargeRepository
# from aws_lambda_powertools.event_handler.api_gateway import Router

#router = Router()
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
        serviceId = request.args.get('serviceId', default = None)
        dto = service.get(serviceId)
        return ResponseBuilder.build(dto)
    
    else:
        return { "statusCode": 404, "body": "NotFound" }