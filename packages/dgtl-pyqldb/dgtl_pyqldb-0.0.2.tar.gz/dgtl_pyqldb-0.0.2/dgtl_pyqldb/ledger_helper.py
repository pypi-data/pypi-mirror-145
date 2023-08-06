import boto3
from botocore.config import Config
import pandas as pd


def convert_to_df(query_return):
    return pd.DataFrame(query_return)


def convert_to_dicts(query_return):
    return convert_to_df(query_return).to_dict(orient="records")


class LedgerHelper:
    def __init__(self, ledger_name: str, table_name: str, index_name:str, extension: str=None, credentials: dict=None, region: str=None):
        """

        :param ledger_name:
        :param table_name:
        :param index_name:
        :param extension: Appends the ledger name. Use to isolate branches during testing. Will create new tables and not remove them afterwards.
        :param credentials: Dictionary with AccessKeyID, SecretAccessKey and SessionToken
        :param region: AWS region (i.e. eu-central-1)
        """

        self.index_name = index_name
        if extension is not None:
            ledger_name = f'{ledger_name}-{extension}'
        else:
            print("Production environment ledger active")

        if credentials is not None:
            qldb_client = boto3.client("qldb",
                                       aws_access_key_id=credentials['AccessKeyId'],
                                       aws_secret_access_key=credentials['SecretAccessKey'],
                                       aws_session_token=credentials['SessionToken'],
                                       config=Config(region_name=region))
        else:
            if not region:
                qldb_client = boto3.client("qldb")
            else:
                qldb_client = boto3.client("qldb", config=Config(region_name=region))

        ledgers = [data['Name'] for data in qldb_client.list_ledgers(MaxResults=20)["Ledgers"]]

        if ledger_name not in ledgers:
            print(f"Creating ledger with name {ledger_name}. This may take a few minutes")
            qldb_client.create_ledger(Name=ledger_name,
                                      PermissionsMode='STANDARD')

        from pyqldb.driver.qldb_driver import QldbDriver
        self.ledger_driver = QldbDriver(ledger_name=ledger_name, region_name=region)
        self.table_name = table_name
        self.index_name = index_name

        if self.table_name not in self.ledger_driver.list_tables():
            self.initiate_table(table_name=self.table_name, index_name=self.index_name)

        print(f"Ledger: {ledger_name}\nTable: {self.table_name}\nIndex: {self.index_name}\n")

    def initiate_table(self, table_name, index_name):
        self.execute_query(query=f"CREATE TABLE {table_name}")
        self.execute_query(query=f"CREATE INDEX ON {table_name} ({index_name})")

    def execute_query(self, query: str, transaction_executor=None, query_arg=None):
        if not transaction_executor:
            return self.ledger_driver.execute_lambda(lambda executor: self.execute_query(query=query,
                                                                                         transaction_executor=executor,
                                                                                         query_arg=query_arg))
        if query_arg is not None:
            return transaction_executor.execute_statement(query, query_arg)
        else:
            return transaction_executor.execute_statement(query)

    def read_entry(self, index: int = None, column: str = None):
        column = column or "*"
        if not index:
            return self.execute_query(query=f"SELECT {column} FROM {self.table_name}")
        else:
            return self.execute_query(query=f"SELECT {column} FROM {self.table_name} WHERE {self.index_name} IN ({index})")

    def add_entry(self, data: dict, index: int = None, retain=False):
        try:
            if not index:
                index = data[self.index_name]
            if not retain:
                self.remove_entry(index=index)
        except KeyError:
            pass
        self.execute_query(f"INSERT INTO {self.table_name} VALUE {data}")

    def modify_entry(self, data: dict, index: int = None):
        data = data.copy()
        try:
            if not index:
                index = data[self.index_name]
                del data[self.index_name]
        except KeyError:
            pass
        for key, value in data.items():
            print("updating ", key, value)
            self.execute_query(f"UPDATE {self.table_name} SET {key} = ? WHERE {self.index_name} = {index}", query_arg=value)

    def remove_entry(self, index: int = None, data: tuple = None):
        if not index:
            self.execute_query(f"DELETE FROM {self.table_name} WHERE {data[0]} = '{data[1]}'")
        else:
            self.execute_query(f"DELETE FROM {self.table_name} WHERE {self.index_name} = {index}")


if __name__ == "__main__":
    pass
