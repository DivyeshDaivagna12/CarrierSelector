
from ast import List
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError
from dataclasses import dataclass
from typing import List, Optional

class ZoneDetailDto:
        id:int
        name:str

class ZoneStatusDetailDto:
        id:int
        name:str
        status:str
 


