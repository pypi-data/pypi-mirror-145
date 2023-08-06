class EventNotRegisteredError(Exception):
    def __init__(self, event_name: str) -> None:
        msg = f"No event called '{event_name}' registered."
        super().__init__(msg)
