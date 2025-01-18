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
from db_gold import DIM_GAME, DIM_ABILITY, DIM_MAPTYPE, DIM_BUILDING, DIM_CALENDAR_DATE, DIM_CALENDAR_TIME, DIM_EVENT_TYPE, DIM_GAME_TIME, DIM_GAME_VERSION, DIM_OBJECT_TYPE, DIM_PLAYER, DIM_PLAYER_AGE, DIM_RESOURCE, DIM_TECHNOLOGY, DIM_UNIT, DIM_UPGRADE

from constants import CIVS

gold_engine = get_engine(dbname=GOLD_DB)
silver_engine = get_engine(dbname=SILVER_DB)

from db_gold import init_gold_database

init_gold_database()
from sqlalchemy import text


def getSQLDimGame():
    return """
    SELECT 
        DISTINCT gameId GameId 
        FROM (
            SELECT DISTINCT gameId FROM GamePlayerBuildOrder
            UNION
            SELECT DISTINCT gameId FROM GamePlayerResources
            UNION
            SELECT DISTINCT gameId FROM GamePlayerAction
        )
    """

def getSQLDimPlayer():
    return """
    SELECT 
        DISTINCT profileId PlayerId
        FROM (
            SELECT DISTINCT profileId FROM GamePlayerBuildOrder
            UNION
            SELECT DISTINCT profileId FROM GamePlayerResources
            UNION
            SELECT DISTINCT profileId FROM GamePlayerAction
        )
    """

def getSQLDimEventType():
    
    return """
        SELECT  EventKey, EventName, EventCategory, EventSubCategory, CivilizationAttributeName, 
                Aoe4AnalyticsGameVersion, Aoe4ReplayApiBuild, Aoe4WorldAppVersion, Aoe4WorldAppDataChecksum, 
                Aoe4WorldMajorVersion, Aoe4WorldDataRepositoryGitCommitHash, PBGID, COUNT(1)  FROM (
            SELECT DISTINCT pbgid PBGID, 'BuildOrder' EventKey, 'N/A' EventName, key EventCategory, type EventSubCategory, civilizationAttrib CivilizationAttributeName ,
            analytics_game_version Aoe4AnalyticsGameVersion,
            aoe_api_version Aoe4ReplayApiVersion,
            aoe_api_build Aoe4ReplayApiBuild,
            aoe2world_app_version Aoe4WorldAppVersion,
            aoe2world_data_checksum Aoe4WorldAppDataChecksum,
            aoe2world_major_version Aoe4WorldMajorVersion,
            aoe4world_data_git_hash Aoe4WorldDataRepositoryGitCommitHash FROM GamePlayerBuildOrder
            UNION
            SELECT DISTINCT NULL PBGID, 'Action' EventKey, 'N/A' EventName, key EventCategory, NULL EventSubCategory, civilizationAttrib CivilizationAttributeName, 
            analytics_game_version Aoe4AnalyticsGameVersion,
            aoe_api_version Aoe4ReplayApiVersion,
            aoe_api_build Aoe4ReplayApiBuild,
            aoe2world_app_version Aoe4WorldAppVersion,
            aoe2world_data_checksum Aoe4WorldAppDataChecksum,
            aoe2world_major_version Aoe4WorldMajorVersion,
            aoe4world_data_git_hash Aoe4WorldDataRepositoryGitCommitHash FROM GamePlayerAction
            UNION
            SELECT NULL PBGID, 'Resources' EventKey, 'N/A' EventName, 'GatheredResources' EventCategory, NULL EventSubCategory, civilizationAttrib CivilizationAttributeName, 
            analytics_game_version Aoe4AnalyticsGameVersion, 
            aoe_api_version Aoe4ReplayApiVersion,
            aoe_api_build Aoe4ReplayApiBuild,
            aoe2world_app_version Aoe4WorldAppVersion,
            aoe2world_data_checksum Aoe4WorldAppDataChecksum,
            aoe2world_major_version Aoe4WorldMajorVersion,
            aoe4world_data_git_hash Aoe4WorldDataRepositoryGitCommitHash From GamePlayerResources
        )
        GROUP BY EventKey, EventName, EventCategory, EventSubCategory, CivilizationAttributeName, Aoe4AnalyticsGameVersion, Aoe4ReplayApiBuild, Aoe4WorldAppVersion, Aoe4WorldAppDataChecksum, Aoe4WorldMajorVersion, Aoe4WorldDataRepositoryGitCommitHash, PBGID
    """             

def array_contains(arrays, keys):
    for array in arrays:
        for key in keys:
            if key in array:
                return 1
    return 0

def getSQLDimObjectType():
    sql = """
        SELECT DISTINCT name, pbgid, classes, civs, effects, producedBy, unlocks, displayClasses, garrison_classes, type, `unique`, unlockedBy, weapons, attribName, armor, 
        analytics_game_version,
        aoe_api_version,
        aoe_api_build,
        aoe2world_app_version,
        aoe2world_data_checksum,
        aoe2world_major_version
        FROM Unit
        UNION
        SELECT DISTINCT name, pbgid, classes, civs, effects, producedBy, unlocks, displayClasses, garrison_classes, type, `unique`, unlockedBy, weapons, attribName, armor, 
                analytics_game_version,
        aoe_api_version,
        aoe_api_build,
        aoe2world_app_version,
        aoe2world_data_checksum,
        aoe2world_major_version
          FROM Building
        UNION
        SELECT DISTINCT name, pbgid, classes, civs, effects, producedBy, unlocks, displayClasses, garrison_classes, type, `unique`, unlockedBy, weapons, attribName, armor,         analytics_game_version,
        aoe_api_version,
        aoe_api_build,
        aoe2world_app_version,
        aoe2world_data_checksum,
        aoe2world_major_version
          FROM Technology
        UNION
        SELECT DISTINCT name, pbgid, classes, civs, effects, producedBy, unlocks, displayClasses, garrison_classes, type, `unique`, unlockedBy, weapons, attribName, armor,         analytics_game_version,
        aoe_api_version,
        aoe_api_build,
        aoe2world_app_version,
        aoe2world_data_checksum,
        aoe2world_major_version
          FROM Ability
        UNION
        SELECT DISTINCT name, pbgid, classes, civs, effects, producedBy, unlocks, displayClasses, garrison_classes, type, `unique`, unlockedBy, weapons, attribName, armor,         analytics_game_version,
        aoe_api_version,
        aoe_api_build,
        aoe2world_app_version,
        aoe2world_data_checksum,
        aoe2world_major_version
          FROM Upgrade
    """
    units = run_query(sql)
    object_types = []
    import json
    types = []
    for row in units:
        ["light", "ranged", "cavalry", "camel"]
        melee = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["Light Melee Cavalry", "melee"])
        ranged = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["ranged"])
        
        cavalry = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["camel", "cavalry"])
        light = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["light"])
        heavy = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["heavy"])
        gunpowder = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["gunpowder"])
        camel = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["camel"])
        archer = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["archer"])
        villager = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["worker"])
        ship = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["ship"])
        religious = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["religious"])
        incendiary = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["incendiary"])
        infantry = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["infantry"])
        siege = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["siege"])
        springald = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["springald"])
        warship = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["warship"])
        khaganate = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["khaganate"])
        mixed = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["mixed"])
        elephant = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["elephant"])
        battle = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["battle"])
        monk = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["monk"])
        hero = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["hero"])
        force = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["force"])
        production = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["production"])
        building = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["building"])
        iv = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["iv"])
        i = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["i"])
        iii = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["iii"])
        ii = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["ii"])
        food = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["food"])
        military = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["military"])
        landmark = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["landmark"])
        influence = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["influence"])
        population = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["population"])
        economic = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["economic"])
        trade = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["trade"])
        passive = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["passive"])
        wonder = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["wonder"])

        farm = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["farm"])
        wood = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["wood"])
        stone = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["stone"])
        contract = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["contract"])
        shinto = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["shinto"])
        mosque = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["mosque"])
        trebuchet = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["trebuchet"])
        longbowman = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["longbowman"])
        buddhist = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["buddhist"])
        imperial = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["imperial"])
        crossbow = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["crossbow"])
        outpost = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["outpost"])
        vision = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["vision"])
        
        hunting = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["hunting"])
        mining = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["mining"])
        tower = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["tower"])
        emplacement = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["emplacement"])
        woodcutting = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["woodcutting"])
        research = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["research"])
        gathering = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["gathering"])
        population = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["population"])
        advance = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["advance"])
        damage = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["damage"])
        naval = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["naval"])
        ram = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["ram"])
        knight = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["knight"])
        grenadier = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["grenadier"])
        packing = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["packing"])
        lancer = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["lancer"])
        defensive = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["defensive"])
        bombard = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["bombard"])
        horseman = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["horseman"])
        horse = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["horse"])
        rider = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["rider"])
        weapon = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["weapon"])
        prelate = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["prelate"])
        scout = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["scout"])
        official = array_contains(arrays=[json.loads(row["displayClasses"]), json.loads(row["classes"])], keys=["official"])
        object_type_unit = 1 if row["type"] == "unit" else 0 
        object_type_technology = 1 if row["type"] == "technology" else 0 
        object_type_ability = 1 if row["type"] == "ability" else 0 
        object_type_upgrade = 1 if row["type"] == "upgrade" else 0 
        object_type_building = 1 if row["type"] == "building" else 0 
        
        isNaval = 1
        isLand = 1
        # isMilitary
        # isCivilian
        # isWorker
        # isSoldier
        # isBuilding
        # isUnit
        # isUpgrade
        # isAbility
        # isTechnology

        # isRanged
        # isMelee
        # isInfantry
        # isCavalry
        # isSiege
        # isShip
        # isLight
        # isHeavy

        # isSpearman
        # isManAtArms
        # isArcher
        # isCavalry
        # UnitCostsGold
        # isHero



        object_types.append({
            "PBGID": row["pbgid"],
            "Category": row["type"].capitalize(),
            "SubCategory": "N/A",
            "Religious": 0,
            "Melee": melee,
            "Ranged": ranged,
            "Cavalry": cavalry,
            "Light": light,
            "Heavy": heavy,
            # "Gunpowder": gunpowder,
            # "Camel": camel,
            "Villager": villager,
            # "Archer": archer,
            # "Ship": ship,
            # "Religious": religious,
            # "Incendiary": incendiary,
            "Infantry": infantry,
            "Siege": siege,
            # "Springald": springald,
            # "Warship": warship,
            # "Khaganate": khaganate,
            # "Mixed": mixed,
            # "Elephant": elephant,
            # "Battle": battle,
            # "Monk": monk,
            # "Hero": hero,
            # "Force": force,
            "Ranged": ranged,
            "Military": military,
            "Civilian": 1 if military == 0 else 0,
            "Unit": object_type_unit,
            "Building": object_type_building,
            "Technology": object_type_technology,
            "Ability": object_type_ability,
            "Upgrade": object_type_unit,
            "Aoe4AnalyticsGameVersion": row["analytics_game_version"],
            "Aoe4ReplayApiVersion": row["aoe_api_version"],
            "Aoe4ReplayApiBuild": row["aoe_api_build"],
            "Aoe4WorldAppVersion": row["aoe2world_app_version"],
            "Aoe4WorldAppDataChecksum": row["aoe2world_data_checksum"],
            "Aoe4WorldDataRepositoryGitCommitHash": row["aoe2world_major_version"],
        })
        types.append(row["type"])
        #types = list(set((row["type"])))
    # print(list(set(types)))
    deduplicated = []
    added = []
    for row in object_types:
        if row["PBGID"] not in added:
            deduplicated.append(row)
            added.append(row["PBGID"])
    return deduplicated

def getSQLGameTimeRows():
    hours = 10
    seconds = []
    from datetime import datetime, timedelta
    
    timestamp = datetime(day=1, year=1, month=1, hour=0, minute=0, second=0)
    for i in range(0, 3600*hours):
        seconds.append({"TotalSecond": i, "Second": timestamp.second, "Minute": timestamp.minute, "Hour": timestamp.hour, "Timestamp": timestamp, "1Minute": timestamp.minute, "5Minute": 5*round(int(timestamp.minute/5)), "2Minute": 2*round(int(timestamp.minute/2)), "10Minute": 10*round(int(timestamp.minute/10))})
        timestamp = timestamp + timedelta(seconds=1)
    return seconds

def getSQLCalendarTimeRows():
    
    seconds = []
    from datetime import datetime, timedelta
    
    timestamp = datetime(day=1, year=1, month=1, hour=0, minute=0, second=0)
    for i in range(0, 3600*24):
        seconds.append({"TotalSecond": i, "Second": timestamp.second, "Minute": timestamp.minute, "Hour": timestamp.hour, "Timestamp": timestamp, "1Minute": timestamp.minute, "5Minute": int(timestamp.minute/5), "2Minute": int(timestamp.minute/2), "10Minute": int(timestamp.minute/10)})
        timestamp = timestamp + timedelta(seconds=1)
    return seconds

def getSQLCalendarDateRows():
    
    seconds = []
    from datetime import datetime, timedelta
    
    timestamp = datetime(day=1, year=2010, month=1, hour=0, minute=0, second=0)
    for i in range(0, 365*20):
        seconds.append({"Day": i, "Year": timestamp.year, "Month": timestamp.month, "Weekday": timestamp.weekday, "Quarter": 1, "WeekNumber": timestamp.strftime("%V"), "WeekdayName": timestamp.strftime("%A"), "Date": timestamp})
        timestamp = timestamp + timedelta(days=1)
    return seconds

def getSQLPlayerAge():
    
    ages = [
        {"AgeNumber": 1, "AgeName": "Stone Age", "AgeLatin": "I", "AgeUpKey": "darkAge"},
        {"AgeNumber": 2, "AgeName": "Feudal Age", "AgeLatin": "II", "AgeUpKey": "feudalAge"},
        {"AgeNumber": 3, "AgeName": "Castle Age", "AgeLatin": "III", "AgeUpKey": "castleAge"},
        {"AgeNumber": 4, "AgeName": "Imperial Age", "AgeLatin": "IV", "AgeUpKey": "imperialAge"},
    ]
    return ages

def getSQLUnit():
    sql = """
        SELECT 
        DISTINCT
             civ_attribName CivilizationAttributeName,
             civ_slug CivilizationSlug,
             civ_name CivilizationName,
             civ_abbr CivilizationAbbreviation,
             costs_stone Stone, 
             costs_food Food, 
             costs_wood Wood,
             costs_gold Gold,
             costs_oliveoil OliveOil,
             costs_vizier VizierPoint,
             costs_total TotalResourcesCost,
             costs_time TimeToProduceSeconds,
             1 Supply,
             sight_line LineOfSight,
             sight_base LineOfSightBase,
             baseId BaseId,
             /*weapons Weapons,*/
             /*armor Armor,*/
             pbgid PBGID,
             age AvaiableAgeId, 
             id ObjectId,
             attribName AttributeName,
             hitpoints Hitpoints,
             producedBy ProducedBy,
             description Description,
             name ObjectName,
             name Name,
             type ObjectNameType,
             description ObjectDescription,
             `unique` IsUniqueToCiv,
             analytics_game_version Aoe4AnalyticsGameVersion,
             aoe_api_version Aoe4ReplayApiVersion,
            aoe_api_build Aoe4ReplayApiBuild,
            aoe2world_app_version Aoe4WorldAppVersion,
            aoe2world_data_checksum Aoe4WorldAppDataChecksum,
            aoe2world_major_version Aoe4WorldMajorVersion,
            aoe4world_data_git_hash Aoe4WorldDataRepositoryGitCommitHash

        FROM Unit
        
    """
    result = run_query(sql)
    # max_weapons = 0
    # for i in result:
    #     if len(i["Weapons"]) > max_weapons:
    #         max_weapons = len(i["Weapons"])
    #         print(i["Weapons"])
    
    return result


def getSQLAbility():
    sql = """
        SELECT 
        DISTINCT
             civ_attribName CivilizationAttributeName,
             civ_slug CivilizationSlug,
             civ_name CivilizationName,
             civ_abbr CivilizationAbbreviation,
             costs_stone Stone, 
             costs_food Food, 
             costs_wood Wood,
             costs_gold Gold,
             costs_oliveoil OliveOil,
             costs_vizier VizierPoint,
             costs_total TotalResourcesCost,
             costs_time TimeToProduceSeconds,
             1 Supply,
             sight_line LineOfSight,
             sight_base LineOfSightBase,
             baseId BaseId,
             /*weapons Weapons,*/
             /*armor Armor,*/
             pbgid PBGID,
             age AvaiableAgeId, 
             id ObjectId,
             attribName AttributeName,
             hitpoints Hitpoints,
             producedBy ProducedBy,
             description Description,
             name ObjectName,
             name Name,
             type ObjectNameType,
             description ObjectDescription,
             `unique` IsUniqueToCiv,
             analytics_game_version Aoe4AnalyticsGameVersion,
             aoe_api_version Aoe4ReplayApiVersion,
            aoe_api_build Aoe4ReplayApiBuild,
            aoe2world_app_version Aoe4WorldAppVersion,
            aoe2world_data_checksum Aoe4WorldAppDataChecksum,
            aoe2world_major_version Aoe4WorldMajorVersion,
            aoe4world_data_git_hash Aoe4WorldDataRepositoryGitCommitHash
             
        FROM Ability
        
    """
    result = run_query(sql)
    # max_weapons = 0
    # for i in result:
    #     if len(i["Weapons"]) > max_weapons:
    #         max_weapons = len(i["Weapons"])
    #         print(i["Weapons"])
    
    return result


def getSQLBuilding():
    sql = """
        SELECT 
            DISTINCT
             civ_attribName CivilizationAttributeName,
             civ_slug CivilizationSlug,
             civ_name CivilizationName,
             civ_abbr CivilizationAbbreviation,
             costs_stone Stone, 
             costs_food Food, 
             costs_wood Wood,
             costs_gold Gold,
             costs_oliveoil OliveOil,
             costs_vizier VizierPoint,
             costs_total TotalResourcesCost,
             costs_time TimeToProduceSeconds,
             0 Supply,
             sight_line LineOfSight,
             sight_base LineOfSightBase,
             baseId BaseId,
             /*weapons Weapons,*/
             /*armor Armor,*/
             pbgid PBGID,
             age AvaiableAgeId, 
             id ObjectId,
             attribName AttributeName,
             hitpoints Hitpoints,
             producedBy ProducedBy,
             description Description,
             name ObjectName,
             name Name,
             type ObjectNameType,
             description ObjectDescription,
             `unique` IsUniqueToCiv,
             analytics_game_version Aoe4AnalyticsGameVersion,
             aoe_api_version Aoe4ReplayApiVersion,
            aoe_api_build Aoe4ReplayApiBuild,
            aoe2world_app_version Aoe4WorldAppVersion,
            aoe2world_data_checksum Aoe4WorldAppDataChecksum,
            aoe2world_major_version Aoe4WorldMajorVersion,
            aoe4world_data_git_hash Aoe4WorldDataRepositoryGitCommitHash
             
        FROM Building
        
    """
    result = run_query(sql)
    # max_weapons = 0
    # for i in result:
    #     if len(i["Weapons"]) > max_weapons:
    #         max_weapons = len(i["Weapons"])
    #         print(i["Weapons"])
    
    return result

def getSQLUpgrade():
    sql = """
        SELECT 
            DISTINCT
             civ_attribName CivilizationAttributeName,
             civ_slug CivilizationSlug,
             civ_name CivilizationName,
             civ_abbr CivilizationAbbreviation,
             costs_stone Stone, 
             costs_food Food, 
             costs_wood Wood,
             costs_gold Gold,
             costs_oliveoil OliveOil,
             costs_vizier VizierPoint,
             costs_total TotalResourcesCost,
             costs_time TimeToProduceSeconds,
             0 Supply,
             sight_line LineOfSight,
             sight_base LineOfSightBase,
             baseId BaseId,
             /*weapons Weapons,*/
             /*armor Armor,*/
             pbgid PBGID,
             age AvaiableAgeId, 
             id ObjectId,
             attribName AttributeName,
             hitpoints Hitpoints,
             producedBy ProducedBy,
             description Description,
             name ObjectName,
             name Name,
             type ObjectNameType,
             description ObjectDescription,
             `unique` IsUniqueToCiv,
             analytics_game_version Aoe4AnalyticsGameVersion,
             aoe_api_version Aoe4ReplayApiVersion,
            aoe_api_build Aoe4ReplayApiBuild,
            aoe2world_app_version Aoe4WorldAppVersion,
            aoe2world_data_checksum Aoe4WorldAppDataChecksum,
            aoe2world_major_version Aoe4WorldMajorVersion,
            aoe4world_data_git_hash Aoe4WorldDataRepositoryGitCommitHash
             
        FROM Upgrade
        
    """
    result = run_query(sql)
    return result

def getSQLTechnology():
    sql = """
        SELECT 
        DISTINCT
             civ_attribName CivilizationAttributeName,
             civ_slug CivilizationSlug,
             civ_name CivilizationName,
             civ_abbr CivilizationAbbreviation,
             costs_stone Stone, 
             costs_food Food, 
             costs_wood Wood,
             costs_gold Gold,
             costs_oliveoil OliveOil,
             costs_vizier VizierPoint,
             costs_total TotalResourcesCost,
             costs_time TimeToProduceSeconds,
             0 Supply,
             sight_line LineOfSight,
             sight_base LineOfSightBase,
             baseId BaseId,
             /*weapons Weapons,*/
             /*armor Armor,*/
             pbgid PBGID,
             age AvaiableAgeId, 
             id ObjectId,
             attribName AttributeName,
             hitpoints Hitpoints,
             producedBy ProducedBy,
             description Description,
             name ObjectName,
             name Name,
             type ObjectNameType,
             description ObjectDescription,
             `unique` IsUniqueToCiv,
             analytics_game_version Aoe4AnalyticsGameVersion,
             aoe_api_version Aoe4ReplayApiVersion,
            aoe_api_build Aoe4ReplayApiBuild,
            aoe2world_app_version Aoe4WorldAppVersion,
            aoe2world_data_checksum Aoe4WorldAppDataChecksum,
            aoe2world_major_version Aoe4WorldMajorVersion,
            aoe4world_data_git_hash Aoe4WorldDataRepositoryGitCommitHash
             
        FROM Technology
        
    """
    result = run_query(sql)
    return result

def getSQLAbility():
    sql = """
        SELECT 
        DISTINCT
            civ_attribName CivilizationAttributeName,
             civ_slug CivilizationSlug,
             civ_name CivilizationName,
             civ_abbr CivilizationAbbreviation,
             costs_stone Stone, 
             costs_food Food, 
             costs_wood Wood,
             costs_gold Gold,
             costs_oliveoil OliveOil,
             costs_vizier VizierPoint,
             costs_total TotalResourcesCost,
             costs_time TimeToProduceSeconds,
             0 Supply,
             sight_line LineOfSight,
             sight_base LineOfSightBase,
             baseId BaseId,
             /*weapons Weapons,*/
             /*armor Armor,*/
             pbgid PBGID,
             age AvaiableAgeId, 
             id ObjectId,
             attribName AttributeName,
             hitpoints Hitpoints,
             producedBy ProducedBy,
             description Description,
             name ObjectName,
             name Name,
             type ObjectNameType,
             description ObjectDescription,
             `unique` IsUniqueToCiv,
             analytics_game_version Aoe4AnalyticsGameVersion,
             aoe_api_version Aoe4ReplayApiVersion,
            aoe_api_build Aoe4ReplayApiBuild,
            aoe2world_app_version Aoe4WorldAppVersion,
            aoe2world_data_checksum Aoe4WorldAppDataChecksum,
            aoe2world_major_version Aoe4WorldMajorVersion,
            aoe4world_data_git_hash Aoe4WorldDataRepositoryGitCommitHash
             
        FROM Ability
        
    """

    result = run_query(sql)
    return result

def add_surrogate_keys(rows:list[dict], surrogate_key:str):
    index = 0
    for row in rows:
        row.update({surrogate_key: index})
        index += 1
    return rows

def run_query(sql:str) -> list[dict]:
    with silver_engine.connect() as connection:
        sql = sql
        tupe_rows = connection.execute(text(sql))
        rows = tupe_rows.fetchall()
        columns = tupe_rows.keys()._keys#.__dir
        result = [{columns[colindex]: row[colindex] for colindex in range(0, len(columns))} for row in rows]
    return result

def insertrows(Table:Base, rows:list[dict]) -> None:
    with gold_engine.connect() as connection:
        #connection.execute(Table.insert)
        connection.execute(delete(Table))
        connection.execute(insert(Table), rows)
        connection.commit()


insertrows(Table=DIM_GAME, rows=add_surrogate_keys(rows=run_query(getSQLDimGame()), surrogate_key="IDGame"))
insertrows(Table=DIM_PLAYER, rows=add_surrogate_keys(rows=run_query(getSQLDimPlayer()), surrogate_key="IDPlayer"))
insertrows(Table=DIM_EVENT_TYPE, rows=add_surrogate_keys(rows=run_query(getSQLDimEventType()), surrogate_key="IDEventType"))

insertrows(Table=DIM_OBJECT_TYPE, rows=add_surrogate_keys(rows=getSQLDimObjectType(), surrogate_key="IDObjectType"))

insertrows(Table=DIM_GAME_TIME, rows=add_surrogate_keys(rows=getSQLGameTimeRows(), surrogate_key="IDGameTime"))
insertrows(Table=DIM_CALENDAR_TIME, rows=add_surrogate_keys(rows=getSQLCalendarTimeRows(), surrogate_key="IDCalendarTime"))
insertrows(Table=DIM_CALENDAR_DATE, rows=add_surrogate_keys(rows=getSQLCalendarDateRows(), surrogate_key="IDCalendarDate"))

insertrows(Table=DIM_PLAYER_AGE, rows=add_surrogate_keys(rows=getSQLPlayerAge(), surrogate_key="IDPlayerAge"))

insertrows(Table=DIM_UNIT, rows=add_surrogate_keys(rows=getSQLUnit(), surrogate_key="IDUnit"))
insertrows(Table=DIM_BUILDING, rows=add_surrogate_keys(rows=getSQLBuilding(), surrogate_key="IDBuilding"))
insertrows(Table=DIM_ABILITY, rows=add_surrogate_keys(rows=getSQLAbility(), surrogate_key="IDAbility"))
insertrows(Table=DIM_UPGRADE, rows=add_surrogate_keys(rows=getSQLUpgrade(), surrogate_key="IDUpgrade"))
insertrows(Table=DIM_TECHNOLOGY, rows=add_surrogate_keys(rows=getSQLTechnology(), surrogate_key="IDTechnology"))
