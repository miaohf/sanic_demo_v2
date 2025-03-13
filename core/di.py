"""
Simple dependency injection system.
Provides a way to manage and inject dependencies.
"""
from typing import Dict, Type, TypeVar, Any, Callable, Optional, get_type_hints

T = TypeVar('T')

class Container:
    """A simple dependency injection container."""
    
    def __init__(self):
        self._services: Dict[Type, Any] = {}
        
    def register(self, service_type: Type[T], instance: T) -> None:
        """Register a service instance."""
        self._services[service_type] = instance
        
    def resolve(self, service_type: Type[T]) -> Optional[T]:
        """Resolve a service instance."""
        return self._services.get(service_type)

# Create a global container instance
container = Container()

def inject(cls):
    """Class decorator for dependency injection."""
    original_init = cls.__init__
    
    def new_init(self, *args, **kwargs):
        hints = get_type_hints(cls.__init__)
        
        # Exclude return type annotation and self
        if 'return' in hints:
            del hints['return']
        if 'self' in hints:
            del hints['self']
            
        for param_name, param_type in hints.items():
            if param_name not in kwargs:
                instance = container.resolve(param_type)
                if instance:
                    kwargs[param_name] = instance
                
        original_init(self, *args, **kwargs)
        
    cls.__init__ = new_init
    return cls 