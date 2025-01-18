from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from db import get_aoe4_json_basecols, get_metadata_cols, Base, get_object_base_cols

Base = declarative_base()

def get_patch_metadata_cols():
    return {
        col: Column(String, default=None)
        for col in [
            "Aoe4AnalyticsGameVersion",
            "Aoe4ReplayApiVersion",
            "Aoe4ReplayApiBuild",
            "Aoe4WorldAppVersion",
            "Aoe4WorldAppDataChecksum",
            "Aoe4WorldMajorVersion",
            "Aoe4WorldDataRepositoryGitCommitHash"
            ]
    }

def get_patch_metadata_cols_silver():
    return {
        col: Column(String, default=None)
        for col in [
            "analytics_game_version",
            "aoe_api_version",
            "aoe_api_build",
            "aoe2world_app_version",
            "aoe2world_data_checksum",
            "aoe2world_major_version",
            "aoe4world_data_git_hash"
            ]
    }


# Data
DIM_UNIT = type(
    "DimUnit",
    (Base,),
    {
        "__tablename__": "DimUnit",
        "id": Column(Integer, primary_key=True, autoincrement=True),
        "IDUnit": Column(Integer),
        **get_object_base_cols(),
        **get_metadata_cols(),
        **get_patch_metadata_cols(),
    },
)
DIM_ABILITY = type(
    "DimAbility",
    (Base,),
    {
        "__tablename__": "DimAbility",
        "id": Column(Integer, primary_key=True, autoincrement=True),
        "IDAbility": Column(Integer),
        **get_object_base_cols(),
        **get_metadata_cols(),
        **get_patch_metadata_cols(),
    },
)
DIM_TECHNOLOGY = type(
    "DimTechnology",
    (Base,),
    {
        "__tablename__": "DimTechnology",
        "id": Column(Integer, primary_key=True, autoincrement=True),
        "IDTechnology": Column(Integer),
        **get_object_base_cols(),
        **get_metadata_cols(),
        **get_patch_metadata_cols(),
    },
)
DIM_BUILDING = type(
    "DimBuilding",
    (Base,),
    {
        "__tablename__": "DimBuilding",
        "id": Column(Integer, primary_key=True, autoincrement=True),
        "IDBuilding": Column(Integer),
        **get_object_base_cols(),
        **get_metadata_cols(),
        **get_patch_metadata_cols(),
    },
)
DIM_RESOURCE = type(
    "DimResource",
    (Base,),
    {
        "__tablename__": "DimResource",
        "id": Column(Integer, primary_key=True, autoincrement=True),
        **get_object_base_cols(),
        **get_metadata_cols(),
        **get_patch_metadata_cols(),
    },
)
DIM_UPGRADE = type(
    "DimUpgrade",
    (Base,),
    {
        "__tablename__": "DimUpgrade",
        "id": Column(Integer, primary_key=True, autoincrement=True),
        "IDUpgrade": Column(Integer),
        **get_object_base_cols(),
        **get_metadata_cols(),
        **get_patch_metadata_cols(),
    },
)


GAME_PLAYER_ACTION_TMP = type(
    "GamePlayerActionTmp",
    (Base,),
    {
        "__tablename__": "GamePlayerActionTmp",
        "GamePlayerActionId": Column(Integer, primary_key=True, autoincrement=True),
        **get_metadata_cols(),
        **{
            "gameId": Column(Integer),
            "profileId": Column(Integer),
            "eventTime": Column(Integer),
            "key": Column(Integer),
            "civilizationAttrib": Column(String),
            "civilization": Column(String),
           # "gameVersion": Column(String),
            "gameId": Column(String),
            "winReason": Column(String),
            "mapId": Column(String),
            "mapName": Column(String),
            "mapSize": Column(String),
            "mapSizeMaxPlayers": Column(String),
            "mapBiome": Column(String),
            "mapSeed": Column(String),
            "leaderboard": Column(String),
            "duration": Column(String),
            "startedAt": Column(String),
            "finishedAt": Column(String),
            "spectatorsCount": Column(String),
        
        },
        **get_patch_metadata_cols_silver()
    },
)


GAME_PLAYER_RESOURCES_TMP = type(
    "GamePlayerResourcesTmp",
    (Base,),
    {
        "__tablename__": "GamePlayerResourcesTmp",
        "GamePlayerResourcesId": Column(Integer, primary_key=True, autoincrement=True),
        **get_metadata_cols(),
        **{
            "gameId": Column(Integer),
            "profileId": Column(Integer),
            "timestamp": Column(Integer),
            "food": Column(Integer),
            "gold": Column(Integer),
            "stone": Column(Integer),
            "wood": Column(String),
            "foodPerMin": Column(Integer),
            "goldPerMin": Column(Integer),
            "stonePerMin": Column(Integer),
            "woodPerMin": Column(Integer),
            "foodGathered": Column(Integer),
            "goldGathered": Column(Integer),
            "stoneGathered": Column(Integer),
            "woodGathered": Column(Integer),
            "total": Column(Integer),
            "military": Column(Integer),
            "economy": Column(Integer),
            "technology": Column(Integer),
            "society": Column(Integer),
            "civilizationAttrib": Column(String),
            "civilization": Column(String),
            #"gameVersion": Column(String),
            "gameId": Column(String),
            "winReason": Column(String),
            "mapId": Column(String),
            "mapName": Column(String),
            "mapSize": Column(String),
            "mapSizeMaxPlayers": Column(String),
            "mapBiome": Column(String),
            "mapSeed": Column(String),
            "leaderboard": Column(String),
            "duration": Column(String),
            "startedAt": Column(String),
            "finishedAt": Column(String),
            "spectatorsCount": Column(String),
            # "gameVersion": Column(String),
        },
        **get_patch_metadata_cols_silver()
    },
)


GAME_PLAYER_BUILDORDER_TMP = type(
    "GamePlayerBuildOrderTmp",
    (Base,),
    {
        "__tablename__": "GamePlayerBuildOrderTmp",
        "GamePlayerBuildOrderId": Column(Integer, primary_key=True, autoincrement=True),
        **get_metadata_cols(),
        **{
            "gameId": Column(Integer),
            "profileId": Column(Integer),
            "eventTime": Column(Integer),
            "pbgid": Column(Integer),
            "key": Column(String),
            "icon": Column(String),
            "modid": Column(String),
            "id": Column(String),
            "type": Column(String),
            "civilizationAttrib": Column(String),
            "civilization": Column(String),
            "gameId": Column(String),
            "winReason": Column(String),
            "mapId": Column(String),
            "mapName": Column(String),
            "mapSize": Column(String),
            "mapSizeMaxPlayers": Column(String),
            "mapBiome": Column(String),
            "mapSeed": Column(String),
            "leaderboard": Column(String),
            "duration": Column(String),
            "startedAt": Column(String),
            "finishedAt": Column(String),
            "spectatorsCount": Column(String),

        },
        **get_patch_metadata_cols_silver(),
    },
)


GAME_PLAYER_AGEUPS_TMP = type(
    "GamePlayerAgeupsTmp",
    (Base,),
    {
        "__tablename__": "GamePlayerAgeupsTmp",
        "GamePlayerAgeupsTmpId": Column(Integer, primary_key=True, autoincrement=True),
        **get_metadata_cols(),
        **{
            "GameId": Column(Integer),
            "ProfileId": Column(Integer),
            "IDGameTime": Column(Integer),
            "AgeKey": Column(String),
        },
        **get_patch_metadata_cols_silver(),
    },
)

DIM_PLAYER_AGE = type(
    "DimPlayerAge",
    (Base,),
    {
        "__tablename__": "DimPlayerAge",
        "id": Column(Integer, primary_key=True, autoincrement=True),
        "IDPlayerAge": Column(Integer),
        "AgeName": Column(String),
        "AgeLatin": Column(String),
        "AgeUpKey": Column(String),
        "AgeNumber": Column(Integer),
        **get_metadata_cols(),
        **get_patch_metadata_cols(),
    },
)

# Hardcoded
DIM_OBJECT_TYPE = type(
    "DimObjectType",
    (Base,),
    {
        "__tablename__": "DimObjectType",
        "id": Column(Integer, primary_key=True, autoincrement=True),
        "IDObjectType": Column(Integer),
        "PBGID": Column(Integer),
        
        "Category": Column(String),
        "SubCategory": Column(String),
        
        "Religious": Column(Integer),
        "Infantry": Column(Integer),
        "Cavalry": Column(Integer),
        "Villager": Column(Integer),
        "Siege": Column(Integer),

        "Ranged": Column(Integer),
        "Melee": Column(Integer),
        
        "Military": Column(Integer),
        "Civilian": Column(Integer),

        "Unit": Column(Integer),
        "Building": Column(Integer),
        "Technology": Column(Integer),
        "Ability": Column(Integer),

        "Gunpowder": Column(Integer),
        "Camel": Column(Integer),
        "Archer": Column(Integer),
        "Villager": Column(Integer),
        "Ship": Column(Integer),
        "Incendiary": Column(Integer),
        "Springald": Column(Integer),
        "Warship": Column(Integer),
        "Khaganate": Column(Integer),
        "Mixed": Column(Integer),
        "Elephand": Column(Integer),
        "Battle": Column(Integer),
        "Monk": Column(Integer),
        "Hero": Column(Integer),
        "Force": Column(Integer),
        **get_metadata_cols(),
        **get_patch_metadata_cols(),
    },
)
DIM_GAME_VERSION = type(
    "DimGameVersion",
    (Base,),
    {
        "__tablename__": "DimGameVersion",
        "id": Column(Integer, primary_key=True, autoincrement=True),
        "IDGameVersion": Column(Integer),
        "PatchKey": Column(String),
        **{},
        **get_metadata_cols(),
        **get_patch_metadata_cols(),
    },
)
DIM_CALENDAR_DATE = type(
    "DimCalendarDate",
    (Base,),
    {
        "__tablename__": "DimCalendarDate",
        "id": Column(Integer, primary_key=True, autoincrement=True),
        "IDCalendarDate": Column(Integer),
        "Day": Column(Integer),
        "Month": Column(Integer),
        "Year": Column(Integer),
        "Quarter": Column(Integer),
        "WeekdayName": Column(String),
        "WeekNumber": Column(String),
        "Date": Column(DateTime),
        **{},
        **get_metadata_cols(),
        **get_patch_metadata_cols(),
    },
)

DIM_CALENDAR_TIME = type(
    "DimCalendarTime",
    (Base,),
    {
        "__tablename__": "DimCalendarTime",
        "id": Column(Integer, primary_key=True, autoincrement=True),
        "IDCalendarTime": Column(Integer),
        "Second": Column(Integer),
        "Minute": Column(Integer),
        "Hour": Column(Integer),
        "Timestamp": Column(DateTime),
        **{},
        **get_metadata_cols(),
        **get_patch_metadata_cols(),
    },
)

# Game
DIM_MAPTYPE = type(
    "DimMapType",
    (Base,),
    {
        "__tablename__": "DimMapType",
        "id": Column(Integer, primary_key=True, autoincrement=True),
        "IDMapType": Column(Integer),
        
        "PlayerCount": Column(Integer),
        "Size": Column(String),
        
        **get_metadata_cols(),
        **get_patch_metadata_cols(),
    },
)
DIM_GAME = type(
    "DimGame",
    (Base,),
    {
        "__tablename__": "DimGame",
        "id": Column(Integer, primary_key=True, autoincrement=True),
        "IDGame": Column(Integer),
        "GameId": Column(Integer),
        "Duration": Column(Integer),
        "MapType": Column(Integer),
        "Started": Column(Integer),
        "StartedDateTime": Column(DateTime),
        "FinishedDateTime": Column(DateTime),
        **get_metadata_cols(),
        **get_patch_metadata_cols(),
    },
)
DIM_PLAYER = type(
    "DimPlayer",
    (Base,),
    {
        "__tablename__": "DimPlayer",
        "id": Column(Integer, primary_key=True, autoincrement=True),
        "IDPlayer": Column(Integer),
        "PlayerId": Column(Integer),
        "PlayerName": Column(String),
        
        **get_metadata_cols(),
        **get_patch_metadata_cols(),
    },
)
DIM_PLAYER_CIVILIZATION = type(
    "DimPlayerCivilization",
    (Base,),
    {
        "__tablename__": "DimPlayerCivilization",
        "id": Column(Integer, primary_key=True, autoincrement=True),
        "IDPlayerCivilization": Column(Integer),
        "Name": Column(Integer),
        **get_metadata_cols(),
        **get_patch_metadata_cols(),
    },
)
DIM_EVENT_TYPE = type(
    "DimEventType",
    (Base,),
    {
        "__tablename__": "DimEventType",
        "id": Column(Integer, primary_key=True, autoincrement=True),
        "IDEventType": Column(Integer),
        "EventKey": Column(String),
        "EventCategory": Column(String),
        "EventSubcategory": Column(String),
        "PBGID": Column(Integer),
        "CivilizationAttributeName": Column(String),
        
        **get_metadata_cols(),
        **get_patch_metadata_cols(),
    },
)
DIM_GAME_TIME = type(
    "DimGameTime",
    (Base,),
    {
        "__tablename__": "DimGameTime",
        "id": Column(Integer, primary_key=True, autoincrement=True),
        "IDGameTime": Column(Integer),
        "TotalSecond": Column(Integer),
        "Second": Column(Integer),
        "Minute": Column(Integer),
        "Hour": Column(Integer),
        "5Minute": Column(Integer),
        "1Minute": Column(Integer),
        "2Minute": Column(Integer),
        "10Minute": Column(Integer),
        "Timestamp": Column(Integer),
        
        **get_metadata_cols(),
        **get_patch_metadata_cols(),
    },
)
FACT_RESOURCE_BALANCE = type(
    "FactResourceBalance",
    (Base,),
    {

        "__tablename__": "FactResourceBalance",
        "id": Column(Integer, primary_key=True, autoincrement=True),
        "IDGame": Column(Integer),
        "GamePlayerBuildOrderId": Column(Integer),
        "IDPlayer": Column(Integer),
        "IDMapType": Column(Integer),
        "IDPlayerAge": Column(Integer),

        "IDEventType": Column(Integer),
        "IDGameTime": Column(Integer),
        "IDCalendarDate": Column(Integer),
        "IDCalendarTime": Column(Integer),
        "IDUnit": Column(Integer),
        "IDTechnology": Column(Integer),
        "IDAbility": Column(Integer),
        "IDBuilding": Column(Integer),
        "MaxIDDataDim": Column(Integer),
        "IDUpgrade": Column(Integer),
        "Amount": Column(Integer),
        "GoldStockpile": Column(Integer),
        "WoodStockpile": Column(Integer),
        "StoneStockpile": Column(Integer),
        "FoodStockpile": Column(Integer),
        "VizierPointStockpile": Column(Integer),
        "OliveOilStockpile": Column(Integer),
        "Supply": Column(Integer),
        "IDGameVersion": Column(Integer),
        "IDObjectType": Column(Integer),
        "IDPlayerCivilization": Column(Integer),
        "Count": Column(Integer),
        
        **get_metadata_cols(),
        **get_patch_metadata_cols(),
    },
)

from db import get_engine, GOLD_DB


def init_gold_database():
    Base.metadata.create_all(get_engine(dbname=GOLD_DB))
