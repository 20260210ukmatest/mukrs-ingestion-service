from dataclasses import dataclass

@dataclass
class Tournament:
    id: int
    ema_id: int
    name: str
    place: str
    country: str
    date: str
    players: int
    mers_weight: float
    mukrs_days: int
    excluded_from_ingestion: bool