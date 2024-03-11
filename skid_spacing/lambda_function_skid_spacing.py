from skid_spacing_dtos import *
from skid_spacing_srv import *
from skid_spacing_repo import *
from application.response_builder import ResponseBuilder

repo = SkidSpacingRepository()
ss = SkidSpacingService(repo)

def lambda_handler(event, context)->any:
    
    resquest =  event["body"]
    path = event['path']
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']
     
    if http_method == "GET" and path == '/':
        dtos = ss.get()
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "GET" and path == '/':
        dtos = ss.get_all()
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "PUT" and path == '/<id>':
        ss.set(event["rawQueryString"])
        return ResponseBuilder.build("Updated successfully")
    
    else:
           return { "statusCode": 404, "body": "NotFound" }