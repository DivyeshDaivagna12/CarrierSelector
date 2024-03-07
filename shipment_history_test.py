import json
from uuid import uuid4
from application.response_encoder import ResponseEncoder
from boto3.dynamodb.conditions import Key
from domain.dtos.shipment_history_dtos import *
from domain.services.shipment_history_srv import *
from infrastructure.repositories.shipment_history_repo import ShipmentHistoryRepository
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError


def test():
    repo = ShipmentHistoryRepository()
    service = ShipmentHistoryService(repo)

    setdto = ShipmentHistorySetDto(
        customer = "5",
        origin_address = "6833 Village Green, Burnaby, BC V5E 4K9, Canada",
        shipment_id = "123",
        carrier_id = "7994",
        shipment_date = 20231130
    )
    # id = uuid4().hex
    # setdto = ShipmentHistorySetDto(id=id, description=f"{id}description", is_active=True)
    service.set(setdto)

    # obj = service.get_by_customer("7")
    # json_str = json.dumps(obj,cls=ResponseEncoder)
    # print(json_str)

    obj = service.get_by_shipment_date(20231130)
    json_str = json.dumps(obj,cls=ResponseEncoder)
    print(json_str)
   
    print("==============================================")

    obj = service.get_by_shipment_date_and_customer(20231130,"7")
    json_str = json.dumps(obj,cls=ResponseEncoder)
    print(json_str)
   
   
test()

