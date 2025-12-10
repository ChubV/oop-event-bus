from typing import Dict, List, Optional

from .event import Event
from .event_listener import EventListener


class EventBus:
    __listeners: Dict[str, List[EventListener]]

    def __init__(self, listeners: Optional[List[EventListener]] = None) -> None:
        self.__listeners = {}
        if not listeners:
            return
        for listener in listeners:
            self.listen(listener)

    def listen(self, listener: EventListener):
        event_name = listener.get_event_name()
        event_names = listener.get_event_names()
        if event_name:
            event_names.append(event_name)
        for name in event_names:
            if name not in self.__listeners:
                self.__listeners[name] = []

            self.__listeners[name].append(listener)

    async def dispatch(self, event: Event):
        if event.get_name() not in self.__listeners:
            return

        listeners = self.__listeners[event.get_name()]
        for listener in listeners:
            await listener(event)
