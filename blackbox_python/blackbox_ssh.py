import pymysql
import pandas as pd
from sshtunnel import SSHTunnelForwarder

sql_hostname = 'localhost'
sql_username = 'whitebox'
sql_password = 'ivorycube'
sql_main_database = 'blackbox_production'
sql_port = 3306
ssh_host = 'white.bluej.org'
ssh_user = 'azh'
ssh_port = 22
sql_ip = '1.1.1.1.1'

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

    def query(self, query):
        if self.mysql_connection is None:
            raise ValueError("Use with statement to initialize this class.")
        return pd.read_sql_query(query, self.mysql_connection)

    def save_query_csv(self, query, save_path):
        self.query(query).to_csv(save_path)
        print("Saved results of the query '{}' to {}.".format(query, save_path))

if __name__ == '__main__':
    with BlackBox() as bb:
        bb.command_line()
