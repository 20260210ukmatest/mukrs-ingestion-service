from psycopg import Connection
from psycopg.rows import class_row

from models.tournament import TournamentModel

def get_tournament(conn: Connection, id: int) -> TournamentModel | None:
    with conn.cursor(row_factory=class_row(TournamentModel)) as cur:
        cur.execute(
            """
            select id, ema_id, name, place, country, date, players, mers_weight, mukrs_days, excluded_from_ingestion
            from tournaments
            where id = %s
            """,
            [id])
        return cur.fetchone()