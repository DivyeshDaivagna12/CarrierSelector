from pydantic import BaseModel

class BulkInsertHistoryDetailDto:
        original_file_name:str
        file_name:str
        user_id:str
        date_time:int
        url:str
 
class BulkInsertHistorySetDto(BaseModel):
       original_file_name:str
       file_name:str
       user_id:str
       date_time:str

