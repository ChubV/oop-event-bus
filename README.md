Intro
===

This package implements an event bus based on the Mediator pattern. 
It is a powerful tool to avoid coupling and make components work together 
without any knowledge about each other (loose coupling). It helps:

- to avoid unneeded dependencies;
- to make testing easier;
- to extend the functionality by adding (not changing) the units;
- to reduce the tech debt.

Installation
===

`pip install oop-event-bus`

Usage
===

Create an event class with all the details you need
```python
class UserSignedIn(Event):
    def __init__(self, email: Email):
        self.email = email
```

Create and register event listeners

```python
class LogSignedInUsersListener(TypedEventListener[UserSignedIn]):
    async def __call__(self, event: UserSignedIn):
        ...

event_bus = EventBus()
event_bus.listen(LogSignedInUsersListener())
```

Dispatch an event

```python
await event_bus.dispatch(UserSignedIn(user.email))
```

### Multi-listener

It is possible to register the listener to be called
for more than one event:

```python
class MyMultiEventListener(MultiEventListener):
    def get_event_names(self) -> List[str]:
        return [TestEvent.__name__, TestEvent2.__name__]

    async def on_test_event(self, event: TestEvent):
        ...
    
    async def on_test_event2(self, event: TestEvent2):
        ...

...
event_bus.listen(MyMultiEventListener())
event_bus.dispatch(TestEvent2(...))
```

Example
===

Given the following code:

```python
class SomethingService:
    def __init__(self, logger: Logger, mailer: Mailer, marketing: MarketingService):
        self.logger = logger
        self.mailer = mailer
        self.marketing = marketing
        
    async def do_something(self):
        self._real()
        self._business()
        self._logic()

        #side effects
        self.logger.info("We did something")

        await self.mailer.send_email("Welcome email")

        #unrelated code that should be executed when we do something
        await self.marketing.increase_marketing_counter()
```

There are SRP breaks, and a number of side effects unrelated to the business problem. This code is hard to test, it 
couples the `SomethingService` with the concrete implementations of logging, mailing and marketing services.

With `oop-event-bus` you can move all side effects and unrelated code out. 
Also, you will make it possible to extend functionality later without changing the code of this method.

```python
from oop_bus import Event, EventBus

class WeDidSomething(Event):
    ...

class SomethingService:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
    async def do_something(self):
        real()
        business()
        logic()

        await self.event_bus.dispatch(WeDidSomething())
```

You can see that every piece of non-related code was replaced with the single `event_bus` call here.