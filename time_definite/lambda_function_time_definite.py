from ast import parse
from application.response_builder import ResponseBuilder
from time_definite.time_definite_dtos import TimeDefiniteSetDto
from time_definite.time_definite_srv import TimeDefinteService
from time_definite.time_definite_repo import TimeDefiniteRepository

repo = TimeDefiniteRepository()
td = TimeDefinteService(repo)

def lambda_handler(event, context)->any:
    
    request =  event["body"]
    path = event['path']
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']
     
    if http_method == "GET" and path == '/':
        dtos = td.get()
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "GET" and path == '/<id>':
        dtos = td.get_all(event["rawQueryString"])
        return ResponseBuilder.build(dtos)
    
    elif  http_method == "PUT" and path == '/':
        parsed_payload: TimeDefiniteSetDto = parse(event=request, model=TimeDefiniteSetDto)
        td.set(parsed_payload)
        return ResponseBuilder.build("Updated successfully")
    
    else:
           return { "statusCode": 404, "body": "NotFound" }