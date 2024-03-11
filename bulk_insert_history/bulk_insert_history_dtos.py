
from ast import List
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError
from typing import List, Optional
import datetime


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

