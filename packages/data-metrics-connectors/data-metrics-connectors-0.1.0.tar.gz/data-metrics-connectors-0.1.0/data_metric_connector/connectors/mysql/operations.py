from __future__ import annotations

import loguru

from data_metric_connector.connectors.mysql.connect import ConnectMySql
from data_metric_connector.utils.file_size import convert_size


class MySql(object):
    """This class is used for executing MySql operations."""

    def __init__(self, logger: loguru.Logger) -> None:
        """
        __init__  function.

        :param logger: provides logging capability
        """
        self.logger = logger

    def get_meta(self, username: str, password: str, host: str, port: int, db: str) -> list[dict[str, dict[str, str]]]:
        """
        Gets the metadata of the Mysql db database.

        :param username: username of db
        :param password: password of the username
        :param host: host name of Mysql db
        :param port: port number of Mysql db
        :param db: Mysql db database name
        :return: metadata of the database
        """
        cxn = ConnectMySql(self.logger).connect_database(username, password, host, port, db)
        cursor = cxn.cursor(buffered=True)
        try:
            with open(
                "connectors/mysql/meta_sql/meta.sql",
            ) as f:
                query_count = 0
                for cursors in cursor.execute(f.read(), (db, db), multi=True):
                    query_count += 1
                    query_result = cursors.fetchall()
                    if query_count == 1:
                        tables_size = {table_name: [convert_size(int(size))] for table_name, size in query_result}
                    elif query_count == 2:
                        tables_count = {
                            table_name: [column_count, int(row_count)]
                            for table_name, column_count, row_count in query_result
                        }
                meta = [
                    {
                        tables: {
                            "Size": tables_size[tables][0],
                            "row_count": tables_count[tables][1],
                            "column_count": tables_count[tables][0],
                        }
                        for tables in tables_size.keys()
                    }
                ]
                self.logger.info(f"MetaData is {meta}")
            return meta
        except Exception as e:
            self.logger.error(f"Unable to execute query! - {e}")
            return []
        finally:
            cursor.close()
            ConnectMySql(self.logger).disconnect_database(cxn)
