from dataclasses import asdict, is_dataclass
import json
from application.response_builder import ResponseBuilder
from customer_surcharge_discount.customer_surcharge_discount_dtos import *
from customer_surcharge_discount.customer_surcharge_discount_srv import *
from infrastructure.repositories.customer_surcharge_discount_repo import CustomerSurchargeDiscountRepository
from aws_lambda_powertools.event_handler.api_gateway import Router

repo = CustomerSurchargeDiscountRepository()
service = CustomerSurchargeDiscountService(repo)

def lambda_handler(event, context)->any:
    resquest =  event["body"]
    path = event['path']
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']

    if http_method == "GET" and path == '/':
        dtos = service.get_all()
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "GET" and path == '/<customer>/<product>':
        dtos = service.get(event["rawQueryString"])
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "PUT" and path == '/':
        dto = CustomerSurchargeDiscountSetDto()
        dto.__dict__ = resquest
        service.set(dto)
        return ResponseBuilder.build("Updated successfully")
    
    elif  http_method == "POST" and path == '/':
        dto = CustomerSurchargeDiscountSetDto()
        dto.__dict__ = resquest
        service.create(dto)
        return ResponseBuilder.build("Saved successfully")
    
    else:
        return { "statusCode": 404, "body": "NotFound" }