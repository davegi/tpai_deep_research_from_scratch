import asyncio
from typing import Callable, Dict, List, Any, Coroutine


class MCPStub:
    """Very small in-process async message bus for tests.

    Usage:
        bus = MCPStub()
        bus.register_handler("topic", handler)
        await bus.publish("topic", message)
    """

    def __init__(self) -> None:
        self._handlers: Dict[str, List[Callable[[Any], Coroutine[Any, Any, None]]]] = {}

    def register_handler(self, topic: str, handler: Callable[[Any], Coroutine[Any, Any, None]]) -> None:
        self._handlers.setdefault(topic, []).append(handler)

    async def publish(self, topic: str, message: Any) -> None:
        handlers = list(self._handlers.get(topic, []))
        if not handlers:
            return
        # Fire all handlers concurrently and wait
        await asyncio.gather(*(h(message) for h in handlers))
