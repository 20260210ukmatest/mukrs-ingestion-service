from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Tournament:
    id: int
    ema_id: int
    name: str
    place: str
    country: str
    date: datetime
    players: int
    mers_weight: float
    mukrs_days: int
    excluded_from_ingestion: bool