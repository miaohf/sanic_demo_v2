"""
Logging system for the application.
Provides structured logging capabilities.
"""
import logging
import sys
from typing import Dict, Any

class Logger:
    """A simple wrapper around the standard logging module."""
    
    def __init__(self, name: str, level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Add console handler if not already present
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            
    def debug(self, message: str, **kwargs):
        """Log a debug message with context."""
        self._log(logging.DEBUG, message, kwargs)
        
    def info(self, message: str, **kwargs):
        """Log an info message with context."""
        self._log(logging.INFO, message, kwargs)
        
    def warning(self, message: str, **kwargs):
        """Log a warning message with context."""
        self._log(logging.WARNING, message, kwargs)
        
    def error(self, message: str, **kwargs):
        """Log an error message with context."""
        self._log(logging.ERROR, message, kwargs)
        
    def _log(self, level: int, message: str, context: Dict[str, Any]):
        """Log a message with context at the specified level."""
        if context:
            context_str = " ".join(f"{k}={v}" for k, v in context.items())
            message = f"{message} - {context_str}"
        self.logger.log(level, message)

# Create a global logger instance
app_logger = Logger("app") 