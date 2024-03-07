import json
from uuid import uuid4
from application.response_encoder import ResponseEncoder
from boto3.dynamodb.conditions import Key
from domain.dtos.customer_dtos import *
from domain.services.customer_srv import *
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError
from domain.services.customer_srv import *
from infrastructure.repositories.customer_repo import *

def test():
    customerRepo = CustomerRepository()
    # obs = carrierRepo.get_by_id("7991")
    # print(obs.weighting)
    service = CustomerService(customerRepo)

    setdto = CustomerSetDto(
        id="0000082",
        description="test customer",
        is_active=True
      
    )
    obj = service.create(setdto)
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

