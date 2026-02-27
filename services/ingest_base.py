import bs4
import psycopg

from datetime import date
from psycopg import OperationalError
from tenacity import retry, retry_if_exception_type, wait_fixed, stop_after_attempt

from services.clean_ema_data import clean_ema_data
from services.download_from_ema import download_from_ema
from services.get_dbconn import get_dbconn
from services.get_latest_tournament_id import get_latest_tournament_id
from services.get_tournament import get_tournament
from services.parse_tournament_info import parse_tournament_info
from services.parse_tournament_results import parse_tournament_results
from services.resolve_players_in_tournament_results import resolve_players_in_tournament_results
from services.save_tournament import save_tournament

@retry(retry=retry_if_exception_type(OperationalError), wait=wait_fixed(45), stop=stop_after_attempt(3))
def ingest(ema_id: int, earliest_date_to_ingest: None | date = None) -> bool:
    DBCONN = get_dbconn()
    with psycopg.connect(DBCONN) as conn:
        latest_tournament_id = get_latest_tournament_id(conn, ema_id)
        if latest_tournament_id is None:
            existing_tournament_info = None
        else:
            existing_tournament_info = get_tournament(conn, latest_tournament_id)
            if existing_tournament_info is not None and existing_tournament_info.excluded_from_ingestion:
                print(f"Tournament with id {ema_id} is excluded from ingestion, skipping")
                return True
        text = download_from_ema(ema_id)
        cleaned_text = clean_ema_data(ema_id, text)
        soup = bs4.BeautifulSoup(cleaned_text, 'html.parser')
        tournament_info = parse_tournament_info(soup)
        if earliest_date_to_ingest and tournament_info.date < earliest_date_to_ingest:
            print(f"Tournament id {ema_id} is too long ago, stopping ingestion")
            return False
        print(f"Ingesting tournament id {ema_id}")
        unresolved_tournament_results = parse_tournament_results(soup)
        tournament_results = resolve_players_in_tournament_results(conn, unresolved_tournament_results)
        save_tournament(conn, existing_tournament_info, tournament_info, tournament_results)
        return True