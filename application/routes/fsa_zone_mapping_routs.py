
from dataclasses import asdict, is_dataclass
import json
from aws_lambda_powertools import Logger, Tracer

from application.response_builder import ResponseBuilder
from domain.dtos.fsa_zone_mapping_dtos import *
from domain.services.fsa_zone_mapping_srv import *
from infrastructure.repositories.dbhelper import DBHelper
from infrastructure.repositories.fsa_zone_mapping_repo import FsaZoneMappingRepository
from aws_lambda_powertools.event_handler.api_gateway import Router
import json
import boto3
import base64
from datetime import datetime

tracer = Tracer()
logger = Logger()
router = Router()
repo = FsaZoneMappingRepository()
service = FsaZoneMappingService(repo)


@router.post("/")
@tracer.capture_method
def create():
    parsed_payload: FsaZoneMappingSetDto = parse(event=router.current_event.body, model=FsaZoneMappingSetDto)
    service.create(parsed_payload)
    return ResponseBuilder.build(parsed_payload.origin_fsa)

@router.put("/")
@tracer.capture_method
def create():
    parsed_payload: FsaZoneMappingSetDto = parse(event=router.current_event.body, model=FsaZoneMappingSetDto)
    service.set(parsed_payload)
    return ResponseBuilder.build(parsed_payload.origin_fsa)

@router.get("/")
@tracer.capture_method
def get_all():
    dtos = service.get_all()
    return ResponseBuilder.build(dtos)

@router.get("/origin-fsa/<origin_fsa>")
@tracer.capture_method
def get_by_origin(origin_fsa:str):
    dto = service.get(origin_fsa)
    return   ResponseBuilder.build(dto)

@router.post("/bulk-upload")
@tracer.capture_method
def bulk_insert():
    file_content=base64.b64decode(router.current_event.body)
    filename_index=file_content.find(b'filename=')    

    if filename_index !=-1:
     filename_start= filename_index + len(b'filename="')
     filename_end=file_content.find(b'"',filename_start)
     filename=file_content[filename_start:filename_end].decode()

     # Find the start of the actual file content
     file_content_start= file_content.find(b'\r\n\r\n') + len(b'\r\n\r\n')
     

     # Extract relevant part of the content
     file_content_without_headers=file_content[file_content_start:]

     boundary=b'\r\n'

     if boundary in file_content_without_headers:
         parts=file_content_without_headers.split(boundary,1)

         file_content_without_headers = parts[0]
      
     user_email = router.context.get('current_user',"")
          
     service.bulk_insert(file_content_without_headers,filename,user_email)

     
   

 
   
  

    

