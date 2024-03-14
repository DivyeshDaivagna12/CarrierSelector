import json
from typing import List, Type, TypeVar
# from domain.interfaces.i_product_repo import IProductRepository
# from domain.entities.product_ent import ProductEntity
import datetime
import boto3
from boto3.dynamodb.conditions import Key
import os

T = TypeVar("T")

class DBHelper():
   
    def put_item(dic: dict) -> None:
            table = DBHelper.get_table()                            
            now =datetime.datetime.now()
            x = int(now.strftime("%m%d%Y%H%M%S"))
            # dic["modify_at"] = x   
            table.put_item(Item = dic)
        
    def get_item(key: str):
            table = DBHelper.get_table()
            now =datetime.datetime.now()
          
            response = table.get_item(
                Key=key
            )
            if 'Item' in response:
                item = response['Item']
                del item['PK']
                del item['SK']
                return item
            else:
                  return None
            
    def delete (key: str):
            table = DBHelper.get_table()

            response = table.delete_item(
                Key=key
            )
            
            status_code = response['Item']
            return status_code
    
    def query(index : str,key: Key,some_class: Type[T])->List[any]:
            table = DBHelper.get_table()
            now =datetime.datetime.now()
                    
            if index is not None:
                response = table.query(
                    IndexName=index,
                    KeyConditionExpression=key,
                )
            else:
                response = table.query(
                    KeyConditionExpression=key,
                )
                 

            result = response['Items']
            

            while 'LastEvaluateKey' in response:
                response = table.query(ExclusiveStartKey=response['LastEvaluatedKey'])
                result.extend(response['Items'])

            items = response['Items']
            list_enty = list()

            for item in items:
                del item['PK']
                del item['SK']
                enty= some_class(item)
                list_enty.append(enty)

            return list_enty

    def get_table():
        #for local debugging uncomment 
        dynamo_client  =  boto3.resource(service_name = 'dynamodb',region_name = 'ca-central-1',
        aws_access_key_id = '',
        aws_secret_access_key = '')
 
        #dynamo_client  =  boto3.resource('dynamodb')
        table = dynamo_client.Table(os.environ['dynamo_table'])
        table.table_status
        return table
