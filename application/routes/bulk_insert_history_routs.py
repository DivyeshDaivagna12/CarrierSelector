
from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer

from application.response_builder import ResponseBuilder
from domain.dtos.bulk_insert_history_dtos import *
from domain.services.bulk_insert_history_srv import *
from infrastructure.repositories.bulk_insert_history_repo import BulkInsertHistoryRepository
from aws_lambda_powertools.event_handler.api_gateway import Router


tracer = Tracer()
logger = Logger()
router = Router()
repo = BulkInsertHistoryRepository()
service = BulkInsertHistoryService(repo)

@router.get("/")
@tracer.capture_method
def get_all():
    dtos = service.get_all()
    return ResponseBuilder.build(dtos)

    

