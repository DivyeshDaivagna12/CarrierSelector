import json
from typing import List, Type, TypeVar
import datetime
import boto3
from boto3.dynamodb.conditions import Key
import os

import psycopg2


T = TypeVar("T")

class RDSDBHelper():

    def get_conn():
        # localConn = psycopg2.connect(
        #     host="localhost",
        #     port="5432",
        #     database="purolatortest",
        #     user="postgres",
        #     password="postgres"
        # )
        awsConn = psycopg2.connect(
            host=os.environ['postgres_host'],
            port=os.environ['postgres_port'],
            database=os.environ['postgres_db_name'],
            user=os.environ['postgres_user_name'],
            password=os.environ['postgres_password']
        )

        approved_table_name = "approved_zones" 
        edit_table_name = "new_zones"
        return awsConn, edit_table_name, approved_table_name
    
    def get_place_index_client():
        
        place_index_client  =  boto3.client('location')
        placeIndexName = os.environ['place_index_name']
        return place_index_client, placeIndexName
        
