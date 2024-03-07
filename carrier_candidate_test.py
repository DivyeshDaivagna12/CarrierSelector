import json
from uuid import uuid4
from application.response_encoder import ResponseEncoder
from boto3.dynamodb.conditions import Key
from domain.dtos.carrier_candidate_dtos import *
from domain.services.carrier_candidate_srv import *
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError


def test():
    service = CarrierCandidateService()
    setdto = CarrierCandidateSetDto(
        origin_address="L0J 3T8", 
        destination_address="L0J 6C9", 
        # request_date=20231215,
        customer="10",
        product_family="e99bbc2921a14089b68de80954a538a9"
    )
    {
}
    # id = uuid4().hex
    # setdto = CarrierCandidateSetDto(id=id, description=f"{id}description", is_active=True)
    # service.set(setdto)

    obj = service.get_candidates(setdto)
    json_str = json.dumps(obj,cls=ResponseEncoder)
    print(json_str)
   
    # print("==============================================")

    # objs = service.get_all()
    # json_str = json.dumps(objs,cls=ResponseEncoder)
    # print(json_str)
   
test()

