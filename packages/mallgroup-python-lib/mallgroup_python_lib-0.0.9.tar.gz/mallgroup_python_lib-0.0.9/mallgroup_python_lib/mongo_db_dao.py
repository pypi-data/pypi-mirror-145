from datetime import datetime
from typing import Any, Mapping, Optional, Union, Dict, List, Iterator
from pymongo import InsertOne, MongoClient, ReplaceOne, UpdateOne  # type: ignore

TIMESTAMPS_COLLECTION = "processed_tables_timestamps"
PROCESSED_TABLES_TABLE_NAME_FIELD = "source"
TIMESTAMPS_FIELD_NAME = "timestamp"


class MongoDBDAO:
    def __init__(self, connection_string: str, database_name: str) -> None:
        self.connection_string = connection_string
        self.database_name = database_name
        self.client = None
        self.database = None
        self.collection = None
        self.operations: List[Any] = []

    def connect(self) -> None:
        """
        Create MongoDBClient and connect to database.
        """
        self.client = MongoClient(self.connection_string)
        self.database = self.client[self.database_name]  # type: ignore

    def disconnect(self) -> None:
        """
        Dereference database and collection, close client and dereference it.
        """
        self.database = None
        self.client.close()  # type: ignore
        self.client = None

    def get_one(
        self, collection_name: str, filter_query: Dict[str, Union[str, int, float]]
    ) -> Optional[Dict[str, Union[str, int, float]]]:
        """
        Get document corresponding to filter_query.
        """
        return self.database[collection_name].find_one(filter_query)  # type: ignore

    def get_many(
        self, collection_name: str, filter_query: Dict[str, Union[str, int, float]]
    ) -> Iterator[Dict[str, Union[str, int, float]]]:
        """
        Get document corresponding to filter_query.
        """
        return (dict(item) for item in self.database[collection_name].find(filter_query))  # type: ignore

    def update_one(
        self,
        collection_name: str,
        filter_query: Dict[str, Union[str, int, float]],
        updates: Dict[str, Union[str, int, float, datetime]],
    ) -> None:
        """
        Set fields in filtered document to
        values supplied in updates dictionary.
        If the document does not exist, create it.
        """
        self.database[collection_name].update_one(  # type: ignore
            filter_query, {"$set": updates}, upsert=True
        )

    def insert_many(self, collection_name: str, data: List[Dict[Any, Any]]) -> None:
        """
        Insert data to MongoDB.
        """
        self.database[collection_name].insert_many(data)  # type: ignore

    def delete_many(
        self, collection_name: str, filter_query: Dict[str, Union[str, int, float]]
    ) -> None:
        self.database[collection_name].delete_many(filter_query)  # type: ignore

    def delete_all(self, collection_name: str) -> None:
        self.delete_many(collection_name, {})

    def update_timestamp(self, table_name: str, timestamp: str) -> None:
        self.update_one(
            TIMESTAMPS_COLLECTION,
            {PROCESSED_TABLES_TABLE_NAME_FIELD: table_name},
            {TIMESTAMPS_FIELD_NAME: timestamp},
        )

    def last_timestamp(self, table_name: str) -> Union[str, None]:
        """
        Returns timestamp from last successful insertion.
        """
        document = self.get_one(
            TIMESTAMPS_COLLECTION, {PROCESSED_TABLES_TABLE_NAME_FIELD: table_name}
        )
        if document is None:
            return None  # type: ignore

        return document[TIMESTAMPS_FIELD_NAME]  # type: ignore

    def add_replace_operation(
        self, filter: Mapping[str, Any], replacement: Mapping[str, Any]
    ) -> None:
        self.operations.append(
            ReplaceOne(filter=filter, replacement=replacement, upsert=True)
        )

    def add_insert_operation(self, document) -> None:
        self.operations.append(InsertOne(document))

    def add_update_operation(
        self, filter: Mapping[str, Any], update: Mapping[str, Any], upsert: bool = False
    ) -> None:
        self.operations.append(UpdateOne(filter, update, upsert))

    def execute_operations(self, collection_name: str) -> None:
        if self.operations:
            self.database[collection_name].bulk_write(self.operations, ordered=False)  # type: ignore
        self.operations = []
