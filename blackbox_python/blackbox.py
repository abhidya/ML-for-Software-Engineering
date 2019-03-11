import pymysql
import pandas as pd
from sshtunnel import SSHTunnelForwarder
import json
from enum import Enum

sql_hostname = 'localhost'
sql_username = 'whitebox'
sql_password = 'ivorycube'
sql_main_database = 'blackbox_production'
sql_port = 3306
ssh_host = 'white.bluej.org'
ssh_user = 'azh'
ssh_port = 22
sql_ip = '1.1.1.1.1'
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', 150)


class BlackBox:
    def __init__(self, database=sql_main_database):
        self.ssh_server = SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_password='eeShai7V',
            remote_bind_address=(sql_hostname, sql_port))
        self.mysql_connection = None
        self.db_name = database

    def __enter__(self):
        self.ssh_server.start()
        self.mysql_connection = pymysql.connect(host='127.0.0.1', user=sql_username,
                                                passwd=sql_password, db=self.db_name,
                                                port=self.ssh_server.local_bind_port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mysql_connection.close()
        self.ssh_server.stop()

    def check_initialized(self):
        if self.mysql_connection is None:
            raise ValueError("Use with statement to initialize this class.")
        return

    def table_sizes(self):
        table_size_query = '''
        SELECT
            TABLE_NAME AS `Table`,
            ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024) AS `Size (MB)`
        FROM
            information_schema.TABLES
        ORDER BY
            (DATA_LENGTH + INDEX_LENGTH)
        DESC;
        '''
        return self.query(table_size_query)

    def query(self, query):
        self.check_initialized()
        return pd.read_sql_query(query, self.mysql_connection)

    def save_query_csv(self, query, save_path):
        self.query(query).to_csv(save_path, index=False)
        print("Saved results of the query '{}' to {}.".format(query, save_path))

    def source_histories(self, n=10000, sort_descending_length=True):
        q = "SELECT * FROM source_histories WHERE (source_history_type='complete' OR source_history_type='diff') LIMIT {};".format(
            n)
        source_histories_df = self.query(q)
        source_histories = []

        def get_source_history(source_file_id):
            for history in source_histories:
                if history.source_file_id == source_file_id:
                    return history
            return None

        for i, row in source_histories_df.iterrows():
            source_history = get_source_history(row["source_file_id"])
            if source_history is None:
                source_history = SourceFileHistory(row["source_file_id"])
                source_histories.append(source_history)
            source_history.parse_row(row)

        if sort_descending_length:
            return sorted(source_histories, key=lambda x: len(x), reverse=True)

        return source_histories


class SourceHistoryType(Enum):
    COMPLETE = "complete"
    DIFF = "diff"


class SourceFileHistory:
    def __init__(self, source_file_id):
        self.source_file_id = source_file_id
        self.contents = {}
        self.diffs = {}

    def parse_row(self, source_histories_row):
        try:
            source_history_type = SourceHistoryType(source_histories_row["source_history_type"])

            if source_history_type == SourceHistoryType.COMPLETE:
                self.contents[str(source_histories_row['id'])] = {
                    "content": source_histories_row["content"],
                    "event_id": source_histories_row["master_event_id"],
                    "source_histories_id": source_histories_row["id"]
                }
            elif source_history_type == SourceHistoryType.DIFF:
                self.diffs[str(source_histories_row['id'])] = {
                    "content": source_histories_row["content"],
                    "event_id": source_histories_row["master_event_id"],
                    "source_histories_id": source_histories_row["id"]
                }
        except ValueError:
            from sys import exit
            print("SourceFileHistory only handles 'complete' and 'diff' source_history_type's")
            exit(1)

    def __str__(self):
        return json.dumps(self.contents)

    def __len__(self):
        return len(self.contents.keys()) + len(self.diffs.keys())


if __name__ == '__main__':
    from pymongo import MongoClient
    mongo = MongoClient()
    db = mongo.blackbox
    coll = db.source_histories
    with BlackBox() as bb:
        source_histories = bb.source_histories(n=500)

    for history in source_histories:
        coll.insert_one(history.__dict__)
    

