from psycopg import Connection
from psycopg.rows import scalar_row
from models.tournament import Tournament
from models.player import Player

def __get_player_id(
        conn: Connection,
        player: Player) -> int | None:
    with conn.cursor(row_factory=scalar_row) as cur:
        if player.ema_number:
            cur.execute(
                "select id from players where ema_number = %s;",
                [player.ema_number])
            return cur.fetchone()

        cur.execute(
            "select id from players where first_name = %s and last_name = %s",
            (player.first_name, player.last_name)
        )
        return cur.fetchone()

def __create_player(
        conn: Connection,
        player: Player) -> int:
    with conn.cursor(row_factory=scalar_row) as cur:
        cur.execute(
            """
            insert into players (ema_number, first_name, last_name, country) 
            values (%s, %s, %s, %s)
            returning id
            """,
            (player.ema_number, player.first_name, player.last_name, player.country))
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
        player_base_ranks: dict[Player, int]) -> None:
    for player in player_base_ranks.keys():
        base_rank = player_base_ranks[player]
        player_id = __get_player_id(conn, player)
        if player_id is None:
            player_id = __create_player(conn, player)
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
        player_base_ranks: dict[Player, int]) -> None:
    tournament_id = __create_tournament(conn, tournament_info)
    __insert_tournament_results(conn, tournament_id, player_base_ranks)