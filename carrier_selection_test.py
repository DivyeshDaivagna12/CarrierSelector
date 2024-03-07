import json
from uuid import uuid4
from application.response_encoder import ResponseEncoder
from boto3.dynamodb.conditions import Key
from domain.dtos.carrier_selection_dtos import *
from domain.services.carrier_selection_srv import *
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError
from domain.services.carrier_srv import *
from infrastructure.repositories.carrier_repo import *

def test():
    carrierRepo = CarrierRepository()
    # obs = carrierRepo.get_by_id("7991")
    # print(obs.weighting)
    service = CarrierSelectionService()

    setdto = CarrierSelectionSetDto(
        origin_address="5151 Oak St, Vancouver, BC V6M 4H1, Canada", 
        destination_address="3638 Rae Ave, Vancouver, BC, Canada", 
        customer="5",
        shipment_date= 20231230,
        product_details=[
        {
            "product": "01",
            "services": [],
            "skids": 8,
            "pieces": 0
        }
    ]
    )
    obj = service.selection(setdto)
    json_str = json.dumps(obj,cls=ResponseEncoder)
    print(json_str)

    # obj = service.get(id)
    # json_str = json.dumps(obj,cls=ResponseEncoder)
    # print(json_str)
   
    # print("==============================================")

    # objs = service.get_all()
    # json_str = json.dumps(objs,cls=ResponseEncoder)
    # print(json_str)
   
test()

