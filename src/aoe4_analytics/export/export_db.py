import pandas as pd
import sqlite3

from db import SILVER_DB, STORAGE

dbfilename = f"{STORAGE}{SILVER_DB}"
print(dbfilename)
conn = sqlite3.connect(dbfilename, isolation_level=None,
                        detect_types=sqlite3.PARSE_COLNAMES)

for table in ["GamePlayerResources", "GamePlayerAction", "Technology", "Building", "Unit", "GamePlayerBuildOrder", "Upgrade", "Ability"]:

    
    db_df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    db_df.to_csv(f'export_{table}.csv', index=False)

    # cur = conn.cursor()
    # cur.execute(f'''SELECT * FROM {table}''')
    # rows = cur.fetchall()
    # print(len(rows))