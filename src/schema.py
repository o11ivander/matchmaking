from dataclasses import dataclass
from typing import Optional


@dataclass
class Player:
    id: str
    skill: Optional[int] = 0
    group: Optional[str] = None

    def __str__(self):
        return (
            f"Player(id): [{self.id}] | skill: {self.skill} | group(id): [{self.group}]"
            if self.group is not None
            else f"Player(id): [{self.id}] | skill: {self.skill}"
        )
