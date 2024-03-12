import json
from common_methods.response_builder import ResponseBuilder
from customer_product_discount.customer_product_discount_dtos import *
from customer_product_discount.customer_product_discount_srv import *
from customer_product_discount_repo import CustomerProductDiscountRepository

repo = CustomerProductDiscountRepository()
service = CustomerProductDiscountService(repo)

def lambda_handler(event, context)->any:
    resquest =  event["body"]
    path = event['path']
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']

    if http_method == "GET" and path == '/':
        dtos = service.get_all()
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "GET" and path == '/<customer>/<product>':
        dtos = service.get(event["queryStringParameters"]["customer"],
                           event["queryStringParameters"]["product"],
                           None)
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "PUT" and path == '/':
        dto = CustomerProductDiscountSetDto()
        dto.__dict__ = resquest
        service.set(dto)
        return ResponseBuilder.build("Updated successfully")
    
    elif  http_method == "POST" and path == '/':
        dto = CustomerProductDiscountSetDto()
        dto.__dict__ = resquest
        service.create(dto)
        return ResponseBuilder.build("Saved successfully")
    
    elif http_method == "GET" and path == '/customer/<customerId>/product/<productId>/rateCode/<rateCode>':
        dto = service.get(event["queryStringParameters"]["customer"],
                           event["queryStringParameters"]["product"],
                           event["queryStringParameters"]["rateCode"])
        return ResponseBuilder.build(dto)
    
    else:
        return { "statusCode": 404, "body": "NotFound" }