from dataclasses import dataclass

@dataclass(frozen=True)
class TournamentResult:
    tournament_id: int
    player_id: int
    base_rank: int