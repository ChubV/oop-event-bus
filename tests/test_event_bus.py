from typing import List

import pytest

from oop_bus import Event, EventBus, EventListener, TypedEventListener


class TestEvent(Event): ...


class TestEvent2(Event): ...


class MyMultiEventListener(EventListener):
    def __init__(self):
        self.called_events = []

    def get_event_names(self) -> List[str]:
        return [TestEvent.__name__, TestEvent2.__name__]

    async def __call__(self, event: Event):
        self.called_events.append(event)


class EventListenerForTest(TypedEventListener[TestEvent]):
    def __init__(self):
        self.called = 0

    async def __call__(self, event: TestEvent):
        self.called += 1


class TestEventBus:
    @pytest.mark.asyncio
    async def test_it_should_run_listeners_for_event(self):
        bus = EventBus()
        event = TestEvent()

        listener1 = EventListenerForTest()
        listener2 = EventListenerForTest()

        bus.listen(listener1)
        bus.listen(listener2)

        await bus.dispatch(event)

        assert listener1.called == 1
        assert listener2.called == 1

    @pytest.mark.asyncio
    async def test_it_should_not_run_listener_if_event_differs(self):
        bus = EventBus()
        event = Event()

        listener1 = EventListenerForTest()
        listener2 = EventListenerForTest()

        bus.listen(listener1)
        bus.listen(listener2)

        await bus.dispatch(event)

        assert listener1.called == 0
        assert listener2.called == 0

    @pytest.mark.asyncio
    async def test_it_should_run_single_listener_for_multiple_events(self):
        bus = EventBus()
        event = TestEvent()
        event2 = TestEvent2()
        listener = MyMultiEventListener()
        bus.listen(listener)

        await bus.dispatch(event)
        await bus.dispatch(event2)

        assert listener.called_events == [event, event2]
