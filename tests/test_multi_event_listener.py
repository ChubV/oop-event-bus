from typing import List

import pytest

from oop_bus import Event, EventBus
from oop_bus.multi_event_listener import MultiEventListener


class TestEvent(Event): ...


class TestEvent2(Event): ...


class MyMultiEventListener(MultiEventListener):
    def __init__(self):
        self.test1_called = False
        self.test2_called = False

    def get_event_names(self) -> List[str]:
        return [TestEvent.__name__, TestEvent2.__name__]

    async def on_test_event(self, event: TestEvent):
        if isinstance(event, TestEvent):
            self.test1_called = True

    async def on_test_event2(self, event: TestEvent2):
        if isinstance(event, TestEvent2):
            self.test2_called = True


class TestMultiEventListener:
    @pytest.mark.asyncio
    async def test_it_should_call_different_methods(self):
        bus = EventBus()
        event = TestEvent()
        event2 = TestEvent2()
        listener = MyMultiEventListener()
        bus.listen(listener)

        await bus.dispatch(event)
        await bus.dispatch(event2)

        assert listener.test1_called
        assert listener.test2_called
