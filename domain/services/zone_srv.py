from  domain.entities.product_ent import ProductEntity
from domain.dtos.zone_dtos import *
from domain.exceptions.not_found_exce import RescourceNotFoundException
from domain.interfaces.i_zone_repo import IZoneRepository
from infrastructure.repositories.RDSdbhelper import RDSDBHelper
import boto3
import os
class ZoneService:
  
  
  def __init__(self, repo: IZoneRepository):
      self.repo = repo
 
  def get_all_zones(self) -> list[ZoneDetailDto]:
        
      list_dto = list()
      zones = self.repo.get_all_zones()

      for zone in zones:
        z = ZoneDetailDto()
        z.id = zone[0]
        z.name = zone[1]
        list_dto.append(z)
      
      return list_dto

  def get_zones_for_address(self, address: str) -> list[ZoneDetailDto]:
      
      client, placeIndexName = RDSDBHelper.get_place_index_client()

      response = client.search_place_index_for_text(
      
          FilterCountries=[
              'CAN',
          ],
          IndexName=placeIndexName,
          # Key='v1.public.eyJqdGkiOiJkN2I5NWFjOC05MDVlLTQ0NGYtOTA3NC0zNmNhYzFkNjg3M2IifRO00CMQARwvKcmkzcYBAXF2fij3OV2Ji8shZt3Wvc3tTQjP8baNTUos0ODHlYB0YBu8-tejsUaWULtsWTRjU9CTYLvnBtrP0Pl1xsauDVQ18iGm1o40t02xU4gnyLU47-keYoqRLn6tuWWtiZ2vbHRUpVKBHioOMc9z0qTFAM4E9UvVmQ4-Mg-eXk9Nq9cWW6dLJsfW2qd0nS7I8W4YzbPEnA2GoYKIfcsAC6BT1sQsV5gsGjpaaVsu1h9IumKNzzjBao_jKeX3LwCtBzpNOav-pCeA-7qjLl7dWV3eWix-6ble_2w9p4SDu8D1gStCTzp4i6Fe0bBbfDcQo4H_wJA.Njg1MGZlZTUtYTI2ZS00MDdlLWJjNDktMDNmZDlkNzVmMjQ0',
          Language='en',
          MaxResults=10,
          Text=address
      )
  
      results = response["Results"]
      if len(results) == 0:
          raise RescourceNotFoundException(f"Invalid address. Please provide correct address")
      long = results[0]["Place"]["Geometry"]["Point"][0]
      lat = results[0]["Place"]["Geometry"]["Point"][1]
        
      list_dto = list()
      zones = self.repo.get_zones_for_coordinates(lat, long)

      for zone in zones:
        z = ZoneDetailDto()
        z.id = zone[0]
        z.name = zone[1]
        list_dto.append(z)
      
      return list_dto
  
  def get_zones_status(self):
     
    list_dto = list()
    zones = self.repo.get_zones_status()

    for zone in zones:
        z = ZoneStatusDetailDto()
        z.id = zone[0]
        z.name = zone[1]
        z.status = zone[2]
        list_dto.append(z)
      
    return list_dto
  
  def update_operation(self):
    return self.repo.update_table_operation()
  
  def get_stream_url(self, user_email):
    if user_email is None:
       user_email = "testuser"
    user_email = "test"
    # client = boto3.client('appstream',
    #             aws_access_key_id = '',
    #             aws_secret_access_key = '',
    #             region_name = 'ap-south-1'
    #         )
    client = boto3.client('appstream')
    stackName = os.environ['app_stream_stack_name']
    fleetName = os.environ['app_stream_fleet_name']
    applicationId = os.environ['app_stream_application_id']
    validity = 1800

    response = client.create_streaming_url(
        StackName=stackName,
        FleetName=fleetName,
        UserId=user_email,
        ApplicationId=applicationId,
        Validity=validity
        # SessionContext='string'
    )
    if "StreamingURL" in response:
      return response["StreamingURL"]
    else:
       raise RescourceNotFoundException("Streaming URL not found")
     
     
     
