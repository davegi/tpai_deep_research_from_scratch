import logging
from assertpy import assert_that
import pytest

logger = logging.getLogger("tdd_demo")
logger.setLevel(logging.INFO)
if not logger.handlers:
    from rich.logging import RichHandler
    logger.addHandler(RichHandler(rich_tracebacks=True))

def add(a, b):
    logger.info(f"Adding {a} + {b}")
    return a + b

def test_add():
    result = add(2, 3)
    logger.info(f"Result of add(2, 3): {result}")
    assert_that(result).is_equal_to(5)

if __name__ == "__main__":
    pytest.main([__file__])
