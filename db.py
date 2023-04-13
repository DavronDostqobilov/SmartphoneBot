import json
from tinydb import TinyDB, Query

class DB:
    def __init__(self,path):
        self.path = path
        self.db=TinyDB(path)

    def get_tables(self):
        """
        To get the list of all the tables in the database
        """
        return list(self.db.tables())
    def getPhone(self,brend,idx):
        """
        Return phone data by brand
        args:
            brand: str
        return:
            dict
        """
        table = self.db.table(brend)
        return table.get(doc_id=idx)

    def get_phone_list(self,brend):
        """
        Return phone list
        """
        table = self.db.table(brend)
        return table.all()

