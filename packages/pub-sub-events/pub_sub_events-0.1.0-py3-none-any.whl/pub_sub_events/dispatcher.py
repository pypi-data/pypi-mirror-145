from functools import wraps
from typing import Callable, Set, Tuple, Any
from .publisher import Publisher
import inspect


def dispatch_events_output(events: Set[str]) -> Callable:
    def _decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Callable:
            result = func(*args, **kwargs)

            for event in events:
                Publisher().dispatch(event, result)

            return result

        return wrapper

    return _decorator


def dispatch_events_input(events: Set[str]) -> Callable:
    """
    The message that will be dispatched to the Publisher should be the first attr,
    it doesn't matter if it's a named parameter or not.
    Examples:
        def fn(attr:str) ...
        fn("my_message")
        the message send to the Publisher will be "my_message"
        class MyClass:
            def method(self, message:str, stuff:str)...
        MyClass().method(message="my_message", stuff="stuff")
        the message send to the Publisher will be "my_message"
    This has the same behavior for functions, static_methods, class_methods and
    instance_methods.It will ignore "self" attr to instance_methods and "cls" attr to
    class_methods and get its first attr.
    Returns:
    """

    def _decorated(fun: Callable) -> Callable:
        desc = next((desc for desc in (staticmethod, classmethod)
                     if isinstance(fun, desc)), None)
        if desc:
            fun = fun.__func__

        @wraps(fun)
        def wrap(*args, **kwargs) -> Any:
            result = fun(*args, **kwargs)

            _, no_self_args = _extract_args(fun, *args)

            if len(no_self_args) != 0:
                message = no_self_args[0]
            else:
                message = next(iter(kwargs.values()))

            for event in events:
                Publisher().dispatch(event, message)

            return result

        wrap.original = fun

        if desc:
            wrap = desc(wrap)
        return wrap

    return _decorated


def _extract_args(fun: Callable, *args: Any) -> Tuple[None, Any]:
    if len(args):
        met = getattr(args[0], fun.__name__, None)
        if met:
            wrap = getattr(met, '__func__', None)
            if getattr(wrap, 'original', None) is fun:
                maybe_cls = args[0]
                cls = maybe_cls if inspect.isclass(maybe_cls) else maybe_cls.__class__
                return cls, args[1:]
    return None, args
