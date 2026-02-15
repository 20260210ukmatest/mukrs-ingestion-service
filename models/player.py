from dataclasses import dataclass

@dataclass(frozen=True)
class Player:
    id: int
    first_name: str
    last_name: str
    country: str
    ema_number: str | None
