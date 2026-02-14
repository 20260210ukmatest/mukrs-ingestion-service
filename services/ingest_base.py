import bs4
import psycopg

from services.clean_ema_data import clean_ema_data
from services.download_from_ema import download_from_ema
from services.get_dbconn import get_dbconn
from services.parse_tournament_info import parse_tournament_info
from services.parse_tournament_results import parse_tournament_results
from services.save_tournament import save_tournament

def ingest(ema_id, earliest_date_to_ingest=None):
    print(f"Ingesting tournament id {ema_id}")
    text = download_from_ema(ema_id)
    cleaned_text = clean_ema_data(ema_id, text)
    soup = bs4.BeautifulSoup(cleaned_text, 'html.parser')
    tournament_info = parse_tournament_info(soup)
    if earliest_date_to_ingest and tournament_info['date'].date() < earliest_date_to_ingest:
        print(f"Did not ingest tournament id {ema_id}, stopping ingestion")
        return False
    player_base_ranks = parse_tournament_results(soup)
    DBCONN = get_dbconn()
    with psycopg.connect(DBCONN) as conn:
        with conn.cursor() as cur:
            save_tournament(cur, tournament_info, player_base_ranks)
    return True