from dataclasses import dataclass
from typing import Dict


ENGINES = ["mongita", "mongita_memory", "mongodb", "mongodb_async"]
JSON_SERIALIZEABLE = [dict, list, tuple, str, int, float, bool]


@dataclass
class Config:

    """
    A configuration for the AutoDBClient class.

    Parameters
    ----------
    `*engine` : str
        What engine to use. Please refer to the engine list below on what engine you can use
    `connection_timeout` : int
        How many milliseconds to wait before timing out on MongoDB and falling back to the mongita engine.
        This setting only applies if your engine is mongodb or a variant of it. Defaults to 10000.
    `connection_string` : str
        MongoDB connection string. This only applies if your engine is mongodb or a variant of it. Defaults to "." for None.
    `path` : str
        The path to a local database (Will be created if it doesn't exist.). This is what the mongita engine will use.
        Defaults to "./db"
    `blueprints` : Dict[str, object]
        A dictionary with keys being a blueprint name and values being a "uninitialized" class. Defaults to None.
    """

    engine: str
    connection_timeout: int = 10000
    connection_string: str = "."
    path: str = "./db"
    blueprints: Dict[str, object] = None

    def __post_init__(self) -> None:
        if self.engine not in ENGINES:
            raise ValueError(f"Invalid engine '{self.engine}'")


def unpack_annotations(annotations: dict) -> dict:
    pass
