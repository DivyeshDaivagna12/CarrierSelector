from common_methods.response_builder import ResponseBuilder
from customer_surcharge_discount.customer_surcharge_discount_dtos import *
from customer_surcharge_discount.customer_surcharge_discount_srv import *
from customer_surcharge_discount_repo import CustomerSurchargeDiscountRepository

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
    
    elif  http_method == "GET" and path == '/customer/<customerId>/surcharge/<surchargeId>':
        dtos = service.get(event["queryStringParameters"]["customerId"],
                           event["queryStringParameters"]["surchargeId"])
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