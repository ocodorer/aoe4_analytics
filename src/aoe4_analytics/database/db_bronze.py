
from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base
from db import get_aoe4_json_basecols, get_metadata_cols, Base, get_engine, BRONZE_DB

Base = declarative_base() # **get_base_cols(), **get_metadata_cols()

# Bronze
GAME = type("Game", (Base,), {"__tablename__": "Game", "id": Column(Integer, primary_key=True, autoincrement=True) , **get_aoe4_json_basecols(), **get_metadata_cols()})
PLAYER = type("Player", (Base,), {"__tablename__": "Player", "id": Column(Integer, primary_key=True, autoincrement=True) , **get_aoe4_json_basecols()})
TECHNOLOGY = type("Technology", (Base,), {"__tablename__": "Technology", "id": Column(Integer, primary_key=True, autoincrement=True) , **get_aoe4_json_basecols()})
UNIT = type("Unit", (Base,), {"__tablename__": "Unit", "id": Column(Integer, primary_key=True, autoincrement=True) , **get_aoe4_json_basecols()})
BUILDING = type("Building", (Base,), {"__tablename__": "Building", "id": Column(Integer, primary_key=True, autoincrement=True) , **get_aoe4_json_basecols()})
UPGRADE = type("Upgrade", (Base,), {"__tablename__": "Upgrade", "id": Column(Integer, primary_key=True, autoincrement=True) , **get_aoe4_json_basecols()})
ABILITY = type("Ability", (Base,), {"__tablename__": "Ability", "id": Column(Integer, primary_key=True, autoincrement=True) , **get_aoe4_json_basecols()})

def init_database():
    Base.metadata.create_all(get_engine(dbname=BRONZE_DB))

