from carrier_repo import *
from carrier_srv import *
from carrier_repo import *
from costing.costing_dtos import *
from costing.costing_srv import CostingService
from common_methods.response_builder import ResponseBuilder
from carrier_product.carrier_product_srv import CarrierProductService
from carrier_product.carrier_product_repo import CarrierProductRepository

repo = CarrierRepository()
service = CarrierService(repo)
cost_service = CostingService()

def lambda_handler(event, context)->any:
    
    request =  event["body"]
    path = event['path']
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']
    
    if http_method == "POST" and path == '/':
        parsed_payload: CarrierSetDto = parse(event=request, model=CarrierSetDto)
        service.create(parsed_payload)
        CarrierProductService(CarrierProductRepository()).add_system_products(parsed_payload.id)
        return ResponseBuilder.build(parsed_payload.id)
    
    elif  http_method == "PUT" and path == '':
        parsed_payload: CarrierSetDto = parse(event=request, model=CarrierSetDto)
        service.update(parsed_payload)
        return ResponseBuilder.build(parsed_payload.id)
    
    elif  http_method == "GET" and path == '/':
        dtos = service.get_all()
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "PUT" and path == '/<id>':
        dto = service.get(event["queryStringParameters"]["id"])
        return   ResponseBuilder.build(dto)
    
    elif  http_method == "GET" and path == '/carrier-cost':
        parsed_payload: CostingDto = parse(event=request, model=CostingDto)
        response  = cost_service.get_details(parsed_payload)
        return ResponseBuilder.build(response)
    else:
        return { "statusCode": 404, "body": "NotFound" }
    
