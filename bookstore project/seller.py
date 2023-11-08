import sqlite3 as sqlite
from unittest import result

from be.model import error
from be.model import db_conn
from flask import Blueprint, request, jsonify, make_response
import json
from flask import Blueprint, request, jsonify, make_response

import json
from pymongo import MongoClient

from be.model.order import order_collection

# 不确定改这里还是改store整体
# client = MongoClient('mongodb://localhost:27017/')
# db = client.mydatabase
# collection_books = db.books
# collection_stores = db.stores
# client = MongoClient("mongodb://localhost:27017/")
# db = client["bookstore"]
# collection_books = db["book"]
# collection_users = db["user"]
# collection_buyers = db["buyer"]
# collection_stores = db["store"]
# collection_orders = db["order"]
# collection_new_order_detail = db["new_order_detail"]
# collection_new_order = db["new_order"]
# collection_user_store = db["user_store"]


class Seller(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)
        # client = MongoClient("mongodb://localhost:27017/")
        # db = client["bookstore"]
        self.collection_books = self.db["book"]
        self.collection_users = self.db["user"]
        self.collection_buyers = self.db["buyer"]
        self.collection_stores = self.db["store"]
        self.collection_orders = self.db["order"]
        self.collection_new_order_detail = self.db["new_order_detail"]
        self.collection_new_order = self.db["new_order"]
        self.collection_user_store = self.db["user_store"]

    # # 对于卖家，我们需要实现订单状态和订单查询的功能。
    # # 更新订单状态
    #
    # def update_order_status(self, order_id: str, new_status: str, seller_id: str):
    #     order = order_collection.find_one({'order_id': order_id})
    #     if order and order['seller'] == seller_id:
    #         order['status'] = new_status
    #         order_collection.update_one({'order_id': order_id}, {'$set': order})
    #
    # # 获取订单信息
    # def get_orders(self, seller_id: str):
    #     return list(order_collection.find({'seller': seller_id}))

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

            self.collection_books.insert_one({
                '_id': book_id,
                'store_id': store_id,
                'book_info': json.loads(book_json_str),
                'stock_level': stock_level,
            })
            return 200, 'OK'
        except Exception as e:
            return 530, f'Error: {str(e)}'

        #     self.conn.execute(
        #         "INSERT into store(store_id, book_id, book_info, stock_level)"
        #         "VALUES (?, ?, ?, ?)",
        #         (store_id, book_id, book_json_str, stock_level),
        #     )
        #     self.conn.commit()
        # except sqlite.Error as e:
        #     return 528, "{}".format(str(e))
        # except BaseException as e:
        #     return 530, "{}".format(str(e))
        # return 200, "ok"

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
            result = self.collection_books.find_one({'_id': book_id})
            if result is None:
                return 529, 'The book_id does not exist'
            self.collection_books.update_one(
                {'_id': book_id},
                {'$set': {'stock_level': result['stock_level'] + add_stock_level}}
            )
            return 200, 'OK'
        except Exception as e:
            return 530, f'Error: {str(e)}'

        #     self.conn.execute(
        #         "UPDATE store SET stock_level = stock_level + ? "
        #         "WHERE store_id = ? AND book_id = ?",
        #         (add_stock_level, store_id, book_id),
        #     )
        #     self.conn.commit()
        # except sqlite.Error as e:
        #     return 528, "{}".format(str(e))
        # except BaseException as e:
        #     return 530, "{}".format(str(e))
        # return 200, "ok"

    def create_store(self, user_id: str, store_id: str) -> (int, str):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if self.store_id_exist(store_id):
                return error.error_exist_store_id(store_id)

            self.collection_stores.insert_one({
                'user_id': user_id,
                'store_id': store_id
            })
            return 200, 'OK'
        except Exception as e:
            return 530, f'Error: {str(e)}'

        #     self.conn.execute(
        #         "INSERT into user_store(store_id, user_id)" "VALUES (?, ?)",
        #         (store_id, user_id),
        #     )
        #     self.conn.commit()
        # except sqlite.Error as e:
        #     return 528, "{}".format(str(e))
        # except BaseException as e:
        #     return 530, "{}".format(str(e))
        # return 200, "ok"
