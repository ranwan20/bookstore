import sqlite3 as sqlite
from unittest import result

from be.model import error
from be.model import db_conn
import json

import json
from pymongo import MongoClient


class Seller(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def send_book(self, store_id, order_id):
        try:
            if not self.store_id_exist(store_id):
                   return error.error_non_exist_store_id(store_id)
            
            if not self.order_id_exist(order_id):
                    return error.error_invalid_order_id(order_id)
        
            self.collection_orders.update_one({"order_id": order_id}, {"$set": {"status": "已发货"}})
            return 200, 'OK'
        except Exception as e:
            return 530, f'Error: {str(e)}'
        
    
    def receive_book(self, store_id, order_id):
        try:
            if not self.store_id_exist(store_id):
                   return error.error_non_exist_store_id(store_id)
            
            if not self.order_id_exist(order_id):
                    return error.error_invalid_order_id(order_id)
        
            self.collection_orders.update_one({"order_id": order_id, "status": "已发货"}, {"$set": {"status": "已收货"}})
            return 200, 'OK'
        except Exception as e:
            return 530, f'Error: {str(e)}'
        

    def add_book(
            self,
            user_id: str,
            store_id: str,
            book_id: str,
            book_json_str: str,
            stock_level: int,
    ):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if self.book_id_exist(store_id, book_id):
                return error.error_exist_book_id(book_id)

            self.collection_stores.insert_one({
                'book_id': book_id,
                'store_id': store_id,
                'book_info': book_json_str,
                'stock_level': stock_level,
            })
            return 200, 'OK'
        except Exception as e:
            return 530, f'Error: {str(e)}'

    def add_stock_level(
            self, user_id: str, store_id: str, book_id: str, add_stock_level: int
    ):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if not self.book_id_exist(store_id, book_id):
                return error.error_non_exist_book_id(book_id)
            result1 = self.collection_stores.find_one({'book_id': book_id})
            if result1 is None:
                return 528, 'The book_id does not exist'
            self.collection_stores.update_one(
                {'book_id': book_id},
                {'$set': {'stock_level': result1['stock_level'] + add_stock_level}}
            )
            return 200, 'OK'
        except Exception as e:
            return 530, f'Error: {str(e)}'

    def create_store(self, user_id: str, store_id: str) -> (int, str):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if self.store_id_exist(store_id):
                return error.error_exist_store_id(store_id)

            self.collection_user_store.insert_one({
                'user_id': user_id,
                'store_id': store_id
            })
            return 200, 'OK'
        except Exception as e:
            return 530, f'Error: {str(e)}'

    def store_get_order(self, store_id):
        try:
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)

            result = []
            orders = self.collection_new_order.find({'store_id': store_id}, {'_id': 0})
            for order in orders:
                result.append(order)

        except Exception as e:
            return 529, "{}".format(str(e)), []
        except BaseException as e:
            return 530, "{}".format(str(e)), []
        return 200, "ok", result
