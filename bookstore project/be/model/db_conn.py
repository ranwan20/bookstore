
from pymongo import MongoClient


class DBConn:
    def __init__(self):
        self.client = MongoClient('127.0.0.1', 27017)
        self.db = self.client['bookstore']
        self.collection_books = self.db["book"]
        self.collection_users = self.db["user"]
        self.collection_stores = self.db["store"]
        self.collection_orders = self.db["order"]
        self.collection_new_order_detail = self.db["new_order_detail"]
        self.collection_new_order = self.db["new_order"]
        self.collection_user_store = self.db["user_store"]
        

    def user_id_exist(self, user_id):
        user = self.collection_users.find_one({"user_id": user_id})
        if user is None:
            return False
        else:
            return True

    def book_id_exist(self, store_id, book_id):
        book = self.collection_stores.find_one({"store_id": store_id, "book_id": book_id})
        if book is None:
            return False
        else:
            return True

    def store_id_exist(self, store_id):
        store = self.collection_user_store.find_one({"store_id": store_id})
        if store is None:
            return False
        else:
            return True
        
    def order_id_exist(self, order_id):
        order = self.collection_orders.find_one({"order_id": order_id})
        if order is None:
            return False
        else:
            return True

    def order_new_id_exist(self, order_id):
        order = self.collection_new_order.find_one({"order_id": order_id})
        if order is None:
            return False
        else:
            return True
