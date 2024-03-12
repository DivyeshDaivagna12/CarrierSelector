from uuid import uuid4
from carrier_candidate.carrier_candidate_dtos import *
from common_methods.bad_request_exce import BadRequestException
from carrier_candidate.lane.lane_repo import LaneRepository, LaneEntity
from carrier_candidate.offering.offering_repo import OfferingRepository, OfferingEntity
from carrier_candidate.carrier.carrier_repo import CarrierRepository
from carrier_candidate.service.service_repo import ServiceRepository, ServiceEntity
from carrier_candidate.carrier_product.carrier_product_repo import CarrierProductRepository
from carrier_candidate.customer.customer_repo import CustomerRepository,CustomerEntity
from carrier_candidate.product.product_repo import ProductRepository, ProductEntity
from carrier_candidate.zones.zone_repo import *
from carrier_candidate.zones.zone_srv import ZoneService
from datetime import date

class CarrierCandidateService:
    def __init__(self):
        self.laneRepo = LaneRepository()
        self.offeringRepo = OfferingRepository()
        self.carrierRepo = CarrierRepository()
        self.carrierProductRepo = CarrierProductRepository()
        self.customerRepo = CustomerRepository()
        self.productRepo = ProductRepository()
        self.serviceRepo = ServiceRepository()
        repo = ZoneRepository()
        self.zs = ZoneService(repo)
        self.matched_lanes_dict = None
        self.vaild_offerings_for_shipment_date_dict = None
 
    # def set(self, dto: CarrierCandidateSetDto)->None:
    #     enty = CarrierCandidateEntity()
    #     if dto.id is None:
    #         dto.id = uuid4().hex
            
    #     enty.set(dto)
    #     self.repo.save(enty)

    def get_candidates(self, request_dto: CarrierCandidateSetDto)->CarrierCandidateDetailDto:
       
        customer = self.customerRepo.get_by_id(request_dto.customer)
        if customer is None:
           raise BadRequestException(f"Customer with id '{request_dto.customer}' not exist")
        

        probable_lanes_ids = self.get_propable_lanes(request_dto.origin_address, request_dto.destination_address)

        matched_lanes = self.get_matched_lanes(probable_lanes_ids)
        # print(matched_lanes)

        product_entities = self.productRepo.get_all()
        product_dict = dict()
        for product_entity in product_entities:
            if product_entity.id not in product_dict:
                product_dict[product_entity.id] = product_entity

        service_entities = self.serviceRepo.get_all()
        service_dict = dict()
        for servive_entity in service_entities:
            if servive_entity.id not in service_dict:
                service_dict[servive_entity.id] = servive_entity

        self.vaild_offerings_for_shipment_date_dict = self.get_vaild_offerings_for_requested_date(request_dto)

        candidate_list = self.find_candidates_list(matched_lanes,request_dto, customer, product_dict, service_dict)
        # print(candidate_list)

        return candidate_list

    def find_candidates_list(self, matched_lanes_ids, request_dto:CarrierCandidateSetDto, customer: CustomerEntity, product_dict, service_dict):
        candidate_list = []
        applicable_offering_ids = set()
        for lane_id in matched_lanes_ids:
           lane_entity:LaneEntity = self.matched_lanes_dict[lane_id]
           if (not customer.excluded_carriers) or (lane_entity.carrier not in customer.excluded_carriers):
                for lane_offering_id in lane_entity.offerings:
                    if lane_offering_id in self.vaild_offerings_for_shipment_date_dict:
                        offering:OfferingEntity = self.vaild_offerings_for_shipment_date_dict[lane_offering_id]
                        product_entity:ProductEntity = product_dict[offering.product]

                        if request_dto.product_family is not None:
                            if product_entity.family == request_dto.product_family:
                                applicable_offering_ids.add(lane_offering_id)
                        else:
                            applicable_offering_ids.add(lane_offering_id)
       
        # print(applicable_offering_ids)
        for offering_id in applicable_offering_ids:
            if offering_id in self.vaild_offerings_for_shipment_date_dict:
                offering:OfferingEntity = self.vaild_offerings_for_shipment_date_dict[offering_id]

                product_entity:ProductEntity = product_dict[offering.product]
                
                product_found = False
                if product_entity.is_restricted and (customer.products and (product_entity.id in customer.products)):
                    product_found = True
                elif not product_entity.is_restricted:
                    product_found = True

                if product_found:
                    detail = CarrierCandidateDetailDto()
                    detail.product_id = offering.product
                    detail.product_name = product_entity.description
                    detail.product_family = product_entity.family
                    detail.packaging = product_entity.packaging
                    detail.time_definite = product_entity.time_definite
                    detail.product_constraints = product_entity.constraints
                    services_array = []
                    for service_id in offering.services:
                        service_entity: ServiceEntity = service_dict[service_id]
                        if service_entity.is_restricted and (customer.services and (service_entity.id in customer.services)):
                            service_dto = ServiceDto()
                            service_dto.service_id = service_entity.id
                            service_dto.service_name = service_entity.description
                            service_dto.service_constraints = service_entity.constraints
                            services_array.append(service_dto)
                        elif not service_entity.is_restricted:
                            service_dto = ServiceDto()
                            service_dto.service_id = service_entity.id
                            service_dto.service_name = service_entity.description
                            service_dto.service_constraints = service_entity.constraints
                            services_array.append(service_dto)

                    detail.services = services_array
                    detail.carrier = offering.carrier
                    candidate_list.append(detail)

        return candidate_list
                

    def get_propable_lanes(self, origin_address:str, destination_address:str):
       # getting origin zones that occupy origin address
       origin_zones = self.zs.get_zones_for_address(origin_address)

       # getting destination zones that occupy destination address
       destination_zones = self.zs.get_zones_for_address(destination_address)
       probable_lanes = []
       # creating probable lanes by combination of origin zones and destination zones
       for origin_zone in origin_zones:
            for destination_zone in destination_zones:
                probable_lanes.append(str(origin_zone.id)+"-"+str(destination_zone.id))
       return probable_lanes
    
    def get_matched_lanes(self, probable_lanes_ids):
        matched_lanes = []
        matched_lanes_dict = dict()

       # getting lanes all at one 
        all_lane_entities = self.laneRepo.get_all()

       # finding existing lanes out of probable lanes
        for lane_id in probable_lanes_ids:
            for lane_entity in all_lane_entities:
                if lane_entity.id == lane_id and lane_entity.is_active:
                    matched_lanes_dict[lane_id] = lane_entity
                    matched_lanes.append(lane_id)

        self.matched_lanes_dict = matched_lanes_dict
        return matched_lanes
    
    def get_vaild_offerings_for_requested_date(self, request_dto: CarrierCandidateSetDto):
        all_offering_entities = self.offeringRepo.get_all()
        
        request_date = int(date.today().strftime('%Y%m%d'))

        if request_dto.request_date is not None:
            request_date = request_dto.request_date
        offering_dict = dict()
       
       # getting offering released version which is applicable to requested shipment date 
        for offering_entity in all_offering_entities:
          try:
            if not offering_entity.is_active:
               offering_entity.is_active = True
          except:
             offering_entity.is_active = True
         #  if not (offering_entity.id in res_dict):
          if request_date >= offering_entity.valid_from and request_date <= offering_entity.valid_to and offering_entity.status == "RELEASED":
             if not (offering_entity.id in offering_dict):
                offering_dict[offering_entity.id] = offering_entity.to_dto()
 
        return offering_dict
    # def get_all(self)->list[CarrierCandidateDetailDto]:
    #    list_dto = list()
    #    entities = self.repo.get_all()
    #    for enty in entities:
    #       try:
    #         list_dto .append(enty.to_dto())
    #       except:
    #        pass
    #    return list_dto
 
