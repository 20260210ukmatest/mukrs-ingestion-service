from psycopg import Connection
from psycopg.rows import class_row

from models.tournament import Tournament

def get_tournament(conn: Connection, ema_id):
    with conn.cursor(row_factory=class_row(Tournament)) as cur:
        cur.execute(
            """
            select id, ema_id, name, place, country, date, players, mers_weight, mukrs_days, excluded_from_ingestion
            from tournaments
            where ema_id = %s
            """,
            [ema_id])
        return cur.fetchone()