import warnings
from pathlib import Path
from typing import Optional, List

import motor.motor_asyncio
from mongita import MongitaClientDisk, MongitaClientMemory
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError

from .common import Config, JSON_SERIALIZEABLE
from .exceptions import *


class AutoDBClient:
    """
    Initialize a database client.

    Parameters
    ----------
    `name` : str
        The default database. This is the database returned from self.db. 
        You can however get a different database by using the `get_database()` method.
    `config` : Config
        Configuration for the database.
    """

    ENGINE_MAPPINGS = {
        "mongodb": MongoClient,
        "mongodb_async": motor.motor_asyncio.AsyncIOMotorClient,
        "mongita": MongitaClientDisk,
        "mongita_memory": MongitaClientMemory
    }

    def __init__(self, name: str, config: Config) -> None:

        # Params
        self.name = name
        self.engine = config.engine
        self.connection_timeout = config.connection_timeout
        self.connection_string = config.connection_string
        self.path = config.path
        self.blueprints = {} if config.blueprints is None else config.blueprints

        self.internal_client = None

        if self.engine in ["mongodb", "mongodb_async"]:
            try:
                self.internal_client = self.ENGINE_MAPPINGS[self.engine](
                    self.connection_string,
                    serverSelectionTimeoutMS=self.connection_timeout
                )
                if not self.engine == "mongodb_async":
                    self.internal_client.server_info()
            except ServerSelectionTimeoutError:
                warnings.warn(
                    f"Cannot connect to MongoDB due to a invalid connection_string. Falling back to mongita.", InvalidConnectionString)
                self.engine = "mongita"

        if self.engine in ["mongita", "mongita_memory"]:
            kwargs = {}
            if self.engine == "mongita":
                kwargs["host"] = self.path
                Path(self.path).mkdir(exist_ok=True, parents=True)

            self.internal_client = self.ENGINE_MAPPINGS[self.engine](**kwargs)

    @property
    def db(self) -> Database:
        return self.get_database(self.name)

    def get_database(self, name: str) -> Database:
        """
        Get a database.

        Parameters
        ----------
        `name` : str
            The name of the database to get.

        Returns
        -------
        `Database`
        """

        return self.internal_client[name]

    def find_blueprint(self, data: dict) -> Optional[object]:
        """
        NOT YET IMPLEMENTED.
        Attempts to find a matching blueprint for the provided data.

        Parameters
        ----------
        `data` : dict

        Returns
        -------
        `Optional[object]` :
            The matched blueprint's object if found.
        """

        # TODO: Support Union, List, Tuple, Optional, etc.
        # TODO: Support nested blueprints and dataclasses
        raise NotImplementedError

        as_types = {k: type(v) for k, v in data.items()}
        for k, v in self.blueprints.items():
            types = list(v.__annotations__.values())
            _has_non_json = bool(
                [x for x in types if x not in JSON_SERIALIZEABLE])
            if not _has_non_json:
                if v.__annotations__ == as_types:
                    return v

    def objectify(self, data: dict, blueprint: str) -> object:
        """
        Converts a dictionary (preferably from a query result) into a object specified in the config's blueprints as a class.
        Keep in mind this will pop the `_id` attribute of the provided `data` if it exists.

        Parameters
        ----------
        `data` : dict
            The dictionary.
        `blueprint` : str
            The blueprint to use. This will map to whatever is in the `blueprints` parameter of the config.

        Returns
        -------
        `object` :
            The class created from the config.

        Raises
        ------
        `BlueprintNotFound` :
            When no blueprint is found.
        """

        data.pop("_id", None)
        class_ = self.blueprints.get(blueprint)
        if class_ is None:
            raise BlueprintNotFound(blueprint)
        return class_(**data)
    
    def find_as_object(self, collection: str, blueprint: str, filter: dict, *args, **kwargs) -> Optional[object]:

        """
        Perform a collection.find_one() and convert the returned object into the specified blueprint.

        Parameters
        ----------
        `colletion` : str
            Collection to look for.
        `blueprint` : str
            The name of the blueprint to use.
        `filter : dict
            find_one() filter parameter.
        `database` : str
            Name of the database. Defaults to self.name.
        `*args`, `**kwargs` :
            Other parameters to be passed onto find_one()

        Returns
        -------
        `Optional[object]` :
            The query result fully mapped into the blueprint's object.

        Raises
        ------
        `BlueprintNotFound` :
            When no blueprint is found.
        """

        # TODO: Asynchronous

        db = self.get_database(kwargs.pop("database", self.name))
        result = db[collection].find_one(filter, *args, **kwargs)
        if not result:
            return
        return self.objectify(result, blueprint)
    
    def find_as_objects(self, collection: str, blueprint: str, filter: dict = None, *args, **kwargs) -> List[object]:

        """
        Perform a collection.find() and convert the returned objects into a list of the specified blueprint.

        Parameters
        ----------
        `colletion` : str
            Collection to look for.
        `blueprint` : str
            The name of the blueprint to use.
        `filter : dict
            find() filter parameter. Defaults to None which is to return all results.
        `database` : str
            Name of the database. Defaults to self.name.
        `*args`, `**kwargs` :
            Other parameters to be passed onto find()

        Returns
        -------
        `List[object]` :
            The query results fully mapped as the provided blueprint's object.

        Raises
        ------
        `BlueprintNotFound` :
            When no blueprint is found.
        """

        # TODO: Asynchronous

        db = self.get_database(kwargs.pop("database", self.name))
        results = db[collection].find(filter, *args, **kwargs)
        objects = [self.objectify(x, blueprint) for x in results]
        return objects
