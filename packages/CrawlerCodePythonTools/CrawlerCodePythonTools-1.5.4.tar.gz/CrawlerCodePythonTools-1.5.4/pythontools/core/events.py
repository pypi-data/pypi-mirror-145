from pythontools.core import logger
from threading import Thread
import traceback


class Event:

    def __init__(self, name, function, scope="global", threaded=False):
        self.name = name
        self.function = function
        self.scope = scope
        self.threaded = threaded

    def call(self, *args, **kwargs):
        if self.threaded is True:
            Thread(target=self.function, args=args, kwargs=kwargs).start()
        else:
            self.function(*args, **kwargs)


events = []


def register_event(event):
    events.append(event)


def unregister_event(event):
    for e in events:
        if e == event:
            events.remove(e)


def call(name, *args, scope="global", **kwargs):
    try:
        for event in events:
            if event.name == name and event.scope == scope:
                event.call(*args, **kwargs)
    except Exception as e:
        logger.log(f"§cEvent '{name}' throw exception: {e}")
        traceback.print_exc()


# --- deprecated --- #
registerEvent = register_event
unregisterEvent = unregister_event
# --- deprecated --- #
