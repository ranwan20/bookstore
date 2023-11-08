from pymongo import MongoClient
from datetime import timedelta, datetime
from be.model import db_conn
from bson import ObjectId


class Orders(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def cancel_order(self, order_id, end_status=0):
        try:
            # 删除订单
            order_query = {"_id": ObjectId(order_id)}
            order = self.collection_new_order.find_one_and_delete(order_query)
            if not order:
                return 404, f"Invalid order_id: {order_id}"

            # 构建订单信息
            order_info = {
                "order_id": str(order["_id"]),
                "user_id": order["user_id"],
                "store_id": order["store_id"],
                "total_price": order["total_price"],
                "order_time": order["order_time"],
                "status": end_status
            }

            # 删除订单详情
            detail_query = {"order_id": ObjectId(order_id)}
            order_details = self.collection_new_order_detail.find(detail_query)
            books = []
            for detail in order_details:
                book = {
                    "book_id": detail["book_id"],
                    "count": detail["count"]
                }
                if end_status == 0:
                    # 更新库存
                    store_query = {
                        "store_id": order_info["store_id"],
                        "book_id": book["book_id"]
                    }
                    update_query = {"$inc": {"stock_level": book["count"]}}
                    result = self.collection_stores.update_one(store_query, update_query)
                    if result.matched_count == 0:
                        return 404, f"Non-existent book_id: {book['book_id']} for store_id: {order_info['store_id']}"
                books.append(book)

            # 更新订单信息
            order_info["books"] = books
            # self.db["history_order"].insert_one(order_info)

            return 200, "ok"
        except Exception as e:
            return 500, str(e)