from psycopg import Connection
from psycopg.rows import scalar_row
from models.player import PlayerModel

def __get_player_id(
        conn: Connection,
        player: PlayerModel) -> int | None:
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
    
def __insert_player(
        conn: Connection,
        player: PlayerModel) -> int:
    with conn.cursor(row_factory=scalar_row) as cur:
        cur.execute(
            """
            insert into players (ema_number, first_name, last_name, country) 
            values (%s, %s, %s, %s)
            returning id
            """,
            (player.ema_number, player.first_name, player.last_name, player.country))
        return next(cur)
    
def __resolve_player(
        conn: Connection,
        player: PlayerModel) -> int:
    player_id = __get_player_id(conn, player)
    if player_id is None:
        player_id = __insert_player(conn, player)
    return player_id

def resolve_players_in_tournament_results(
        conn: Connection,
        player_base_ranks: dict[PlayerModel, int]) -> dict[int, int]:
    return {__resolve_player(conn, player): base_rank for player, base_rank in player_base_ranks.items()}