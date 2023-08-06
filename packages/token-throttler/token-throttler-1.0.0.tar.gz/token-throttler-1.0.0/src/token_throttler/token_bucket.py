from datetime import datetime, timezone
from typing import Union


class TokenBucket:
    def __init__(self, replenish_time: int, max_tokens: int) -> None:
        self.replenish_time: int = replenish_time
        self.max_tokens: int = max_tokens
        self.tokens: int = max_tokens
        self.last_replenished: float = datetime.now(timezone.utc).timestamp()
        self.identifier: Union[str, None] = None
        self.cost: int = 0
        self._validate_init()

    def _validate_init(self) -> None:
        if not isinstance(self.replenish_time, int):
            raise TypeError("Invalid `replenish_time` type")
        if not isinstance(self.max_tokens, int):
            raise TypeError("Invalid `max_tokens` type")

    def consume(self) -> bool:
        if self.tokens < self.cost:
            return False

        self.tokens -= self.cost
        return True
