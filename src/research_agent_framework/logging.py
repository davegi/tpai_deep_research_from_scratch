
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable, Any
from pydantic import BaseModel
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

    @property
    def logger(self) -> Any: ...

    def debug(self, msg: str, *args, **kwargs) -> None: ...
    def info(self, msg: str, *args, **kwargs) -> None: ...
    def warning(self, msg: str, *args, **kwargs) -> None: ...
    def error(self, msg: str, *args, **kwargs) -> None: ...
    def critical(self, msg: str, *args, **kwargs) -> None: ...

# ───────────────────────────────────────────────────────────── BaseLogger: abstract class with shared methods
# ─────────────────────────────────────────────────────────────
class BaseLogger(BaseModel, ABC):
    model_config = {
        "arbitrary_types_allowed": True
    }

    @property
    @abstractmethod
    def level(self) -> str: ...
    @level.setter
    @abstractmethod
    def level(self, value: str) -> None: ...

    @property
    @abstractmethod
    def fmt(self) -> str: ...
    @fmt.setter
    @abstractmethod
    def fmt(self, value: str) -> None: ...

    @property
    @abstractmethod
    def logger(self) -> Any: ...

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
    def __init__(self, sink=sys.stderr, level="INFO", fmt="{time} | {level} | {message}"):
        super().__init__()
        self._sink = sink
        self._level = level
        self._fmt = fmt
        self._handler_id = None
        self._logger = _loguru_logger.bind()
        self._configure()

    def _configure(self):
        if self._handler_id is not None:
            self._logger.remove(self._handler_id)
        self._handler_id = self._logger.add(self._sink, level=self._level, format=self._fmt)

    @property
    def level(self) -> str:
        return self._level

    @level.setter
    def level(self, value: str):
        self._level = value
        self._configure()

    @property
    def fmt(self) -> str:
        return self._fmt

    @fmt.setter
    def fmt(self, value: str):
        self._fmt = value
        self._configure()

    @property
    def logger(self):
        return self._logger

# ───────────────────────────────────────────────────────────── StdLogger: concrete implementation using logging.Logger
# ─────────────────────────────────────────────────────────────

class StdLogger(BaseLogger):
    def __init__(self, name="std_logger", level="INFO", fmt="%(asctime)s | %(levelname)s | %(message)s", stream=None):
        super().__init__()
        self._level = level
        self._fmt = fmt
        self._logger = logging.getLogger(name)
        if stream is None:
            stream = sys.stderr
        self._handler = logging.StreamHandler(stream)
        self._configure()

    def _configure(self):
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
        self._configure()

    @property
    def fmt(self) -> str:
        return self._fmt

    @fmt.setter
    def fmt(self, value: str):
        self._fmt = value
        self._configure()

    @property
    def logger(self):
        return self._logger
