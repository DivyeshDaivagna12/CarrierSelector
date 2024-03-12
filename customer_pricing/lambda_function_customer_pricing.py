# Standard library imports
from ast import parse

# Local application imports
from i_customer_pricing_repo import *
from customer_pricing_repo import *
from customer_pricing_dtos import *
from customer_pricing_srv import CustomerPricingService
from customer_pricing.common_methods.response_builder import ResponseBuilder

repo = CustomerPricingRepository()
service = CustomerPricingService(repo)

def lambda_handler(event, context)->any:
    request =  event["body"]
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']

    if  http_method == "GET" and path == '/<productId>':
        productId = event["queryStringParameters"]["productId"]
        dtos = service.get_all(productId)
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "GET" and path == '/rate-code/<rateCode>/product/<productId>':
        rateCode = event["queryStringParameters"]["rateCode"]
        productId = event["queryStringParameters"]["productId"]
        dtos = service.get(rateCode,productId)
        return ResponseBuilder.build(dtos)

    elif  http_method == "PUT" and path == '/':
        parsed_payload: CustomerPricingSetDto = parse(event=request, model=CustomerPricingSetDto)
        service.set(parsed_payload)
        return ResponseBuilder.build(parsed_payload.product)
    
    else:
        return { "statusCode": 404, "body": "NotFound" }
    
