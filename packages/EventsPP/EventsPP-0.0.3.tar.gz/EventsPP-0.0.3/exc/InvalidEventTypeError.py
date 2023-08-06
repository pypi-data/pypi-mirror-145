class InvalidEventTypeError(Exception):
    def __str__(self):
        return 'Events must be function type or None'
