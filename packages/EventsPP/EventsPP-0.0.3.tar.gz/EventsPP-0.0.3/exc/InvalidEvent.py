class InvalisEvent(Exception):
    __slots__ = '__event'

    def __init__(self, event):
        self.__event = event

    def __str__(self):
        return self.__event + ' is not a valid event'
