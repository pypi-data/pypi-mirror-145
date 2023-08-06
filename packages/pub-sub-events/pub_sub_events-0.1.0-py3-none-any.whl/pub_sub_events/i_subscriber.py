from typing import Any, Protocol


class Subscriber(Protocol):

    def execute(self, message: Any) -> None:  # pragma: no cover
        pass
