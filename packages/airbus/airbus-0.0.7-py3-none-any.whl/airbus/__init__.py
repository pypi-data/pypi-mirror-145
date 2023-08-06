import logging
import click
from rich.logging import RichHandler
from rich.traceback import install

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
    )

install(suppress=[click])
