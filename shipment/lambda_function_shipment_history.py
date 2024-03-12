# Standard library imports
from dataclasses import asdict, is_dataclass
import json

# Local application imports

from application.response_builder import ResponseBuilder
from shipment_history_dtos import *
from domain.services.shipment_history_srv import *
from shipment_history_repo import ShipmentHistoryRepository
# from aws_lambda_powertools.event_handler.api_gateway import Router


repo = ShipmentHistoryRepository()
service = ShipmentHistoryService(repo)


def lambda_handler(event, context)->any:
    request =  event["body"]
    #path = event['path']
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']


    if  http_method == "PUT" and path == '/':
        parsed_payload: ShipmentHistorySetDto = parse(event=request, model=ShipmentHistorySetDto)
        service.set(parsed_payload)
        return ResponseBuilder.build("Success")
    
    elif http_method == "GET" and path == '/customer/<customerId>/shipment_date/<shipment_date>':
         shipment_date = request.args.get('shipment_date', default = None)
         customerId = request.args.get('customerId', default = None)
         dto = service.get_by_shipment_date_and_customer(int(shipment_date), customerId)
         return   ResponseBuilder.build(dto)
    
    elif http_method == "GET" and path == '/shipment_date/<shipment_date>':
         shipment_date = request.args.get('shipment_date', default = None)
         dto = service.get_by_shipment_date(int(shipment_date))
         return   ResponseBuilder.build(dto)
   
    else:
        return { "statusCode": 404, "body": "NotFound" }
    
