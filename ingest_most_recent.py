from datetime import datetime, timedelta
from services.get_most_recent_tournament_ema_id import get_most_recent_tournament_ema_id
from services.ingest_base import ingest

if __name__ == '__main__':
    today = datetime.now().date()
    earliest_date_to_ingest = today - timedelta(days=180)
    ema_id = get_most_recent_tournament_ema_id()
    ingestion_continuing = True
    while ingestion_continuing:
        ingestion_continuing = ingest(ema_id, earliest_date_to_ingest) and ema_id > 0
        ema_id -= 1