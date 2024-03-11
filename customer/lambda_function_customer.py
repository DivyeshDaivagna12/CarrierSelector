from aws_lambda_powertools import Logger, Tracer
from application.response_builder import ResponseBuilder
from customer.customer_dtos import *
from domain.services.customer_srv import *
from infrastructure.repositories.customer_repo import CustomerRepository
from aws_lambda_powertools.event_handler.api_gateway import Router
from infrastructure.repositories.customer_surcharge_repo import CustomerSurchargeRepository

repo = CustomerRepository()
service = CustomerService(repo)

def lambda_handler(event, context)->any:
    resquest =  event["body"]
    path = event['path']
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']

    if http_method == "GET" and path == '/':
        dtos = service.get_all()
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "GET" and path == '/<id>':
        dtos = service.get(event["rawQueryString"])
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "PUT" and path == '/':
        dto = CustomerSetDto()
        dto.__dict__ = resquest
        service.update(dto)
        return ResponseBuilder.build("Updated successfully")
    
    elif  http_method == "POST" and path == '/':
        dto = CustomerSetDto()
        dto.__dict__ = resquest
        service.create(dto)
        return ResponseBuilder.build("Saved successfully")
