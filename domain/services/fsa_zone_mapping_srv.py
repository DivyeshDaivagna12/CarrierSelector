from uuid import uuid4
from domain.dtos.bulk_insert_history_dtos import BulkInsertHistorySetDto
from domain.entities.bulk_insert_history_ent import BulkInsertHistoryEntity
from  domain.entities.fsa_zone_mapping_ent import FsaZoneMappingEntity
from domain.dtos.fsa_zone_mapping_dtos import *
from domain.exceptions.not_found_exce import RescourceNotFoundException
from domain.interfaces.i_fsa_zone_mapping_repo import IFsaZoneMappingRepository
import io
import boto3
import openpyxl
import datetime
from domain.services.bulk_insert_history_srv import BulkInsertHistoryService
from domain.constants import *
from infrastructure.repositories.bulk_insert_history_repo import BulkInsertHistoryRepository

client=boto3.client('s3')

#sheet1
_key_sheet1 = "RM#FSA"
_entity_sheet1 = "fsazonemapping"
_sk_sheet1 = "#OZ"

#sheet2
_key_sheet2 = "#OZ"
_entity_sheet2 = "fsaratemapping"
_sk_sheet2 = "#FSA"


class FsaZoneMappingService:
    def __init__(self, repo: IFsaZoneMappingRepository):
        self.repo = repo
 
    def create(self, dto: FsaZoneMappingSetDto)->None:
        enty = FsaZoneMappingEntity()                
        enty.set(dto)
        self.repo.create(enty)

    def set(self, dto: FsaZoneMappingSetDto)->None:
        enty = FsaZoneMappingEntity()                
        enty.set(dto)
        self.repo.save(enty)

    def get(self, origin_fsa: str)->FsaZoneMappingDetailDto:
       enty = self.repo.get_by_origin(origin_fsa)
       if enty is None:raise RescourceNotFoundException(f"FSAZoneMapping {origin_fsa} not found")
       return enty.to_dto()
    
    def get_all(self)->list[FsaZoneMappingDetailDto]:
       list_dto = list()
       entities = self.repo.get_all()
       for enty in entities:
          try:
            list_dto .append(enty.to_dto())
          except:
           pass
       return list_dto
    
    def bulk_insert(self, file_content:str,filename:str,user_email:str):
       original_file_name=filename
       filename=uuid4().hex+'_'+filename
       print("filename:",filename)

       response=client.put_object(
       Body=file_content,
       Bucket=s3_bucket_bulk_upload,
       Key=filename
    )
       
       # Retrieve the file from S3 Bucket
       response=client.get_object(Bucket=s3_bucket_bulk_upload, Key=filename)
       xlsx_content=response['Body'].read()

       # Load the workbook from the Excel file content
       try:
        workbook=openpyxl.load_workbook(io.BytesIO(xlsx_content))
       except:
        raise RescourceNotFoundException("File uploaded seems to be corrupted, please check the file and try again.")
       # Process Sheet1
       print("Processing Sheet1 data")
       sheet1= workbook.worksheets[0]
       origin_zone_values=self.repo.process_zone_mapping_batch(sheet1,_key_sheet1,_sk_sheet1,_entity_sheet1)
       print("origin_zone_values from process1:",origin_zone_values)
       print("Sheet1 data processing completed")

       # Process Sheet2
       print("Processing Sheet2 data")
       sheet2=workbook.worksheets[1]
       origin_zone=origin_zone_values[0]

       if origin_zone is None:
          raise RescourceNotFoundException("Origin_zone is None. Cannot process with sheet2")
       else:
        print("origin_zone value:",origin_zone)
        self.repo.process_rate_mapping_batch(sheet2,_key_sheet2,_sk_sheet2,_entity_sheet2,origin_zone)
        print("Sheet2 data processing completed")

        # bulk-insert-history
       
      #  now =datetime.datetime.now()
      #  start_date_time = now.strftime("%m%d%Y%H%M%S")
       start_date_time=int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

       bulk_insert_history_entity=  BulkInsertHistorySetDto(original_file_name=original_file_name,file_name=filename,user_id=user_email,date_time=start_date_time)
              
       bulk_insert_history_repo_instance=BulkInsertHistoryRepository()

       bulk_insert_history_service_instance=BulkInsertHistoryService(bulk_insert_history_repo_instance)
       
       bulk_insert_history_service_instance.set(bulk_insert_history_entity)
       
       




     
 
