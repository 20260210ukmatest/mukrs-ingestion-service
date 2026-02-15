import bs4
import psycopg

from datetime import date

from services.clean_ema_data import clean_ema_data
from services.download_from_ema import download_from_ema
from services.get_dbconn import get_dbconn
from services.get_tournament import get_tournament
from services.parse_tournament_info import parse_tournament_info
from services.parse_tournament_results import parse_tournament_results
from services.save_tournament import save_tournament

def ingest(ema_id: int, earliest_date_to_ingest: None | date = None) -> bool:
    DBCONN = get_dbconn()
    with psycopg.connect(DBCONN) as conn:
        existing_tournament_info = get_tournament(conn, ema_id)
        if existing_tournament_info is not None and existing_tournament_info.excluded_from_ingestion:
            print(f"Tournament with id {ema_id} is excluded from ingestion, skipping")
            return True
        text = download_from_ema(ema_id)
        cleaned_text = clean_ema_data(ema_id, text)
        soup = bs4.BeautifulSoup(cleaned_text, 'html.parser')
        tournament_info = parse_tournament_info(soup)
        if earliest_date_to_ingest and tournament_info.date.date() < earliest_date_to_ingest:
            print(f"Tournament id {ema_id} is too long ago, stopping ingestion")
            return False
        print(f"Ingesting tournament id {ema_id}")
        player_base_ranks = parse_tournament_results(soup)
        save_tournament(conn, tournament_info, player_base_ranks)
        return True