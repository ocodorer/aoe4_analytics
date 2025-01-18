import pandas as pd
import sqlite3

from db import GOLD_DB, STORAGE

dbfilename = f"{STORAGE}{GOLD_DB}"
print(dbfilename)
conn = sqlite3.connect(
    dbfilename, isolation_level=None, detect_types=sqlite3.PARSE_COLNAMES
)

for table in [
    "DimPlayer",
    "DimTechnology",
    "DimUpgrade",
    "FactResourceBalance",
    "DimGameTime",
    "DimCalendarTime",
    "DimCalendarDate",
    "DimObjectType",
    "DimEventType",
    "DimUnit",
    "DimBuilding",
    "DimAbility",
    "DimUpgrade",
    "DimResource",
    "DimPlayerAge",
    "DimGameVersion",
    "DimMapType",
    "DimGame",
]:

    db_df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    db_df.to_csv(f"export/{table}.csv", index=False)

    # cur = conn.cursor()
    # cur.execute(f'''SELECT * FROM {table}''')
    # rows = cur.fetchall()
    # print(len(rows))
