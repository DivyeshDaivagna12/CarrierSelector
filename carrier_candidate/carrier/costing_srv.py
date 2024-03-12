import json,re
from costing_dtos import *
from offering.offering_srv import *
from carrier_product.carrier_product_srv import *
from offering.offering_repo import OfferingRepository
from carrier_product.carrier_product_repo import CarrierProductRepository


class CostingService:

    def __init__(self):
        self.offering_repo = OfferingRepository()
        self.offering_service = OfferingService(self.offering_repo)
        self.product_repo = CarrierProductRepository()
        self.produc_service = CarrierProductService(self.product_repo)

    def get_details(self,request_dto: CostingDto):

        final_response = dict()
        today = int(date.today().strftime('%Y%m%d'))
        alpha_number = {1 :"one",2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven",8 :"eight",9:"nine"}
        basecost = 0
        additional_piece_cost = 0
        additional_skid_cost  = 0
        total_cost  = []
        offering_entities = self.offering_repo.get_all()
        for product_details in request_dto.product_details:
            for offer in offering_entities:
                if offer.product == product_details["product"]:
                    if today >= int(offer.valid_from) and today <= int(offer.valid_to) and offer.status == "RELEASED":
                        cost=  offer.cost 
                        try:
                            cost = (cost.replace('""','"').replace("null",'""'))
                            cost  = re.findall('{(.*)}',cost)
                            cost = json.loads('{'+cost[0]+'}')
                    
                            if cost.get('scale_skid'):
                                if int(product_details["skids"]) > 6:
                                    basecost = cost.get('scale_skid')["six_skid_cost"]
                                    additional_skid_cost = self.produc_service.get(request_dto.route_number,"EXCESSIVE_SKID_SPACE")
                                    additional_skid_cost = additional_skid_cost.cost
                                       
                                else:

                                    if 1 <= int(product_details["skids"]) <=2:
                                        basecost = cost.get('scale_skid')["two_skid_cost"]
                                    elif 3 <= int(product_details["skids"]) <=4:
                                        basecost = cost.get('scale_skid')["four_skid_cost"]
                                    elif 5 <= int(product_details["skids"]) <=6:
                                        basecost = cost.get('scale_skid')["six_skid_cost"]

                            elif cost.get('fixed_cost'):
                                basecost = cost.get('fixed_cost')
                            else:
                                if  cost.get('scale_piece'):
                                    basecost = cost.get('scale_piece')["one_piece_cost"]
                                    additional_piece_cost = cost.get('scale_piece')["additional_piece_cost"]
                            break
                        except Exception as e:
                            raise e

            total_excessive_skid_cost = (int(product_details["skids"])-6) *(additional_skid_cost)
            services_list = []
            for services in product_details["services"]:
                service_dict = dict()
                service_cost = self.produc_service.get(request_dto.route_number,services)
                total_cost.append(float(service_cost.cost))
                service_dict["service_id"] = services
                service_dict["service_cost"] = service_cost.cost
                services_list.append(service_dict)
            total_cost.append(float(basecost))
            total_cost.append(float(additional_piece_cost))
            total_cost.append(float(additional_skid_cost))
            total_cost.append(float(total_excessive_skid_cost))
            final_response["basecost"] = basecost
            final_response["additional_piece_cost"] = additional_piece_cost
            final_response["additional_skid_cost"] = additional_skid_cost
            final_response["total_excessive_skid_cost"] =total_excessive_skid_cost
            final_response["services"] =services_list
            final_response["total_cost"] = sum(total_cost)
           
            return final_response

