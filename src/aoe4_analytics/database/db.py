
import sqlite3
from os import remove, path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Double, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

from sqlalchemy import Column, Integer,Float,DateTime, String, MetaData
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import declarative_base
metadata = MetaData()

engine = create_engine('sqlite:///test.db', echo=True)
STORAGE = "/home/oadmin/oetl/storage/"
BRONZE_DB = "bronze.sqlite"
SILVER_DB = "silver.sqlite"
GOLD_DB = "gold.sqlite"
# GOLD_DB = path.join(STORAGE, "storage", "gold.sqlite")
METADATA_COLS = [
      ('__AddedDate', 'VARCHAR')
]


# def initialize_sqlite_table(name:str, database:str, cols, surrogate_key:str): 
#     conn = sqlite3.connect(path.join(STORAGE, f'{database}.sqlite'))
#     cur = conn.cursor()
#     cur.execute(f'CREATE TABLE {name} ({surrogate_key} INT, {','.join(f'{colname} {dtype}' for colname, dtype in cols)}, {','.join(f'{colname} {dtype}' for colname, dtype in METADATA_COLS)});')

from datetime import datetime


def get_object_base_cols():
    return {
            'NormalizedId': Column(String),
            'PBGID': Column(Integer),

            'CivilizationAbbreviation': Column(String),
            'CivilizationSlug': Column(String),
            'CivilizationAttributeName': Column(String),
            
            'ObjectId': Column(Integer),
            'ObjectName': Column(String),
            'ObjectNameType': Column(String),
            'ObjectDescription': Column(String),

            'ObjectId': Column(Integer),
            'BaseId': Column(Integer),
            'Name': Column(String),
            'AttributeName': Column(String),
            'Description': Column(String),
            'AvaiableAgeId': Column(Integer),
            'Hitpoints': Column(Integer),

            'Food': Column(Integer),
            'Gold': Column(Integer),
            'Wood': Column(Integer),
            'Stone': Column(Integer),
            'AgeId': Column(Integer),
            'VizierPoint': Column(Integer),
            'OliveOil': Column(Integer),
            'Total': Column(Integer),
            'Supply': Column(Integer),
            'Armor': Column(String),
            'Weapon': Column(String),
    }

def get_aoe4_json_basecols():
    return {
          "JsonRaw": Column(String)
      }



class Base(DeclarativeBase):
    pass


def get_engine(dbname):
    return create_engine(f"sqlite:///{STORAGE}{dbname}", echo=False)


def get_metadata_cols():
    return {
        '__AddedDate': Column(DateTime),
        '__AddedYear': Column(Integer),
        '__AddedMonth': Column(Integer),
        '__AddedDay': Column(Integer),
        '__SourceFile': Column(String),
    }



def init_database(db_name:str, config:dict) -> None: 
    engine = create_engine("sqlite:///" + db_name, echo=False)
    Base = declarative_base()
    tables = {}
    for tablename, surrogate_key, base_attributes in config:
        base_attributes.update({"__tablename__": tablename, surrogate_key: Column(Integer, primary_key=True, autoincrement=True)})
        base_attributes.update(get_metadata_cols())
        tables[tablename] = type(tablename, (Base,), base_attributes)
    Base.metadata.create_all(engine)


