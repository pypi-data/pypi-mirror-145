from typing import Dict, Callable, Any

from .errors import EventNotRegisteredError
from .i_subscriber import Subscriber
import contextlib
from threading import Lock


class PublisherMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Publisher(metaclass=PublisherMeta):
    def __init__(self) -> None:
        self._events: Dict[str, Dict[Subscriber, Callable]] = {}

    def get_subscribers(self, event: str) -> Dict[Subscriber, Callable]:
        try:
            return self._events[event]
        except KeyError:
            raise EventNotRegisteredError(event)

    def register(self, event: str, subscriber: Subscriber, callback: Callable = None) -> None:
        if not callback:
            callback = getattr(subscriber, 'execute')

        if self._events.get(event, None):
            self._events[event][subscriber] = callback
            return

        self._events[event] = {subscriber: callback}

    def unregister(self, event: str, subscriber: Subscriber) -> None:
        with contextlib.suppress(KeyError):
            del self.get_subscribers(event)[subscriber]

    def dispatch(self, event: str, message: Any) -> None:
        subscribers = self.get_subscribers(event)
        for _, callback in subscribers.items():
            callback(message)
