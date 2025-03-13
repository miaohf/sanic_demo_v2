"""
Event system for the application.
Implements a simple publish-subscribe pattern.
"""
import asyncio
from enum import Enum, auto
from typing import Dict, List, Callable, Any

# Define event types
class EventType(Enum):
    USER_CREATED = auto()
    USER_UPDATED = auto()
    USER_DELETED = auto()
    POST_CREATED = auto()
    POST_UPDATED = auto()
    POST_DELETED = auto()
    TAG_CREATED = auto()
    TAG_UPDATED = auto()
    TAG_DELETED = auto()

class EventBus:
    """
    A simple event bus that allows components to subscribe to events
    and publish events to subscribers.
    """
    
    def __init__(self):
        self._subscribers: Dict[EventType, List[Callable]] = {}
        
    def subscribe(self, event_type: EventType, callback=None):
        """
        Subscribe to an event type. Can be used as a decorator or direct method call.
        
        Examples:
            # As direct method call
            event_bus.subscribe(EventType.POST_CREATED, handle_post_created)
            
            # As decorator
            @event_bus.subscribe(EventType.POST_CREATED)
            async def handle_post_created(data):
                pass
        """
        # 用作装饰器
        if callback is None:
            def decorator(func):
                if event_type not in self._subscribers:
                    self._subscribers[event_type] = []
                self._subscribers[event_type].append(func)
                return func
            return decorator
        
        # 直接调用
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
        return callback
        
    def unsubscribe(self, event_type: EventType, callback: Callable[[Any], Any]) -> None:
        """Unsubscribe from an event type."""
        if event_type in self._subscribers and callback in self._subscribers[event_type]:
            self._subscribers[event_type].remove(callback)
            
    async def publish(self, event_type: EventType, data: Any = None) -> None:
        """Publish an event with optional data to all subscribers."""
        if event_type not in self._subscribers:
            return
            
        coroutines = []
        
        for callback in self._subscribers[event_type]:
            if asyncio.iscoroutinefunction(callback):
                coroutines.append(callback(data))
            else:
                callback(data)
                
        if coroutines:
            await asyncio.gather(*coroutines)

# Create a global event bus instance
event_bus = EventBus() 