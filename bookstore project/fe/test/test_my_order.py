from fe.access.buyer import Buyer
from fe.access.book import Book
from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer_auth
import uuid
import pytest


class TestOrders:
    seller_id: str
    store_id: str
    buyer_id: str
    password: str
    buy_book_info_list: [Book]
    total_price: str
    order_id: str
    buyer: Buyer

    # def __init__(self):
    #     # self.gen_book = None

    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.seller_id = "test_order_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_order_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_order_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        self.buyer, self.auth = register_new_buyer_auth(self.buyer_id, self.password)
        self.gen_book = GenBook(self.seller_id, self.store_id)
        self.seller = self.gen_book.get_seller()
        self.temp_order = None

        yield

    # 正确
    # 取消订单
    def test_cancel_order_ok(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        code = self.buyer.cancel(self.buyer_id, order_id)
        print(code)
        assert code == 200

    # 正确
    # 用户错误下取消订单
    def test_cancel_non_exist_buyer_id(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        code = self.buyer.cancel(self.buyer_id + "_x", order_id)
        assert code != 200

    # 正确
    # 订单ID错误下取消订单
    def test_cancel_non_exist_order_id(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        code = self.buyer.cancel(self.buyer_id, order_id + "_x")
        assert code != 200

    # 正确
    # 获取买家订单
    def test_get_order(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        code, result = self.auth.get_order(self.buyer_id)
        assert code == 200

    # 正确
    # 获取卖家订单
    def test_seller_get_order(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        code, result = self.seller.store_get_order(self.store_id)
        assert code == 200

    # ok, buy_book_id_list = gen_book.gen(
    #     non_exist_book_id=False, low_stock_level=False, max_book_count=5
    # )
    # self.buy_book_info_list = gen_book.buy_book_info_list
    # assert ok
    #
    # b = register_new_buyer(self.buyer_id, self.password)
    # self.buyer = b
    #
    # code, self.order_id = b.new_order(self.store_id, buy_book_id_list)
    # assert code == 200
    #
    # self.total_price = 0
    # for item in self.buy_book_info_list:
    #     book: Book = item[0]
    #     num = item[1]
    #     if book.price is None:
    #         continue
    #     else:
    #         self.total_price = self.total_price + book.price * num

    # def teardown_class(self):
    #     self.client.close()

    # def test_ok(self):
    #     # code = self.buyer.add_funds(self.total_price)
    #     # assert code == 200
    #     # print(code)
    #     # code = self.buyer.payment(self.order_id)
    #     # assert code == 200
    #
    #     code = self.buyer.get_order()
    #     print(code)
    #     assert code == 200
    #
    #     code = self.buyer.cancel_order(self.order_id)
    #     assert code == 200
    #
    #     code = self.buyer.check_expired_orders()
    #     assert code == 200

    # # 正确
    # # 订单ID错误下取消订单
    # def test_cancel_non_exist_order_id(self):
    #     ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
    #     assert ok
    #     code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
    #
    #     self.buyer.password = self.buyer.password + "_x"
    #     code = self.buyer.get_order()
    #     print(code)
    #     assert code != 200
    #
    #     code = self.buyer.cancel(self.buyer_id,order_id+ "_x")
    #     assert code != 200

    # # 正确
    # # 买家密码错误
    # def test_get_error_password_order(self):
    #     ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
    #     assert ok
    #     code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
    #     self.buyer.password = self.buyer.password + "_x"
    #     code,result = self.auth.get_order(self.buyer_id)
    #     assert code == 200

    # 正确
    # # 获取卖家订单
    # def test_seller_error_password_get_order(self):
    #     ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
    #     assert ok
    #     code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
    #     code, result = self.seller.store_get_order(self.store_id+ "_x")
    #     assert code != 200
    # # 正确
    # def test_non_exist_book_id(self):
    #     ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=True, low_stock_level=False)
    #     assert ok
    #     code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
    #     assert code != 200

    # # 错误（自己写的）
    # def test_get_order(self):
    #     # 测试正确情况和密码错误的情况
    #     # def get_order(self, buyer_id: str, order_id: str, order=None) -> (int, str)
    #     code,_,url,headers,json = self.buyer.get_order()
    #     print(code,_,url,headers,json)
    #     assert code == 200
    #
    #     self.buyer.password = self.buyer.password + "_x"
    #     code = self.buyer.get_order()
    #     print(code)
    #     assert code != 200
    # # 错误
    # def test_cancel_order(self):
    #     # 测试用户错误和密码错误的情况
    #     code = self.buyer.cancel_order(self.order_id)
    #     assert code == 200
    #
    #     self.buyer.password = self.buyer.password + "_x"
    #     code = self.buyer.cancel_order(self.order_id)
    #     assert code != 200
    #
    #     self.buyer.user_id = self.buyer.user_id + "_x"
    #     code = self.buyer.cancel_order(self.order_id)
    #     assert code != 200
    #
    #     # # 假设订单不存在
    #     # result_code, message = self.collection_orders.cancel_order('invalid_user', order_id)
    #     # assert result_code == error.error_authorization_fail
    # # 错误
    # def test_repeat_cancel_order(self):
    #     # 测试订单重复的情况
    #     code = self.buyer.cancel_order(self.order_id)
    #     assert code == 200
    #
    #     code = self.buyer.cancel_order(self.order_id)
    #     assert code != 200
    # # 错误
    # def test_check_expired_orders(self):
    #     code = self.buyer.check_expired_orders()
    #     assert code == 200

    # def test_get_order(self):#下单后查询历史订单，空
    #     ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
    #     assert ok
    #     code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
    #     code,result = self.auth.history_order(self.buyer_id)
    #     assert result == []
    #
    # def test_get_order_sent(self):#发货后查询历史订单，空
    #     ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
    #     assert ok
    #     code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
    #     code = self.seller.send_books(self.store_id, order_id)
    #     code,result = self.auth.history_order(self.buyer_id)
    #     assert result == []
    #
    # def test_history_order_receive(self):#收货后查询历史订单
    #     ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
    #     assert ok
    #     code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
    #     code = self.seller.send_books(self.store_id, order_id)
    #     code = self.buyer.receive_books(self.buyer_id, self.password, order_id)
    #     code, result = self.auth.history_order(self.buyer_id)
    #     assert code == 200
    # def test_check_expired_orders1(self):
    #     # 模拟过期订单的数据
    #     expired_orders = [
    #         {
    #             "order_id": "order_id_1",
    #             "user_id": "user_id_1",
    #             "book_id": "book_id_1",
    #             "quantity": 2,
    #             "timestamp": 1600000000  # 设置一个过去的时间戳
    #         },
    #         {
    #             "order_id": "order_id_2",
    #             "user_id": "user_id_2",
    #             "book_id": "book_id_2",
    #             "quantity": 3,
    #             "timestamp": 1600000000
    #         }
    #     ]
    #
    #     # 模拟用户和书籍数据
    #     users = {
    #         "user_id_1": {"user_id": "user_id_1", "balance": 100},
    #         "user_id_2": {"user_id": "user_id_2", "balance": 200}
    #     }
    #
    #     books = {
    #         "book_id_1": {"book_id": "book_id_1", "price": 10},
    #         "book_id_2": {"book_id": "book_id_2", "price": 20}
    #     }
    #
    #     # 模拟数据库集合的方法
    #     class CollectionMock:
    #         def find(self, query):
    #             return expired_orders
    #
    #         def find_one(self, query):
    #             return users.get(query["user_id"])
    #
    #         def update_one(self, filter, update):
    #             pass
    #
    #         def delete_one(self, filter):
    #             pass
    #
    #     # 创建待测试的对象
    #     orders =order.Order()
    #     orders.collection_orders = CollectionMock()
    #     orders.collection_users = CollectionMock()
    #     orders.collection_books = CollectionMock()
    #
    #     # 调用待测试的方法
    #     code = self.buyer.check_expired_orders()
    #
    #     # 验证结果
    #     assert code == 200
    #     # assert message == "ok"

    # user_id = 'test_user'
    # order_id = 'test_order'
    # self.auth = auth.Auth(conf.URL)
    # self.seller_id = "test_cancel_order_seller_id_{}".format(str(uuid.uuid1()))
    # self.store_id = "test_payment_store_id_{}".format(str(uuid.uuid1()))
    # print(self.seller_id)
    # # self.user_id = "test_cancel_order_user_id_{}".format(str(uuid.uuid1()))
    # # print(self.user_id)
    # # self.order_id = "test_cancel_order_order_id_{}".format(str(uuid.uuid1()))
    # self.buyer_id = "test_cancel_order_buyer_id_{}".format(str(uuid.uuid1()))
    # # print(self.user_id)
    # self.password = self.seller_id
    # self.buyer = register_new_buyer(self.buyer_id, self.password)
    # print("buyer",self.buyer.password)
    # # self.buyer_id = "test_new_order_buyer_id_{}".format(str(uuid.uuid1()))
    # # self.password = self.seller_id
    # # self.buyer = register_new_buyer(self.buyer_id, self.password)
    # # self.gen_book = GenBook(self.seller_id, self.store_id)
    # gen_book = GenBook(self.seller_id, self.store_id)
    # ok, buy_book_id_list = gen_book.gen(
    #     non_exist_book_id=False, low_stock_level=False, max_book_count=5
    # )
    # self.buy_book_info_list = gen_book.buy_book_info_list
    # assert ok
    # b = register_new_buyer(self.buyer_id, self.password)
    # self.buyer = b
    # code, self.order_id = b.new_order(self.store_id, buy_book_id_list)
    # assert code == 200
