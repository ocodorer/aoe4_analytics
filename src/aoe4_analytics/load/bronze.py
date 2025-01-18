import os
import json
from src.aoe4_analytics.database.db_bronze import get_engine, BRONZE_DB, declarative_base, GAME, PLAYER, TECHNOLOGY, UNIT, BUILDING, ABILITY, UPGRADE, init_database
from src.aoe4_analytics.constants import CIVS, GAMESDIR, PLAYERDIR



from sqlalchemy import create_engine
from sqlalchemy import Column, Integer,Float,DateTime, String, MetaData

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from sqlalchemy import insert

class Base(DeclarativeBase):
    pass

def main():

    engine = get_engine(dbname=BRONZE_DB)

    init_database()

    with engine.connect() as conn:
        gamefiles = os.listdir(GAMESDIR)
        for gamefile in [os.path.join(GAMESDIR, file) for file in gamefiles]:
            filecontent = json.load(open(gamefile, "r"))
            conn.execute(
                insert(GAME),
                [
                    {"JsonRaw": json.dumps(filecontent)},
                ],
            )

        playerfiles = os.listdir(PLAYERDIR)
        for file in [os.path.join(PLAYERDIR, file) for file in playerfiles]:
            filecontent = json.load(open(file, "r"))
            conn.execute(
                insert(PLAYER),
                [
                    {"JsonRaw": json.dumps(filecontent)},
                ],
            )

        for data_table, source_folder in [
            (TECHNOLOGY, "technologies"),
            (UNIT, "units"),
            (ABILITY, "abilities"),
            (BUILDING, "buildings"),
            (UPGRADE, "upgrades"),
            ]:
            for civ in CIVS:
                filecontent = json.load(open(os.path.join("..", "data", source_folder, f"{civ}.json"), "r"))
                conn.execute(
                    insert(data_table),
                    [
                        {"JsonRaw": json.dumps(filecontent)}, # __IngestionDate, __SourceFile, __SourceSystem
                    ],
                )
        conn.commit()

