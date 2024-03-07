import json
from uuid import uuid4
from application.response_encoder import ResponseEncoder
from boto3.dynamodb.conditions import Key
from domain.dtos.rate_master_dtos import *
from domain.dtos.carrier_product_dtos import *
from domain.services.rate_master_srv import *
from domain.services.customer_surcharge_srv import *
from infrastructure.repositories.customer_surcharge_repo import *
from infrastructure.repositories.carrier_product_repo import *
from domain.services.carrier_product_srv import *
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError


def test():
    service = RateMasterService()
    setdto = RateMasterSetDto(
        customer_number= "5", #7991 with no rate code and 5 with rate code D4 and 7995 with no discount
        origin_fsa= "V6M",
        destination_fsa= "4H1",
        product_details=[
            {
                "product": "22", 
                "services": ["57a7fb8393954a33af4af5f998cc92e0"],
                "skids" : 11,
                "pieces": 0
            }
        ]
    )

    # id = uuid4().hex
    # setdto = RateMasterSetDto(id=id, description=f"{id}description", is_active=True)
    # service.get_pricing(setdto)

    obj = service.get_pricing(setdto)
    json_str = json.dumps(obj,cls=ResponseEncoder)
    print(json_str)
   
    # print("==============================================")

    # objs = service.get_all()
    # json_str = json.dumps(objs,cls=ResponseEncoder)
    # print(json_str)

def test2():
    customerSurchargeRepo = CustomerSurchargeRepository()
    t = customerSurchargeRepo.get_by_service("EXCESSIVE_SKID_SPACE")
    print(t.price)

def test3():
    t = CustomerProductDiscountRepository()
    r = t.get("5", "22", "D04")
    r.to_dto()

def test4():
    r = CarrierProductRepository()
    s = CarrierProductService(r)

    setdto = CarrierProductSetDto(
        carrier = "7991",
        product = "4c5be53c3de64f518a773c783209e228",
        cost = 211.5,
        is_active = False
    )
    s.set(setdto)

test()

