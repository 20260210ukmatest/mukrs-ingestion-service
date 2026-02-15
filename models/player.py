from dataclasses import dataclass

@dataclass(frozen=True)
class PlayerDto:
    first_name: str
    last_name: str
    country: str
    ema_number: str | None
