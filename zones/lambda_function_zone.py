from zone_dtos import *
from zone_srv import *
from infrastructure.repositories.zone_repo import *
from application.response_builder import ResponseBuilder

repo = ZoneRepository()
zs = ZoneService(repo)

def lambda_handler(event, context)->any:
    
    resquest =  event["body"]
    path = event['path']
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']
    
    if http_method == "GET" and path == '/':
        dtos = zs.get_all_zones()
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "GET" and path == '/address/<address>':
        dtos = zs.get_zones_for_address(event["rawQueryString"])
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "GET" and path == '/status':
        dtos = zs.get_zones_status()
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "PUT" and path == '/update':
        zs.update_operation()
        return ResponseBuilder.build("Updated successfully")
    
    elif  http_method == "GET" and path == '/qgis-screen"':
        user_email = context.get('current_user',"")
        dtos = zs.get_stream_url(user_email)
        return ResponseBuilder.build(dtos)
    else:
        return { "statusCode": 404, "body": "NotFound" }