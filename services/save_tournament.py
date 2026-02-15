from psycopg import Connection
from psycopg.rows import scalar_row
from models.tournament import Tournament

def __get_player_id(
        conn: Connection,
        ema_number: str | None,
        first_name: str,
        last_name: str) -> int | None:
    with conn.cursor(row_factory=scalar_row) as cur:
        if ema_number:
            cur.execute(
                "select id from players where ema_number = %s;",
                [ema_number])
            return cur.fetchone()

        cur.execute(
            "select id from players where first_name = %s and last_name = %s",
            (first_name, last_name)
        )
        return cur.fetchone()

def __create_player(
        conn: Connection,
        first_name: str,
        last_name: str,
        country: str,
        ema_number: str | None) -> int:
    with conn.cursor(row_factory=scalar_row) as cur:
        cur.execute(
            """
            insert into players (ema_number, first_name, last_name, country) 
            values (%s, %s, %s, %s)
            returning id
            """,
            (ema_number, first_name, last_name, country))
        return next(cur)

def __create_tournament(conn: Connection, tournament_info: Tournament) -> int:
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
        player_base_ranks: list) -> None:
    for player in player_base_ranks:
        ema_number = player['ema_number']
        last_name = player['last_name']
        first_name = player['first_name']
        country = player['country']
        base_rank = player['base_rank']
        if base_rank == "-" or base_rank == "N/A":
            continue
        player_id = __get_player_id(conn, ema_number, first_name, last_name)
        if player_id is None:
            player_id = __create_player(conn, first_name, last_name, country, ema_number)
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tournament_results (tournament_id, player_id, base_rank) 
                VALUES (%s, %s, %s)
                """,
                (tournament_id, player_id, base_rank)
            )
        
def save_tournament(
        conn: Connection,
        tournament_info: Tournament,
        player_base_ranks: list) -> None:
    tournament_id = __create_tournament(conn, tournament_info)
    __insert_tournament_results(conn, tournament_id, player_base_ranks)