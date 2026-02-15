from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class CreateTournamentModel:
    ema_id: int
    name: str
    place: str
    country: str
    date: date
    players: int
    mers_weight: float
    mukrs_days: int