import os
import json
from db import get_engine, BRONZE_DB, declarative_base

GAMESDIR = "games"
PLAYERDIR = "players"

    # print(gamefile)
# from bronze_db import GAME

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer,Float,DateTime, String, MetaData

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from sqlalchemy import insert

# with get_engine(dbname=BRONZE_DB).connect() as conn:
#      result = conn.execute(
#          insert(GAME),
#          [
#              {"JsonRaw": "{}"},
#          ],
#      )
#      conn.commit()


# from sqlalchemy import select
# stmt = select(GAME).where(GAME.c.JsonRaw == "spongebob")
class Base(DeclarativeBase):
    pass

# class Game(Base):
#      __tablename__ = "Game"
#      Id = Column(Integer, primary_key=True)
#      JsonRaw = Column(Integer, primary_key=True)

from db_bronze import GAME, PLAYER, TECHNOLOGY, UNIT, BUILDING, ABILITY, UPGRADE
from constants import CIVS

engine = get_engine(dbname=BRONZE_DB)

from db_bronze import init_database
init_database()

with engine.connect() as conn:
    gamefiles = os.listdir(GAMESDIR)
    for gamefile in [os.path.join(GAMESDIR, file) for file in gamefiles]:
        filecontent = json.load(open(gamefile, "r"))
        result = conn.execute(
            insert(GAME),
            [
                {"JsonRaw": json.dumps(filecontent)},
            ],
        )

    playerfiles = os.listdir(PLAYERDIR)
    for file in [os.path.join(PLAYERDIR, file) for file in playerfiles]:
        filecontent = json.load(open(file, "r"))
        result = conn.execute(
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
            result = conn.execute(
                insert(data_table),
                [
                    {"JsonRaw": json.dumps(filecontent)}, # __IngestionDate, __SourceFile, __SourceSystem
                ],
            )
    conn.commit()

