from functools import wraps
from exc.InvalidEventTypeError import InvalidEventTypeError
from exc.InvalidEvent import InvalisEvent


def event_driven(*events):
    return EventManager(*events).events


class EventManager:

    __slots__ = '__events'


    def __init__(self, *events):
         self.__create_events(*events)


    @staticmethod
    def call(event, *args, **kwargs):
        if event is not None:
            return event(*args, **kwargs)

    @staticmethod
    def make_event(func, doc):

        if not ((func is None) or callable(func)):
            raise InvalidEventTypeError()

        @wraps(func)
        def decorated(*args, **kwargs):
            return EventManager.call(func, *args, **kwargs)

        decorated.__doc__ = doc
        decorated.__name__ = 'NoneFunction' if func is None else func.__name__
        decorated.__qualname__ = 'NoneFunction' if func is None else func.__qualname__
        return decorated


    def __create_events(self, *events):
        self.__events = type('Events', (object, ), {})

        for name, doc in events:
            self.__set_event(name, doc)


    def __set_event(self, name, doc):
        def getter(self):
            return getattr(self, '_'+name)

        def set_(self, f):
            setattr(self, '_'+name, EventManager.make_event(f, getattr(self, '_'+name).__doc__))

        setattr(self.__events, 'set_'+name, set_)
        setattr(self.__events, '_'+name, self.make_event(None, doc))
        setattr(self.__events, name, property(getter))


    @property
    def events(self):
        return self.__events
