from common_methods.response_builder import ResponseBuilder
from bulk_insert_history.bulk_insert_history_dtos import *
from bulk_insert_history.bulk_insert_history_srv import *
from bulk_insert_history.bulk_insert_history_repo import BulkInsertHistoryRepository

repo = BulkInsertHistoryRepository()
service = BulkInsertHistoryService(repo)

def lambda_handler(event, context)->any:
    resquest =  event["body"]
    path = event['path']
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']

    if http_method == "GET" and path == '/':
        dtos = service.get_all()
        return ResponseBuilder.build(dtos)