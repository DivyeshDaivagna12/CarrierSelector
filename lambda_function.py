import json
from uuid import uuid4

import requests
from application.token_validator import get_email_from_access_token
from application.unauthorized_exception import UnauthorizedException
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver,CORSConfig
from aws_lambda_powertools.utilities.typing import LambdaContext
from application.exception_handler import exception_response
from application.routes import product_routs,product_family_routs,packaging_routs,service_routs, time_definite_routs, zone_routs ,customer_routs,carrier_routs,product_routs,auxiliary_rout,lane_routs,offering_routs,carrier_offering_routs,carrier_product_routs,customer_pricing_routs,customer_surcharge_routs,fsa_zone_mapping_routs,carrier_selection_routs,fsa_rate_mapping_routs,customer_product_discount_routs,customer_surcharge_discount_routs,shipment_history_routs,rate_master_routs,skid_spacing_routs,bulk_insert_history_routs,carrier_candidate_routs,skid_spacing_engine_routs#template_routs
from application.response_encoder import *


tracer = Tracer()
logger = Logger()
cors_config = CORSConfig(allow_origin="*", max_age=300)
app = APIGatewayHttpResolver(serializer=custom_serializer,cors=cors_config)
app.include_router(zone_routs.router,prefix="/zone")
app.include_router(product_family_routs.router,prefix="/product-family") 
app.include_router(packaging_routs.router,prefix="/packaging") 
app.include_router(service_routs.router,prefix="/service") 
app.include_router(customer_routs.router,prefix="/customer") 
app.include_router(carrier_routs.router,prefix="/carrier") 
app.include_router(product_routs.router,prefix="/product") 
app.include_router(auxiliary_rout.router,prefix="") 

app.include_router(lane_routs.router,prefix="/lane") 
app.include_router(carrier_product_routs.router,prefix="/carrier-product") 
app.include_router(offering_routs.router,prefix="/offering") 
app.include_router(carrier_offering_routs.router,prefix="/carrier-offering") 
app.include_router(customer_pricing_routs.router,prefix="/customer-pricing") 
app.include_router(customer_surcharge_routs.router,prefix="/customer-surcharge") 
app.include_router(fsa_zone_mapping_routs.router,prefix="/fsa-zone-mapping") 
app.include_router(carrier_selection_routs.router,prefix="/carrier-selection") 
app.include_router(fsa_rate_mapping_routs.router,prefix="/fsa-rate-mapping") 
app.include_router(customer_product_discount_routs.router,prefix="/customer-product-discount") 
app.include_router(customer_surcharge_discount_routs.router,prefix="/customer-surcharge-discount") 
app.include_router(shipment_history_routs.router,prefix="/shipment-history") 
app.include_router(bulk_insert_history_routs.router,prefix="/bulk-insert-history") 
app.include_router(rate_master_routs.router,prefix="/rate-master") 
app.include_router(skid_spacing_routs.router,prefix="/skid-spacing") 
app.include_router(carrier_candidate_routs.router,prefix="/carrier-candidate") 
app.include_router(skid_spacing_engine_routs.router,prefix="/skid-spacing-engine")
app.include_router(time_definite_routs.router,prefix="/time-definite")
#template_include
#template app.include_router(product_family_routs.router,prefix="/"route-prefix")#

@app.exception_handler(Exception)
def handle_error(ex: Exception):  
    metadata = {"path": app.current_event.path, "query_strings": app.current_event.query_string_parameters}
    exName = ex.__class__.__name__
    logger.error(f"error_type: {exName} message: {ex}", extra=metadata)
    return exception_response(ex)

def lambda_handler(event: dict, context: LambdaContext)->any:

    try:
         
        get_current_user(event)

    except UnauthorizedException as e:
        return{
           'statusCode':401,
            'body' : str(e)
            } 

    res= app.resolve(event, context)
    res["body"] = sanitize_response(res["body"])
    return res 

def get_current_user(event):
    authorization = event.get('headers',{}).get('authorization')
    if not authorization:
        raise UnauthorizedException("Access token not found")
    authorization=authorization.replace('Bearer', '').strip()
    user_email=get_email_from_access_token(authorization)

    if user_email:
        app.append_context(current_user=user_email)
   

def sanitize_response(body):
    if type(body) is str:
        body = body.replace('\\', '').replace('"[', '[').replace('"[', '[').replace(']"', ']')
    return body


   


  
