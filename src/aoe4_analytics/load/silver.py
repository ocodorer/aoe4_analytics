import os
import json
from db import get_engine, SILVER_DB, BRONZE_DB, declarative_base


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from sqlalchemy import insert, select


class Base(DeclarativeBase):
    pass


from db_bronze import (
    GAME,
    PLAYER,
    TECHNOLOGY as TECHNOLOGY_BRONZE,
    UNIT as UNIT_BRONZE,
    BUILDING as BUILDING_BRONZE,
    ABILITY as ABILITY_BRONZE,
    UPGRADE as UPGRADE_BRONZE,
)
from db_silver import (
    GAME_PLAYER_STATS,
    GAME_PLAYER_RESOURCES,
    GAME_PLAYER_ACTION,
    GAME_PLAYER_BUILDORDER,
    TECHNOLOGY as TECHNOLOGY_SILVER,
    UNIT as UNIT_SILVER,
    BUILDING as BUILDING_SILVER,
    ABILITY as ABILITY_SILVER,
    UPGRADE as UPGRADE_SILVER,
    GAME_PLAYER
)
from constants import CIVS

patch_map = json.load(open("patch_map.json", "r"))

current_patch = patch_map[0]

bronze_engine = get_engine(dbname=BRONZE_DB)
silver_engine = get_engine(dbname=SILVER_DB)

from db_bronze import init_database

init_database()

from db_silver import init_silver_database as init_silver_db

init_silver_db()

with bronze_engine.connect() as conn:
    games = conn.execute(select(GAME.id, GAME.JsonRaw)).fetchall()


resources = []
actions_rows = []
buildOrder = []
allgameplayers = []
with silver_engine.connect() as conn:

    # print(rows[3])

    for game_row in games:
        payload = json.loads(game_row[1])
        # print(payload.keys())

        # game_version = payload["_recentGameHash"]["patch"]["app_version"]
        # print(game_version)   

        game = {
            key: payload[key]
            for key in [
                "gameId",
                "winReason",
                "mapId",
                "mapName",
                "mapSize",
                "mapSizeMaxPlayers",
                "mapBiome",
                "mapSeed",
                "duration",
                "startedAt",
                "finishedAt",
                "spectatorsCount",
                "leaderboard",
            ]
        }
        game.update(current_patch)
        #allgames.append(game)
        

        for player in payload.get("players"):
            player_rows = {
                key: player[key]
                for key in [
                    "profileId",
                    "name",
                    "civilization",
                    "team",
                    "teamName",
                    "apm",
                    "result",
                    "civilizationAttrib",
                ]
            }
            player_rows.update(game)
            allgameplayers.append(player_rows)

            for key, items in player["actions"].items():
                
                for row in items:
                    
                    
                    actions_rows.append(
                        {
                            "key": key,
                            "eventTime": row,
                            "profileId": player["profileId"],
                            "gameId": payload["gameId"],
                            "civilizationAttrib": player["civilizationAttrib"],
                            "civilization": player["civilization"],
                            
                            "gameId": payload["gameId"],
                            "winReason": payload["winReason"],
                            "mapId": payload["mapId"],
                            "mapName": payload["mapName"],
                            "mapSize": payload["mapSize"],
                            "mapSizeMaxPlayers": payload["mapSizeMaxPlayers"],
                            "mapBiome": payload["mapBiome"],
                            "mapSeed": payload["mapSeed"],
                            "leaderboard": payload["leaderboard"],
                            "duration": payload["duration"],
                            "startedAt": payload["startedAt"],
                            "finishedAt": payload["finishedAt"],
                            "spectatorsCount": payload["spectatorsCount"],
                            **current_patch,
                        }
                    )

            for item in player["buildOrder"]:
                for key in [
                    "finished",
                    "constructed",
                    "packed",
                    "unpacked",
                    "transformed",
                    "destroyed",
                ]:
                    for event_timestamp in item[key]:
                        buildOrder.append(
                            {
                                "key": key,
                                "eventTime": event_timestamp,
                                "pbgid": item["pbgid"],
                                "icon": item["icon"],
                                "modid": item["modid"],
                                "id": item["id"],
                                "type": item["type"],
                                "profileId": player["profileId"],
                                "gameId": payload["gameId"],
                                "civilizationAttrib": player["civilizationAttrib"],
                                "civilization": player["civilization"],
                                
                                "gameId": payload["gameId"],
                                "winReason": payload["winReason"],
                                "mapId": payload["mapId"],
                                "mapName": payload["mapName"],
                                "mapSize": payload["mapSize"],
                                "mapSizeMaxPlayers": payload["mapSizeMaxPlayers"],
                                "mapBiome": payload["mapBiome"],
                                "mapSeed": payload["mapSeed"],
                                "leaderboard": payload["leaderboard"],
                                "duration": payload["duration"],
                                "startedAt": payload["startedAt"],
                                "finishedAt": payload["finishedAt"],
                                "spectatorsCount": payload["spectatorsCount"],
                                **current_patch,
                            }
                        )

            timestamps = player["resources"]["timestamps"]
            for index in range(0, len(timestamps)):
                resources.append(
                    {
                        "key": key,
                        "index": index,
                        
                        

                        "timestamp": timestamps[index],
                        **{
                            key: player["resources"][key][index]
                            for key in ["food", "wood", "gold", "stone"]
                        },
                        **{
                            key: player["resources"][key][index]
                            for key in [
                                "foodPerMin",
                                "goldPerMin",
                                "stonePerMin",
                                "woodPerMin",
                            ]
                        },
                        **{
                            key: player["resources"][key][index]
                            for key in [
                                "foodGathered",
                                "woodGathered",
                                "goldGathered",
                                "stoneGathered",
                            ]
                        },
                        "profileId": player["profileId"],
                        "gameId": payload["gameId"],
                        "civilizationAttrib": player["civilizationAttrib"],
                        "civilization": player["civilization"],
                        
                        "gameId": payload["gameId"],
                        "winReason": payload["winReason"],
                        "mapId": payload["mapId"],
                        "mapName": payload["mapName"],
                        "mapSize": payload["mapSize"],
                        "mapSizeMaxPlayers": payload["mapSizeMaxPlayers"],
                        "mapBiome": payload["mapBiome"],
                        "mapSeed": payload["mapSeed"],
                        "leaderboard": payload["leaderboard"],
                        "duration": payload["duration"],
                        "startedAt": payload["startedAt"],
                        "finishedAt": payload["finishedAt"],
                        "spectatorsCount": payload["spectatorsCount"],
                        **current_patch,
                        

                    }
                )
    
    conn.execute(insert(GAME_PLAYER_RESOURCES), resources)
    conn.execute(insert(GAME_PLAYER_ACTION), actions_rows)
    conn.execute(insert(GAME_PLAYER_BUILDORDER), buildOrder)
    conn.execute(insert(GAME_PLAYER), allgameplayers)
    # # conn.execute(
    # #     insert(GAME_PLAYER_RESOURCES), resources

    # # )
    conn.commit()

    # conn.commit()

from collections.abc import MutableMapping


def flatten_dict(
    d: MutableMapping, parent_key: str = "", sep: str = "."
) -> MutableMapping:
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# load AOE4 World data repository
payload_keys = []
classes = []

for bronze_table, silver_table in [
    (UNIT_BRONZE, UNIT_SILVER),
    (TECHNOLOGY_BRONZE, TECHNOLOGY_SILVER),
    (UPGRADE_BRONZE, UPGRADE_SILVER),
    (ABILITY_BRONZE, ABILITY_SILVER),
    (BUILDING_BRONZE, BUILDING_SILVER),
]:
    with bronze_engine.connect() as conn:
        rows = conn.execute(select(bronze_table.id, bronze_table.JsonRaw)).fetchall()

        index = 0
    silver_data = []

    for row in rows:

        payload = json.loads(row[1])

        #print(payload["civ"])
        #{'name': 'Abbasid Dynasty', 'abbr': 'ab', 'slug': 'abbasid', 'attribName': 'abbasid', 'expansion': ['base']}
        #exit()

        for row_index in range(0, len(payload["data"])):
            variation_index = 0
            new_row = {
                "civ_name": payload["civ"]["name"],
                "civ_abbr": payload["civ"]["abbr"],
                "civ_slug": payload["civ"]["slug"],
                "civ_attribName": payload["civ"]["attribName"],
                "active": None,
                "auraRange": None,
                "unlockedBy": None,
                "effects": None,
                "costs_wood": None,
                "classes": None,
                "costs_time": None,
                "civs": None,
                "age": None,
                "id": None,
                "sight_inner_height": None,
                "icon": None,
                "attribName": None,
                "costs_popcap": None,
                "sight_inner_radius": None,
                "costs_oliveoil": None,
                "hitpoints": None,
                "movement_speed": None,
                "producedBy": None,
                "sight_outer_radius": None,
                "costs_food": None,
                "displayClasses": None,
                "sight_height": None,
                "type": None,
                "costs_gold": None,
                "costs_vizier": None,
                "description": None,
                "name": None,
                "costs_stone": None,
                "unique": None,
                "sight_line": None,
                "sight_base": None,
                "sight_outer_height": None,
                "costs_total": None,
                "baseId": None,
                "weapons": None,
                "armor": None,
                "pbgid": None,
                "civ": "",
            }
            flat = flatten_dict(payload["data"][row_index], sep="_")

            new_row.update(flat)
            new_row.update(current_patch)
            for key, value in new_row.items():
                
                if type(new_row[key]) in [list, dict]:
                    new_row[key] = json.dumps(new_row[key])

            silver_data.append(new_row)
            #payload_keys = list(set(payload_keys + list(flat.keys())))
            #classes = list(set(classes + list(flat["classes"])))
            index += 1
    # print(len(silver_data))

    with silver_engine.connect() as conn:
        
        conn.execute(insert(silver_table), silver_data)
        conn.commit()

#print(classes)

