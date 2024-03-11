from application.response_builder import ResponseBuilder
from product_dtos import *
from product_srv import *
from product_repo import ProductRepository

repo = ProductRepository()
ps = ProductService(repo)

def lambda_handler(event, context)->any:
    
    request =  event["body"]
    path = event['path']
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']
     
    if http_method == "GET" and path == '/<id>':
        dtos = ps.get(event["rawQueryString"])
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "GET" and path == '/':
        dtos = ps.get_all()
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "Post" and path == '/':
        parsed_payload: ProductSetDto = parse(event=request, model=ProductSetDto)
        ps.create(parsed_payload)
        return ResponseBuilder.build("Added successfully")
    
    elif  http_method == "PUT" and path == '/':
        parsed_payload: ProductSetDto = parse(event=request, model=ProductSetDto)
        ps.update(parsed_payload)
        return ResponseBuilder.build("Updated successfully")
    
    else:
         return { "statusCode": 404, "body": "NotFound" }
