from fsa_zone_mapping.bulk_insert_history_dtos import *
from domain.constants import *
import boto3

class BulkInsertHistoryEntity():
    original_file_name:str
    file_name:str
    user_id:str
    date_time:int
  
    def __init__(self,prop_dict=None):
        if prop_dict != None:
            self.__dict__ = prop_dict
    
    def to_dto(self)->BulkInsertHistoryDetailDto:
        dto = BulkInsertHistoryDetailDto()
        dto.original_file_name=self.original_file_name
        dto.file_name = self.file_name
        dto.user_id = self.user_id
        dto.date_time = int(self.date_time)
        dto.url = self.create_presigned_url(s3_bucket_bulk_upload,self.file_name)
        return dto
    
    def set(self, dto:BulkInsertHistorySetDto):
        self.original_file_name=dto.original_file_name
        self.file_name = dto.file_name
        self.user_id = dto.user_id
        self.date_time = dto.date_time
        return self

    def create_presigned_url(self, bucket_name:str, object_name:str, expiration=3600):
        # Generate a presigned URL for the S3 object
        s3_client = boto3.client('s3')
        
        response = s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': bucket_name,
                                                                'Key': object_name},
                                                        ExpiresIn=expiration)
       
      

        # The response contains the presigned URL
        return response