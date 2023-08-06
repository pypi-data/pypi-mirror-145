from abc import ABC, abstractmethod
from typing import Dict, List


class DatabaseAdapter(ABC):
    """
    An adapter for an arbitrary data store.
    """

    def __init__(self, config: Dict, table_name: str):
        self.initialize(config, table_name)

    @abstractmethod
    def initialize(self, config: Dict, table_name: str):
        """
        Initializes the database adapter.
        :param config: a dictionary with configuration entries for the adapter.
        :param table_name: name of the table/collection used by the adapter implementation.
        """
        raise NotImplementedError()

    @abstractmethod
    def find_by_id(self, id: str) -> Dict:
        """
        Finds an item by its id.
        :param id: the id of the item to be looked for.
        :return: data from the database as a dictionary.
        """
        raise NotImplementedError()

    @abstractmethod
    def find_by_criteria(self, criteria: Dict) -> List[Dict]:
        """
        Finds an item by a given criteria.
        :param criteria: a dictionary with field names and values.
        :return: a list of dictionaries where each entry represents a value from the database.
        """
        raise NotImplementedError()

    @abstractmethod
    def insert(self, data: Dict) -> str:
        """
        Persists an entry in the data store.
        :param data: the data to be inserted in the database as a dictionary.
        :return: the id of the item that has been inserted.
        """
        raise NotImplementedError()

    @abstractmethod
    def all(self, limit: int = None, skip: int = None) -> List[Dict]:
        """
        Returns all items for a given table or document in the database.
        :param limit: maximum amount of items to be returned.
        :param skip: how many results to skip starting at the beginning of the result list.
        :return: a list of dictionaries where each entry represents a value from the database.
        """
        raise NotImplementedError()

    @abstractmethod
    def summary(self, projection: List[str], limit: int = 10) -> List[Dict]:
        """
        Returns a list of the most recent items inserted in the database.
        :param projection: a list of fields to be returned in the result. Other fields from the document/table are going
                           to be ignored.
        :param limit: maximum amount of items to be returned.
        :return: a list of dictionaries where each entry represents a value from the database.
        """
        raise NotImplementedError()

    @abstractmethod
    def count(self) -> int:
        """
        Returns the total amount of items found in the database for this table / document.
        :return: the count of items for this table/document.
        """
        raise NotImplementedError()

    @abstractmethod
    def truncate(self) -> None:
        """
        Removes all records for this document / table. Used for testing only.
        """
        raise NotImplementedError()

    def delete(self, id: int) -> None:
        """
        Deletes an entity using its id.
        :param id: the id of the entity to be deleted.
        """
        raise NotImplementedError()


class DataNotFoundException(Exception):
    """
    Raised when no data has been found in a method that should return data.
    """
    ...


class DataFetchException(Exception):
    """
    Raised when there was a infrastructure problem when fetching data from the data source.
    """
    ...


class DataInsertException(Exception):
    """
    Raised when there was a problem persisting data in the database.
    """
    ...
