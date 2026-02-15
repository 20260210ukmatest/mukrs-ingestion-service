from psycopg import Connection
from psycopg.rows import scalar_row

def get_latest_tournament_id(conn: Connection, ema_id: int) -> int | None:
    with conn.cursor(row_factory=scalar_row) as cur:
        cur.execute(
            """
            select id
            from tournaments
            where ema_id = %s
            and is_latest = true
            """,
            [ema_id])
        return cur.fetchone()