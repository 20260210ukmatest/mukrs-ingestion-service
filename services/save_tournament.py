from psycopg import Connection
from psycopg.rows import scalar_row
from entities.tournament import Tournament

def __insert_tournament(conn: Connection, tournament_info: Tournament) -> int:
    with conn.cursor(row_factory=scalar_row) as cur:
        cur.execute(
            """
            insert into tournaments (ema_id, name, place, country, date, players, mers_weight, mukrs_days) 
            values (%s, %s, %s, %s, %s, %s, %s, %s)
            returning id
            """,
            (
                tournament_info.ema_id,
                tournament_info.name,
                tournament_info.place,
                tournament_info.country,
                tournament_info.date,
                tournament_info.players,
                tournament_info.mers_weight,
                tournament_info.mukrs_days
            )
        )
        return next(cur)

def __insert_tournament_results(
        conn: Connection,
        tournament_id: int,
        tournament_results: dict[int, int]) -> None:
    for player_id in tournament_results.keys():
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tournament_results (tournament_id, player_id, base_rank) 
                VALUES (%s, %s, %s)
                """,
                (tournament_id, player_id, tournament_results[player_id])
            )
        
def save_tournament(
        conn: Connection,
        tournament_info: Tournament,
        tournament_results: dict[int, int]) -> None:
    tournament_id = __insert_tournament(conn, tournament_info)
    __insert_tournament_results(conn, tournament_id, tournament_results)