import json
from zone.i_zone_repo import IZoneRepository
from zone.zone_dtos import ZoneDetailDto, ZoneStatusDetailDto
from boto3.dynamodb.conditions import Key
import datetime
import boto3
import os
from common_methods.not_found_exce import RescourceNotFoundException

from infrastructure.repositories.RDSdbhelper import RDSDBHelper

class ZoneRepository(IZoneRepository):
    def get_all_zones(self) -> list[object]:
        conn, edit_table_name, approved_table_name = RDSDBHelper.get_conn()
        cur = conn.cursor()
        query = "SELECT id,name FROM {} ORDER BY id".format(approved_table_name)
        cur.execute(query)
        results = cur.fetchall()
        
        res = []
        for result in results:
                res.append([result[0], result[1].strip() if result[1] != None else ""])
        return res
    
    def get_zones_status(self) -> list[ZoneStatusDetailDto]:
        conn, edit_table_name, approved_table_name = RDSDBHelper.get_conn()
        cur = conn.cursor()
        resultArray = []
        # to get all zones that are deleted
        deletedZonesQuery = "SELECT t1.ID, t1.name, 'Deleted' as status FROM {} t1 LEFT JOIN {} t2 ON t1.ID = t2.ID WHERE t2.ID IS NULL".format(approved_table_name,edit_table_name)
        cur.execute(deletedZonesQuery)
        results = cur.fetchall()
        for result in results:
            resultArray.append([result[0], result[1].strip() if result[1] != None else "" , result[2].strip() if result[2] != None else ""])

        #to get all zones that are newly added
        newlyAddedZonesQuery = "SELECT t1.ID, t1.name, 'Added' as status FROM {} t1 LEFT JOIN {} t2 ON t1.ID = t2.ID WHERE t2.ID IS NULL".format(edit_table_name,approved_table_name)
        cur.execute(newlyAddedZonesQuery)
        results = cur.fetchall()
        # print(results)
        for result in results:
            resultArray.append([result[0], result[1].strip() if result[1] != None else "" , result[2].strip() if result[2] != None else ""])
        
        #to get all zones that are updated
        updatedZonesQuery = "SELECT t1.ID, t1.name, 'Updated' as status FROM {} as t1 INNER JOIN {} as t2 ON t1.ID=t2.ID WHERE t1.name != t2.name OR not st_equals(t1.geom, t2.geom);".format(edit_table_name,approved_table_name)
        cur.execute(updatedZonesQuery)
        results = cur.fetchall()
        for result in results:
            resultArray.append([result[0], result[1].strip() if result[1] != None else "" , result[2].strip() if result[2] != None else ""])
        
        #to get all zoned that are unchanged
        notChangedZonesQuery = "SELECT t1.ID, t1.name, 'Not changed' as status FROM {} as t1 INNER JOIN {} as t2 ON t1.ID=t2.ID WHERE t1.name = t2.name and st_equals(t1.geom, t2.geom);".format(edit_table_name,approved_table_name)
        cur.execute(notChangedZonesQuery)
        results = cur.fetchall()
        # print(results)
        for result in results:
            resultArray.append([result[0], result[1].strip() if result[1] != None else "" , result[2].strip() if result[2] != None else ""])
        
        return resultArray

    def get_zones_for_coordinates(self, lat: float, long: float) -> list[ZoneDetailDto]:
        conn, edit_table_name, approved_table_name = RDSDBHelper.get_conn()
        cur = conn.cursor()
        
        # print(lat,long)
        query = "SELECT id,name FROM {} WHERE ST_Within(ST_SetSRID(ST_POINT({},{}),4326), geom::geometry) ORDER BY id".format(approved_table_name,long,lat)
        cur.execute(query)
        results = cur.fetchall()
        res = []
        for result in results:
                res.append([result[0], result[1].strip() if result[1] != None else ""])
        return res
    
    def update_table_operation(self) -> None:
        conn, edit_table_name, approved_table_name = RDSDBHelper.get_conn()
        cur = conn.cursor()

        # to do update operation
        updateOperationQuery = "do $$ begin if (SELECT EXISTS (SELECT * FROM information_schema.tables WHERE table_name = '{}')) then DROP TABLE {}; CREATE TABLE {} AS TABLE {} WITH DATA; else CREATE TABLE {} AS TABLE {} WITH DATA; END if; end $$".format(approved_table_name,approved_table_name,approved_table_name,edit_table_name,approved_table_name,edit_table_name)
        cur.execute(updateOperationQuery)
        conn.commit()
        return "success"
        