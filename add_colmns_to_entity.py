import json
from typing import List, Type, TypeVar
from domain.interfaces.i_product_repo import IProductRepository
from domain.entities.product_ent import ProductEntity
import datetime
import boto3
from boto3.dynamodb.conditions import Key
import os
   
def put_item(dic: dict,table_name) -> None:
            table = get_table(table_name)                            
            now =datetime.datetime.now()
            x = int(now.strftime("%m%d%Y%H%M%S"))
            # dic["modify_at"] = x   
            table.put_item(Item = dic)
        
    
    
def get_all_rows(enty:str, table_name: str)->List[any]:
            table = get_table(table_name)
            now =datetime.datetime.now()
   
            response = table.query(
                IndexName='entity-PK-index',
                KeyConditionExpression=Key('entity').eq(enty))
          
                 

            result = response['Items']

            while 'LastEvaluateKey' in response:
                response = table.query(ExclusiveStartKey=response['LastEvaluatedKey'])
                result.extend(response['Items'])

            items = response['Items']
            return items

def get_table(table_name:str):
        #for local debugging uncomment 
        dynamo_client  =  boto3.resource(service_name = 'dynamodb',region_name = 'ap-south-1',
                aws_access_key_id = '',
                aws_secret_access_key = '')

       #dynamo_client  =  boto3.resource('dynamodb')
        table = dynamo_client.Table(table_name)
        table.table_status
        return table

def add_columns(enty:str,table_name:str,columns:dict):
       rows = get_all_rows(enty,table_name)
       for row in rows:
        for col_name in columns:
            row[col_name]= columns[col_name]

       count=0
       for row in rows:
        print(row)
        put_item(row,table_name)
        count = count +1
        print(count)  

col=dict()
col["is_system"]=False
col["is_active"]=True
col["constraints"]="[]"

#add_columns("service",os.environ['dynamo_table'], col)