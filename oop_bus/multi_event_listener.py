from functools import reduce

from oop_bus import Event, EventListener


class MultiEventListener(EventListener):
    async def __call__(self, event: Event):
        event_name_snake_case = reduce(
            lambda x, y: x + ("_" if y.isupper() else "") + y,
            event.get_name().split(".")[-1],
        ).lower()
        method_name = f"on_{event_name_snake_case}"
        apply_method = getattr(self, method_name)
        await apply_method(event)
