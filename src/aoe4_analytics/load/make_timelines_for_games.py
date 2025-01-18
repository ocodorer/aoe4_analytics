

from gold2 import gold_engine 
from sqlalchemy import text
from gold2 import gold_engine,silver_engine
from sqlalchemy import insert, select, delete

with silver_engine.connect() as conn:
    # conn.execute(delete(GAME_PLAYER_AGEUPS_TMP))
    result = conn.execute(text("SELECT DISTINCT gameId, profileId, duration FROM GamePlayer"))

for gameId, profileId, game_duration in result:
    print(gameId, profileId, game_duration)
    sql = f"""
    WITH

    data AS (
        SELECT * FROM (SELECT profileId, gameId, 'darkAge' `key`, 0 eventTime FROM GamePlayerActionTmp WHERE profileId = {profileId} AND gameId = {gameId} LIMIT 1

        ) T
        UNION
        SELECT profileId, gameId, `key`, eventTime FROM GamePlayerActionTmp
        WHERE profileId = {profileId} AND gameId = {gameId} and `key` IN (NULL, 'feudalAge', 'castleAge', 'imperialAge')
        UNION
        /*The last time shoudlbe from game duration*/
        SELECT * FROM (SELECT profileId, gameId, NULL `key`, {game_duration} eventTime FROM GamePlayerActionTmp WHERE profileId = {profileId} AND gameId = {gameId} LIMIT 1
        ) T2
    )
    ,LastDate AS (
        SELECT `key` AgeUpKey, profileId, gameId, MAX(eventTime) MaxDate FROM data
        GROUP BY profileId, gameId
    ), Source AS (
    SELECT  eventTime
            ,LEAD(eventTime, 1, (SELECT MaxDate FROM LastDate)) OVER(
                    ORDER BY eventTime
            ) AS NextTime
            ,gameId
            ,profileId
            ,`key`
        FROM data
    ), date_series_with_ageups AS (
        SELECT Source.NextTime
            ,DimGameTime.IDGameTime
            ,Source.gameId
            ,Source.profileId
            ,Source.`key`
        FROM Source
            LEFT JOIN DimGameTime
            ON DimGameTime.TotalSecond BETWEEN Source.eventTime AND Source.NextTime
    ORDER BY IDGameTime ASC
    )
    INSERT INTO  GamePlayerAgeupsTmp (IDGameTime, GameId, ProfileId, AgeKey)  SELECT IDGameTime, gameId GameId, profileId ProfileId, `key` AgeKey FROM date_series_with_ageups

    """

    with gold_engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
