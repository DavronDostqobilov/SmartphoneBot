from tinydb import TinyDB, Query

class Cart:
    def __init__(self,cart_path:str):
        self.db = TinyDB(cart_path, indent=4)
        self.table = self.db.table('cart')
        
    def add(self,brend, doc_id, chat_id):
        data = {
            'brand':brend,
            'doc_id': doc_id,
            'chat_id': chat_id
        }
        print(data)
        self.table.insert(data)

    def get_cart(self, chat_id):
        user = Query()
        return self.table.search(user.chat_id == chat_id)

    def remove(self, chat_id):
        user = Query()
        self.table.remove(user.chat_id == chat_id)