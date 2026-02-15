from dataclasses import dataclass
from datetime import date

from models.create_tournament import CreateTournamentModel

@dataclass(frozen=True)
class TournamentModel:
    id: int
    ema_id: int
    name: str
    place: str
    country: str
    date: date
    players: int
    mers_weight: float
    mukrs_days: int
    excluded_from_ingestion: bool

    def to_create_tournament_model(self) -> CreateTournamentModel:
        return CreateTournamentModel(
            ema_id=self.ema_id,
            name=self.name,
            place=self.place,
            country=self.country,
            date=self.date,
            players=self.players,
            mers_weight=self.mers_weight,
            mukrs_days=self.mukrs_days
        )