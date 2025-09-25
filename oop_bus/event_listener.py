from abc import ABC, abstractmethod
from typing import List, Optional

from .event import Event


class EventListener(ABC):
    @abstractmethod
    async def __call__(self, event: Event): ...

    def get_event_name(self) -> Optional[str]:
        return None

    def get_event_names(self) -> List[str]:
        return []
