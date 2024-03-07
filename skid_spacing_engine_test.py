import json
from uuid import uuid4
from application.response_encoder import ResponseEncoder
from boto3.dynamodb.conditions import Key
from domain.dtos.skid_spacing_engine_dtos import *
from domain.services.skid_spacing_engine_srv import *
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError


def test():
    service = SkidSpacingEngineService()

    setdto = SkidSpacingEngineRequestDto(
        dimensions=[
            {
                "length": 145, 
                "width": 23,
            }
        ]
    )
    # id = uuid4().hex
    # setdto = SkidSpacingEngineSetDto(id=id, description=f"{id}description", is_active=True)
    # service.set(setdto)

    obj = service.get_skids_count(setdto)
    json_str = json.dumps(obj,cls=ResponseEncoder)
    print(json_str)
   
    # print("==============================================")

    # objs = service.get_all()
    # json_str = json.dumps(objs,cls=ResponseEncoder)
    # print(json_str)
   
test()

