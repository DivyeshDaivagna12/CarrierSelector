from common_methods.response_builder import ResponseBuilder
from carrier_product.carrier_product_dtos import *
from carrier_product.carrier_product_srv import *
from carrier_product.carrier_product_repo import CarrierProductRepository

repo = CarrierProductRepository()
service = CarrierProductService(repo)

def lambda_handler(event, context)->any:
    resquest =  event["body"]
    path = event['path']
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']

    if http_method == "GET" and path == '/<carrier>':
        dtos = service.get_all(event["queryStringParameters"]["carrier"])
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "GET" and path == '/<carrier>/<product>':
        dtos = service.get(event["queryStringParameters"]["product"])
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "PUT" and path == '/':
        dto = CarrierProductSetDto()
        dto.__dict__ = resquest
        service.set(dto)
        return ResponseBuilder.build("Updated successfully")
    
    elif  http_method == "POST" and path == '/':
        dto = CarrierProductSetDto()
        dto.__dict__ = resquest
        service.create(dto)
        return ResponseBuilder.build("Saved successfully")
    
    else:
        return { "statusCode": 404, "body": "NotFound" }