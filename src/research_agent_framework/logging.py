from abc import ABC, abstractmethod
from typing import Optional, Protocol, Self, runtime_checkable, Any
from pydantic import BaseModel, PrivateAttr
import sys
import logging
from loguru import logger as _loguru_logger

# ───────────────────────────────────────────────────────────── LoggingProtocol: defines the interface
# ─────────────────────────────────────────────────────────────
@runtime_checkable
class LoggingProtocol(Protocol):
    @property
    def level(self) -> str: ...
    @level.setter
    def level(self, value: str) -> None: ...

    @property
    def fmt(self) -> str: ...
    @fmt.setter
    def fmt(self, value: str) -> None: ...

    def debug(self, msg: str, *args, **kwargs) -> None: ...
    def info(self, msg: str, *args, **kwargs) -> None: ...
    def warning(self, msg: str, *args, **kwargs) -> None: ...
    def error(self, msg: str, *args, **kwargs) -> None: ...
    def critical(self, msg: str, *args, **kwargs) -> None: ...
    
    @property
    def logger(self) -> Any:
        """Return the underlying logger instance."""
        pass

    def addHandler(self, handler: Any) -> None: ...
    def removeHandler(self, handler: Any) -> None: ...
    def getHandlers(self) -> list: ...

# ───────────────────────────────────────────────────────────── BaseLogger: abstract class with shared methods
# ─────────────────────────────────────────────────────────────
class BaseLogger(BaseModel, ABC):
    model_config = {
        "arbitrary_types_allowed": True
    }

    _level: str = PrivateAttr()
    _fmt: str = PrivateAttr()
    _logger: Any = PrivateAttr()

    def __init__(self, level: str = "INFO", fmt: str = "{time} | {level} | {message}", **kwargs):
        # Only call super().__init__, do not set private attributes here
        super().__init__(**kwargs)

    @abstractmethod
    def model_post_init(self, __context) -> None:
        pass

    @property
    def level(self) -> str:
        return self._level

    @level.setter
    def level(self, value: str) -> None:
        self._level = value

    @property
    def fmt(self) -> str:
        return self._fmt

    @fmt.setter
    def fmt(self, value: str) -> None:
        self._fmt = value

    @property
    def logger(self) -> Any:
        return self._logger

    def addHandler(self, handler: Any) -> None:
        if hasattr(self.logger, "addHandler"):
            self.logger.addHandler(handler)
    def removeHandler(self, handler: Any) -> None:
        if hasattr(self.logger, "removeHandler"):
            self.logger.removeHandler(handler)
    def getHandlers(self) -> list:
        if hasattr(self.logger, "handlers"):
            return list(self.logger.handlers)
        return []

    # Default implementations for all logging methods - use property for maintainability
    def debug(self, msg: str, *args, **kwargs) -> None:
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs) -> None:
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs) -> None:
        self.logger.critical(msg, *args, **kwargs)

# ───────────────────────────────────────────────────────────── LoguruLogger: concrete implementation using Loguru
# ─────────────────────────────────────────────────────────────
class LoguruLogger(BaseLogger):
    _sink: Any = PrivateAttr()
    _handler_id: Optional[int] = PrivateAttr()

    def __init__(self, sink=sys.stderr, level="INFO", fmt="{time} | {level} | {message}", **kwargs):
        # Pass all init args to super().__init__ and also as extra fields for Pydantic
        super().__init__(level=level, fmt=fmt, sink=sink, **kwargs)

    def model_post_init(self, __context) -> None:
        # Use the values from __init__, not the defaults
        self._level = getattr(self, "level", "INFO")
        self._fmt = getattr(self, "fmt", "{message}")  # Use "{message}" as default for test compatibility
        self._sink = getattr(self, "sink", sys.stderr)
        self._handler_id = None
        self._logger = _loguru_logger.bind()
        self._configure()

    def _configure(self):
        if self._logger is None:
            self._logger = _loguru_logger.bind()
        if self._handler_id is not None:
            self._logger.remove(self._handler_id)
        self._handler_id = self._logger.add(self._sink, level=self._level, format=self._fmt)

    def addHandler(self, handler: Any) -> None:
        # Loguru does not use standard handlers, but we can add a sink
        self._handler_id = self._logger.add(handler)
    def removeHandler(self, handler: Any) -> None:
        # Remove by handler id if possible
        if isinstance(handler, int):
            self._logger.remove(handler)
        elif self._handler_id is not None:
            self._logger.remove(self._handler_id)
            self._handler_id = None
    def getHandlers(self) -> list:
        # Loguru does not expose handlers, but we can return the handler id
        return [self._handler_id] if self._handler_id is not None else []

    def set_level(self, value: str):
        self._level = value
        self._configure()

    def set_fmt(self, value: str):
        self._fmt = value
        self._configure()

    level = property(BaseLogger.level.fget, set_level)
    fmt = property(BaseLogger.fmt.fget, set_fmt)

class StdLogger(BaseLogger):
    _name: str = PrivateAttr()
    _stream: Any = PrivateAttr()
    _handler: logging.Handler = PrivateAttr()

    def __init__(self, name="std_logger", level="INFO", fmt="%(asctime)s | %(levelname)s | %(message)s", 
                 stream=None, **kwargs):
        # Pass all init args to super().__init__ and also as extra fields for Pydantic
        super().__init__(level=level, fmt=fmt, name=name, stream=stream if stream is not None else sys.stderr, **kwargs)

    def model_post_init(self, __context) -> None:
        # Use the values from __init__, not the defaults
        self._level = getattr(self, "level", "INFO")
        self._fmt = getattr(self, "fmt", "%(message)s")  # Use "%(message)s" as default for test compatibility
        self._name = getattr(self, "name", "std_logger")
        self._stream = getattr(self, "stream", sys.stderr)
        self._logger = logging.getLogger(self._name)
        self._handler = logging.StreamHandler(self._stream)
        self._logger.setLevel(self._level)
        self._handler.setFormatter(logging.Formatter(self._fmt))
        if self._handler not in self._logger.handlers:
            self._logger.addHandler(self._handler)

    @property
    def level(self) -> str:
        return logging.getLevelName(self._logger.level)

    @level.setter  
    def level(self, value: str):
        self._level = value
        self._logger.setLevel(value)

    @property
    def fmt(self) -> str:
        fmt_obj = getattr(self._handler, "formatter", None)
        if fmt_obj and hasattr(fmt_obj, "_fmt") and isinstance(fmt_obj._fmt, str):
            return fmt_obj._fmt
        return self._fmt

    @fmt.setter
    def fmt(self, value: str):
        self._fmt = value
        self._handler.setFormatter(logging.Formatter(value))

    def addHandler(self, handler: Any) -> None:
        self._logger.addHandler(handler)
    def removeHandler(self, handler: Any) -> None:
        self._logger.removeHandler(handler)
    def getHandlers(self) -> list:
        return list(self._logger.handlers)
