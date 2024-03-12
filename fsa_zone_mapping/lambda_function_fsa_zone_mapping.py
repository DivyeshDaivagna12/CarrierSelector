# Standard library imports
from ast import parse
from dataclasses import asdict, is_dataclass
import json
import json
import boto3
import base64
from datetime import datetime

# Local application imports
from common_methods.response_builder import ResponseBuilder
from fsa_zone_mapping_dtos import *
from fsa_zone_mapping.fsa_zone_mapping_srv import *
from infrastructure.repositories.dbhelper import DBHelper
from fsa_zone_mapping_repo import FsaZoneMappingRepository

repo = FsaZoneMappingRepository()
service = FsaZoneMappingService(repo)

def lambda_handler(event, context)->any:
    request =  event["body"]
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']

    if  http_method == "POST" and path == '/':
        parsed_payload: FsaZoneMappingSetDto = parse(event=request, model=FsaZoneMappingSetDto)
        service.create(parsed_payload)
        return ResponseBuilder.build(parsed_payload.origin_fsa)
    
    elif  http_method == "PUT" and path == '/':
        parsed_payload: FsaZoneMappingSetDto = parse(event=request, model=FsaZoneMappingSetDto)
        service.set(parsed_payload)
        return ResponseBuilder.build(parsed_payload.origin_fsa)
    
    elif  http_method == "GET" and path == '/':
        dtos = service.get_all()
        return ResponseBuilder.build(dtos)

    
    elif  http_method == "GET" and path == '/origin-fsa/<origin_fsa>':
          origin_fsa = event["queryStringParameters"]["origin_fsa"]
          dto = service.get(origin_fsa)
          return ResponseBuilder.build(dto)
    
    elif  http_method == "POST" and path == '/bulk-upload':
          file_content=base64.b64decode(request)
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
        
    user_email = request.context.get('current_user',"")
    service.bulk_insert(file_content_without_headers,filename,user_email)