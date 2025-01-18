from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from db import (
    get_aoe4_json_basecols,
    get_metadata_cols,
    Base,
    get_object_base_cols,
    SILVER_DB,
    init_database,
    get_engine,
)

Base = declarative_base()  # **get_base_cols(), **get_metadata_cols()

def get_patch_metadata_cols():
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



def get_object_base_cols():
    return {
        col: Column(String, default=None)
        for col in [
            "costs_wood",
            "classes",
            "costs_time",
            "civs",
            "age",
            "id",
            "sight_inner_height",
            "icon",
            "auraRange",
            "attribName",
            "costs_popcap",
            "sight_inner_radius",
            "costs_oliveoil",
            "effects",
            "hitpoints",
            "movement_speed",
            "unlocks",
            "producedBy",
            "sight_outer_radius",
            "active",
            "costs_food",
            "displayClasses",
            "garrison_classes",
            "sight_height",
            "type",
            "costs_gold",
            "costs_vizier",
            "description",
            "name",
            "costs_stone",
            "unique",
            "sight_line",
            "sight_base",
            "unlockedBy",
            "garrison_capacity",
            "sight_outer_height",
            "costs_total",
            "baseId",
            "weapons",
            "armor",
            "pbgid",
            "civ_name",
            "civ_abbr",
            "civ_slug",
            "civ_attribName",
        ]
    }

# Bronze
GAME_PLAYER = type(
    "GamePlayer",
    (Base,),
    {
        "__tablename__": "GamePlayer",
        "id": Column(Integer, primary_key=True, autoincrement=True),
        **get_aoe4_json_basecols(),
        **get_metadata_cols(),
        **{
            "gameId": Column(Integer),
            "profileId": Column(Integer),
            "bprod": Column(String),
            "gt": Column(String),
            "inactperiod": Column(Integer),
            "gameId": Column(Integer),
            "winReason": Column(String),
            "mapId": Column(Integer),
            "mapName": Column(String),
            "mapSize": Column(String),
            "mapSizeMaxPlayers": Column(String),
            "mapBiome": Column(String),
            "mapSeed": Column(Integer),
            "duration": Column(Integer),
            "startedAt": Column(Integer),
            "finishedAt": Column(Integer),
            "spectatorsCount": Column(Integer),
            "leaderboard": Column(String),
        },
        **get_patch_metadata_cols()
    },
)


GAME_PLAYER_STATS = type(
    "GamePlayerStats",
    (Base,),
    {
        "__tablename__": "GamePlayerStats",
        "id": Column(Integer, primary_key=True, autoincrement=True),
        **get_aoe4_json_basecols(),
        **get_metadata_cols(),
        **{
            "gameId": Column(Integer),
            "profileId": Column(Integer),
            "bprod": Column(Integer),
            "gt": Column(Integer),
            "inactperiod": Column(Integer),
            "totalcmds": Column(String),
        },
        **get_patch_metadata_cols()
    },
)

GAME_PLAYER_RESOURCES = type(
    "GamePlayerResources",
    (Base,),
    {
        "__tablename__": "GamePlayerResources",
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
        **get_patch_metadata_cols()
    },
)


GAME_PLAYER_BUILDORDER = type(
    "GamePlayerBuildOrder",
    (Base,),
    {
        "__tablename__": "GamePlayerBuildOrder",
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
        **get_patch_metadata_cols()
    },
)



GAME_PLAYER_ACTION = type(
    "GamePlayerAction",
    (Base,),
    {
        "__tablename__": "GamePlayerAction",
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
        **get_patch_metadata_cols()
    },
)


TECHNOLOGY = type(
    "Technology",
    (Base,),
    {
        "__tablename__": "Technology",
        "TechnologyId": Column(Integer, primary_key=True, autoincrement=True),
        **get_object_base_cols(),
        **get_patch_metadata_cols()
    },
)
UNIT = type(
    "Unit",
    (Base,),
    {
        "__tablename__": "Unit",
        "UnitId": Column(Integer, primary_key=True, autoincrement=True),
        **get_object_base_cols(),
        **get_patch_metadata_cols()
    },
)
BUILDING = type(
    "Building",
    (Base,),
    {
        "__tablename__": "Building",
        "BuildingId": Column(Integer, primary_key=True, autoincrement=True),
        **get_object_base_cols(),
        **get_patch_metadata_cols()
    },
)
UPGRADE = type(
    "Upgrade",
    (Base,),
    {
        "__tablename__": "Upgrade",
        "UpgradeId": Column(Integer, primary_key=True, autoincrement=True),
        **get_object_base_cols(),
        **get_patch_metadata_cols()
    },
)
ABILITY = type(
    "Ability",
    (Base,),
    {
        "__tablename__": "Ability",
        "AbilityId": Column(Integer, primary_key=True, autoincrement=True),
        **get_object_base_cols(),
        **get_patch_metadata_cols()
    },
)



def init_silver_database():
    Base.metadata.create_all(get_engine(dbname=SILVER_DB))
