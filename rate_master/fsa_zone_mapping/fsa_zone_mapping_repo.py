from rate_master.common_methods.already_exist_exce import AlreadyExistException
from boto3.dynamodb.conditions import Key
from rate_master.infrastructure.dbhelper import DBHelper
from concurrent.futures import ThreadPoolExecutor, wait
from rate_master.fsa_zone_mapping.fsa_zone_mapping_ent import FsaZoneMappingEntity
from rate_master.fsa_zone_mapping.i_fsa_zone_mapping_repo import IFsaZoneMappingRepository



table_name=DBHelper.get_table()

_key = "RM#FSA"
_entity = "fsazonemapping"
_sk = "#OZ"

batch_size = 25

class FsaZoneMappingRepository(IFsaZoneMappingRepository):
  
    def create(self, enty: FsaZoneMappingEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = _key + enty.origin_fsa
            dic['SK'] = _sk
            dic['entity'] = _entity
            
            if self.origin_zone_exists(enty):
                 raise AlreadyExistException(f"Origin FSA already mapped to Zone!")
           
            DBHelper.put_item(dic)
   
    def save(self, enty: FsaZoneMappingEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = _key + enty.origin_fsa
            dic['SK'] = _sk
            dic['entity'] = _entity                  
            DBHelper.put_item(dic)
        
    def get_by_origin(self, origin_fsa: str) -> FsaZoneMappingEntity:
            key =  Key={
                    "PK": _key +origin_fsa,
                    "SK": _sk
                }
            item = DBHelper.get_item(key)
            if item is None:
                   return None
            enty = FsaZoneMappingEntity(item)
            return enty
    
    def get_all(self) -> list[FsaZoneMappingEntity]:
         k=Key('SK').eq(_sk)
         return DBHelper.query('SK-PK-index',k,FsaZoneMappingEntity)

    # Bulk Insert 
    
    def process_zone_mapping_row(batch, key, sk,entity,batch_writer):
         last_valid_origin_zone=None
       
         for row in batch:
            origin_fsa, origin_zone= row[0],row[1]

            # Check if any cell in the row contains None
            if None in(origin_fsa, origin_zone):
                #Skip the row if it contains None
                continue
            
            print(" origin_fsa:", origin_fsa)
            print(" origin_zone:", origin_zone)      
      
            # Upload data to DynamoDb
            batch_writer.put_item(Item={
                                        'PK':key+origin_fsa,
                                        'SK':sk,
                                        'entity':entity,               
                                        'origin_fsa':origin_fsa,
                                        'origin_zone':origin_zone,
                                        'is_active':True
                                        })
          
            print(f"Saved data for zone mapping: PK={key+origin_fsa}, SK={sk}, Entity={entity},Origin_FSA={origin_fsa}, Origin_Zone={origin_zone}")
            
            last_valid_origin_zone=origin_zone
         return last_valid_origin_zone
    
    def process_rate_mapping_row(batch, key, sk,entity,batch_writer, origin_zone):
  
      
      #Extract data from the row
         destination_fsa, rate_code = batch[0], batch[1]

         for row in batch:
           # print("row->",row)
           destination_fsa, rate_code= row[0], row[1]

           # Check if any cell in the row contains None
           if None in(destination_fsa, rate_code):
                #Skip the row if it contains None
                continue

           print(" destination_fsa:", destination_fsa)
           print(" rate_code:", rate_code)

           # Upload data to DynamoDb
           batch_writer.put_item(Item={
                        'PK':key+str(origin_zone),
                        'SK':sk+destination_fsa,
                        'entity':entity,
                        'destination_fsa':destination_fsa,
                        'origin_zone' :origin_zone,
                        'rate_code':rate_code,
                        'is_active':True

                     })
         
           print(f"Saved data for rate mapping: PK={key+str(origin_zone)}, SK={sk+destination_fsa},"
            f"Entity={entity}, Destination_FSA={destination_fsa}, Origin_Zone={origin_zone}, Rate_Code={rate_code}")

    def process_zone_mapping_batch(self,sheet,key,sk,entity):

          rows = list(sheet.iter_rows(min_row=2, values_only=True))
          print("rows:",rows)
          try:
               with table_name.batch_writer() as batch_writer: 
                    with ThreadPoolExecutor(max_workers=None) as executor:

                         #Split rows into batches
                         batches = [rows[i:i + batch_size] for i in range (0, len(rows), batch_size)]
                         
                         #Submit each batch to the executor
                         futures=[executor.submit(FsaZoneMappingRepository.process_zone_mapping_row,batch,key,sk,entity,batch_writer) for batch in batches]
                         print("futures:",futures)

                         # Wait for all futures to complete
                         wait(futures)   

                         origin_zone_values=[future.result() for future in futures]

                         return origin_zone_values 
          except Exception as e:
               raise e

    def process_rate_mapping_batch(self,sheet,key,sk,entity,origin_zone):

         rows = list(sheet.iter_rows(min_row=2, values_only=True))
         print("rows:",rows)
     
         with table_name.batch_writer() as batch_writer: 
            with ThreadPoolExecutor(max_workers=None) as executor:

                    #Split rows into batches
               batches = [rows[i:i + batch_size] for i in range (0, len(rows), batch_size)]

               futures=[executor.submit(FsaZoneMappingRepository.process_rate_mapping_row,batch,key,sk,entity,batch_writer,origin_zone) for batch in batches]
               print("futures:",futures)

               # Wait for all futures to complete
               wait(futures)       
    
    def origin_zone_exists(self, entity:FsaZoneMappingEntity) -> bool:
        k = Key('PK').eq(_key + entity.origin_fsa) & Key('SK').eq( _sk )
        items = DBHelper.query(None,k,FsaZoneMappingEntity)

        if items and len(items) > 0:
             return True
        
        return False
       

        
  
