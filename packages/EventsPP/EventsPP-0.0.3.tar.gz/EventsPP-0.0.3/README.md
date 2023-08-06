# Package Events++

## Classes
### Events
This class is runtime created and its purpose is to be inhereted by the event-driven
target class. It has the following structure:

    class Events:
        def _event1(...):
            # Implementation...

        @property
        def event1(self):
            return self._event1

        @event1.setter
        def event1(self, value):
            self._event1 = EventManager.make_event(value)

        def _event2(...):
            # Implementation...

        @property
        def event2(self):
            return self._event1

        @event2.setter
        def event1(self, value):
            self._event2 = EventManager.make_event(value)

        ...

### EventManager
This class builds the **_Events_** class, which must be inherited by the event-driven
target class. Its implementation is omitted in this tutorial for it is not relevant
for the package usage.

### event_driven function
This function gets events names-docstring tuples as attributes, creates an
**_EventManager_** instance and returns an **_Events_** class ready to be inherited.

Example:

    events_class = event_driven(
                        ('event1', '...'),
                        ('event2', '...'),
                        ('event3', '...'),
                        ...
                    )


### Usage example

    class TargetClass(event_driven(('event1', '...'), ('event2', '...'))):
        __slots__ = 'baa', 'foo'

        def __init__(self):
            # Implementation...

        def foo_maker(self, value):
            self.baa = self.event2(baa)
            self.foo = self.event1(value, self.baa)

When an event is declared, it is created as **_None_**, so that nothing will happen
during the execution of **_self.event2_**, nor **_self.event1(value, self.baa)_**.
Furthermore, even though **_None_** is not callable, when an event is None, it is
simply not called, no exception is called.

    target_instance = TargetClass()

    @target_instance.set_event1
    def new_event1(self, *args):
        # Implementation...

    @target_instance.set_event2
    def new_event2(self, baa):
        # Implementation...



Those lines would change **_event1_** and **_event2_** behaviour for
**_target_instance_**. Although it is not a rule, it is undoubtedly a good habit to
use docstring to events for the TargetClass implementation probably expects
**_event1_** and **_event2_** to have specific arguments, or none.