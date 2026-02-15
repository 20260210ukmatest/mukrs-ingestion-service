from psycopg import Connection
from psycopg.rows import scalar_row
from models.create_tournament import CreateTournamentModel
from models.tournament import TournamentModel

def __should_save_tournament(
        conn: Connection,
        existing_tournament_info: TournamentModel | None,
        new_tournament_info: CreateTournamentModel,
        new_tournament_results: dict[int, int]) -> bool:
    if existing_tournament_info is None:
        return True
    existing_tournament_info_as_create_model = existing_tournament_info.to_create_tournament_model()
    if existing_tournament_info_as_create_model.__hash__() != new_tournament_info.__hash__():
        return True
    existing_tournament_results = __get_tournament_results(conn, existing_tournament_info.id)
    return existing_tournament_results != new_tournament_results
      
def __get_tournament_results(conn: Connection, tournament_id: int) -> dict[int, int]:
    with conn.cursor() as cur:
        cur.execute(
            """
            select player_id, base_rank from tournament_results where tournament_id = %s
            """,
            [tournament_id]
        )
        return {row[0]: row[1] for row in cur.fetchall()}

def __insert_tournament(conn: Connection, tournament_info: CreateTournamentModel) -> int:
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

def unmark_older_tournament_as_latest(conn: Connection, id: int) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE tournaments
            SET is_latest = false
            WHERE id = %s
            """,
            [id]
        )

def save_tournament(
        conn: Connection,
        existing_tournament_info: TournamentModel | None,
        tournament_info: CreateTournamentModel,
        tournament_results: dict[int, int]) -> None:
    if not __should_save_tournament(conn, existing_tournament_info, tournament_info, tournament_results):
        print(f"Tournament with id {tournament_info.ema_id} already exists and has not changed, skipping save")
        return
    tournament_id = __insert_tournament(conn, tournament_info)
    __insert_tournament_results(conn, tournament_id, tournament_results)
    if existing_tournament_info is not None:
        unmark_older_tournament_as_latest(conn, existing_tournament_info.id)