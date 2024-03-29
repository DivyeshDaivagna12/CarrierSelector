
from ast import List
from typing import List, Optional
from carrier_candidate.shared import ConstraintDto

class ServiceDto:
        service_id: str
        service_name: str
        service_constraints: List[ConstraintDto]

class CarrierCandidateDetailDto:
        carrier: str
        product_id: str
        product_name: str
        product_family: str
        packaging: str
        time_definite: str
        product_constraints: List[ConstraintDto]
        services: List[ServiceDto]
 
class CarrierCandidateSetDto:
        origin_address: str
        destination_address: str
        request_date: Optional[int]
        customer: str
        product_family: Optional[str]

