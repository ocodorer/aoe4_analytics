import os
import json
from db import get_engine, SILVER_DB, BRONZE_DB, GOLD_DB, declarative_base


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from sqlalchemy import insert, select, delete

import db_gold

class Base(DeclarativeBase):
    pass


from db_silver import (
    GAME_PLAYER_STATS,
    GAME_PLAYER_RESOURCES,
    GAME_PLAYER_ACTION,
    GAME_PLAYER_BUILDORDER,
)
from db_gold import DIM_GAME, DIM_ABILITY, DIM_MAPTYPE, DIM_BUILDING, DIM_CALENDAR_DATE, DIM_CALENDAR_TIME, DIM_EVENT_TYPE, DIM_GAME_TIME, DIM_GAME_VERSION, DIM_OBJECT_TYPE, DIM_PLAYER, DIM_PLAYER_AGE, DIM_RESOURCE, DIM_TECHNOLOGY, DIM_UNIT, DIM_UPGRADE, GAME_PLAYER_BUILDORDER_TMP, GAME_PLAYER_RESOURCES_TMP, GAME_PLAYER_ACTION_TMP, FACT_RESOURCE_BALANCE

from constants import CIVS

gold_engine = get_engine(dbname=GOLD_DB)
silver_engine = get_engine(dbname=SILVER_DB)

from db_gold import init_gold_database

init_gold_database()
from sqlalchemy import text



def array_contains(arrays, keys):
    for array in arrays:
        for key in keys:
            if key in array:
                return 1
    return 0

def add_surrogate_keys(rows:list[dict], surrogate_key:str):
    index = 0
    for row in rows:
        row.update({surrogate_key: index})
        index += 1
    return rows

def run_query_silver(sql:str) -> list[dict]:
    with silver_engine.connect() as connection:
        sql = sql
        tupe_rows = connection.execute(text(sql))
        rows = tupe_rows.fetchall()
        columns = tupe_rows.keys()._keys#.__dir
        result = [{columns[colindex]: row[colindex] for colindex in range(0, len(columns))} for row in rows]
    return result

def run_query_gold(sql:str) -> list[dict]:
    with gold_engine.connect() as connection:
        sql = sql
        tupe_rows = connection.execute(text(sql))
        rows = tupe_rows.fetchall()
        columns = tupe_rows.keys()._keys#.__dir
        result = [{columns[colindex]: row[colindex] for colindex in range(0, len(columns))} for row in rows]
    return result

def insertrows_gold(Table:Base, rows:list[dict]) -> None:
    with gold_engine.connect() as connection:
        #connection.execute(Table.insert)
        connection.execute(delete(Table))
        connection.execute(insert(Table), rows)
        connection.commit()


insertrows_gold(Table=GAME_PLAYER_BUILDORDER_TMP, rows=run_query_silver(sql="""
SELECT * FROM  GamePlayerBuildOrder          
"""))

insertrows_gold(Table=GAME_PLAYER_ACTION_TMP, rows=run_query_silver(sql="""
SELECT * FROM  GamePlayerAction          
"""))


insertrows_gold(Table=GAME_PLAYER_RESOURCES_TMP, rows=run_query_silver(sql="""
SELECT * FROM  GamePlayerResources          
"""))

# result = run_query_gold(sql="""
#                         WITH
          
          
#             SELECT 
#                         DimGame.IDGame,
#                         DimPlayer.IDPlayer,  
#                         -1 IDMapType,
#                         -1 IDPlayerAge,
#                         -1 IDEventType,
#                         DimGameTime.IDGameTime,
#                         -1 IDCalendarDate,
#                         -1 IDCalendarTime,
#                         COALESCE(DimUnit.IDUnit, -1) IDUnit,
#                         COALESCE(DimAbility.IDAbility, -1) IDAbility,
#                         COALESCE(DimTechnology.IDTechnology, -1) IDTechnology,
#                         COALESCE(DimBuilding.IDBuilding, -1) IDBuilding,
#                         COALESCE(DimUpgrade.IDUpgrade, -1) IDUpgrade,
#                         /*CASE 
#                             WHEN DimEventType.EventKey = 'BuildOrder' AND DimEventType.EventCategory = 'constructed' THEN 1
#                             WHEN DimEventType.EventKey = 'BuildOrder' AND DimEventType.EventCategory = 'destroyed' THEN -1
#                             WHEN DimEventType.EventKey = 'BuildOrder' AND DimEventType.EventCategory = 'finished' THEN -1
#                             ELSE 0
#                         END Amount,*/
#                         1 Amount,
#                         COALESCE(DimUnit.Food, DimAbility.Food, DimTechnology.Food, DimBuilding.Food, DimUpgrade.Food, 0) Food,
#                         COALESCE(DimUnit.Wood, DimAbility.Wood, DimTechnology.Wood, DimBuilding.Wood, DimUpgrade.Wood, 0) Wood,
#                         COALESCE(DimUnit.Stone, DimAbility.Stone, DimTechnology.Stone, DimBuilding.Stone, DimUpgrade.Stone, 0) Stone,
#                         COALESCE(DimUnit.Gold, DimAbility.Gold, DimTechnology.Gold, DimBuilding.Gold, DimUpgrade.Gold, 0) Gold,
#                         COALESCE(DimUnit.VizierPoint, DimAbility.VizierPoint, DimTechnology.VizierPoint, DimBuilding.VizierPoint, DimUpgrade.VizierPoint, 0) Food,
#                         COALESCE(DimUnit.OliveOil, DimAbility.OliveOil, DimTechnology.OliveOil, DimBuilding.OliveOil, DimUpgrade.OliveOil, 0) OliveOil,
#                         COALESCE(DimUnit.Supply, DimAbility.Supply, DimTechnology.Supply, DimBuilding.Supply, DimUpgrade.Supply, 0) Supply
#                         /*COALESCE(DimObjectType.IDObjectType, -1) IDObjectType*/
                        

#             FROM GamePlayerBuildOrderTmp tran
#                         LEFT JOIN DimGame ON DimGame.GameId = tran.GameId
#                         LEFT JOIN DimPlayer ON DimPlayer.PlayerId = tran.profileId
#                         /*LEFT JOIN DimMapType ON DimPlayer.PlayerId = tran.profileId*/
#                         /*LEFT JOIN DimPlayerAge ON DimPlayerAge.AgeId = tran.??? find the smallest age from the upgrade events */
#                         LEFT JOIN DimEventType ON DimEventType.PBGID = tran.pbgid /* AND DimEventType.civilizationAttributeName = tran.civilizationAttrib*/
#                         LEFT JOIN DimGameTime ON  DimGameTime.TotalSecond = tran.eventTime
#                         /*LEFT JOIN DimCalendarDate ON  DimCalendarDate = Make date(game start time + tran.eventTime seconds) */
#                         /*LEFT JOIN DimCalendarTime ON  DimCalendarDate = Make date(game start time + tran.eventTime seconds) */
#                         LEFT JOIN DimBuilding ON DimBuilding.PBGID = tran.pbgid 
#                         LEFT JOIN DimTechnology ON DimTechnology.PBGID = tran.pbgid 
#                         LEFT JOIN DimUpgrade ON DimUpgrade.PBGID = tran.pbgid 
#                         LEFT JOIN DimAbility ON DimAbility.PBGID = tran.pbgid 
#                         /*LEFT JOIN DimObjectType ON DimObjectType.PBGID = tran.pbgid and civ */
#                         AND DimEventType.CivilizationAttributeName = tran.civilizationAttrib 
#                         LEFT JOIN DimUnit ON DimUnit.PBGID = tran.pbgid AND DimUnit.CivilizationAttributeName = tran.civilizationAttrib AND DimUnit.Aoe4AnalyticsGameVersion = tran.analytics_game_version
#             WHERE tran.GameId = 159753877



# """)

# insertrows_gold(Table=FACT_RESOURCE_BALANCE, rows=result)