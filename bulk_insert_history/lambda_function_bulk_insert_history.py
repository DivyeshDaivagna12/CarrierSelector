from dataclasses import asdict, is_dataclass
from application.response_builder import ResponseBuilder
from bulk_insert_history.bulk_insert_history_dtos import *
from domain.services.bulk_insert_history_srv import *
from infrastructure.repositories.bulk_insert_history_repo import BulkInsertHistoryRepository
from aws_lambda_powertools.event_handler.api_gateway import Router

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