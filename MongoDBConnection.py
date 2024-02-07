from pymongo import MongoClient

class MongoDBConnection:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client["test_results"]
        self.collection = self.db["download_tests"]

    def close_connection(self):
        self.client.close()