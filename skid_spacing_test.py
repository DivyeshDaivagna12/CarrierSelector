import json
from uuid import uuid4
from application.response_encoder import ResponseEncoder
from boto3.dynamodb.conditions import Key
from domain.dtos.skid_spacing_dtos import *
from domain.services.skid_spacing_srv import *
from infrastructure.repositories.skid_spacing_repo import SkidSpacingRepository
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError


def test():
    repo = SkidSpacingRepository()
    service = SkidSpacingService(repo)

    id = 1
    id1= 'newid'
    setdto = SkidSpacingSetDto(id=id1, skid_space=id, longest_side_min=1,longest_side_max=10, second_longest_side_min=5, second_longest_side_max=25, is_active=True)
    service.set(setdto)

    # obj = service.get(id)
    # json_str = json.dumps(obj,cls=ResponseEncoder)
    # print(json_str)
   
    print("==============================================")

    objs = service.get_all()
    json_str = json.dumps(objs,cls=ResponseEncoder)
    print(json_str)
   
test()

