from __future__ import annotations

import loguru

from data_metric_connector.connectors.mongo.connect import ConnectMongo
from data_metric_connector.utils.file_size import convert_size


class Mongo(object):
    """This class is used for executing Mongo db operations."""

    def __init__(self, logger: loguru.Logger):
        """
        __init__  function.

        :param logger: provides logging capability
        """
        self.logger = logger

    def get_meta(self, username: str, password: str, host: str, port: int, db: str) -> list[dict[str, dict[str, str]]]:
        """
        Gets the metadata of the mongo db database.

        :param username: username of db
        :param password: password of the username
        :param host: host name of mongo db
        :param port: port number of mongo db
        :param db: mogo db database name
        :return: metadata of the database
        """
        try:
            meta = []
            client = ConnectMongo(self.logger).connect_database(username, password, host, port, db)
            for dbs in client.list_databases():
                mongo_data = client.get_database(dbs["name"]).command("dbstats")
                mongo_data.update({"avgObjSize": convert_size(mongo_data["avgObjSize"])})
                mongo_data.update({"dataSize": convert_size(mongo_data["dataSize"])})
                mongo_data.update({"storageSize": convert_size(mongo_data["storageSize"])})
                mongo_data.update({"indexSize": convert_size(mongo_data["indexSize"])})
                mongo_data.update({"totalSize": convert_size(mongo_data["totalSize"])})
                mongo_data.update({"fsUsedSize": convert_size(mongo_data["fsUsedSize"])})
                mongo_data.update({"fsTotalSize": convert_size(mongo_data["fsTotalSize"])})
                coll_info = {}
                for collections in client.get_database(dbs["name"]).list_collection_names():
                    collection = client.get_database(dbs["name"]).command("collStats", collections)
                    coll_info[collections] = {
                        "count": collection["count"],
                        "storageSize": convert_size(collection["storageSize"]),
                    }
                mongo_data["collections"] = coll_info
                meta.append(mongo_data)
            self.logger.info(f"MetaData is {meta}")
            ConnectMongo(self.logger).disconnect_database(client)
            return meta
        except Exception as e:
            self.logger.error(f"get_meta failed with Exception - {e}")
            return []
