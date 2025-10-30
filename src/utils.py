from random import randint
from uuid import uuid4


def generate_users(cnt: int) -> list[dict]:
    return [
        {
            "id": str(uuid4()),
            "skill": randint(1, 100),
        }
        for i in range(cnt)
    ]
