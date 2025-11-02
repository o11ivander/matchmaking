from dataclasses import dataclass
from typing import Optional


@dataclass
class Player:
    id: str
    skill: Optional[int] = 0
    squad_id: Optional[int] = None

    def __str__(self):
        return (
            f"Player(id): [{self.id}] | skill: {self.skill} | group(id): [{self.squad_id}]"
            if self.squad_id is not None
            else f"Player(id): [{self.id}] | skill: {self.skill}"
        )


@dataclass
class Squad:
    avg_skill: float
    id: int
    cnt_players: int
    players: list[Player]
