import pytest

from fe.access import buyer
from fe.access import seller
from fe.access.new_buyer import register_new_buyer
from fe.access.new_seller import register_new_seller
from fe.test.gen_book_data import GenBook
import uuid
from fe import conf

class TestSendBook:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_send_book_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_send_book_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_send_book_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.buyer_id
        self.buyer = register_new_buyer(self.buyer_id, self.password)
        self.gen_book = GenBook(self.seller_id, self.store_id)
        self.seller = self.gen_book.get_seller()
        yield

    def test_send_book_ok(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        _, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        code = self.buyer.add_funds(10000)
        code = self.buyer.payment(order_id)
        code = self.seller.send_book(self.store_id,order_id)
        assert code == 200

    def test_send_noexist_order(self):
        order_id = '1'
        code = self.seller.send_book(self.store_id,order_id)
        assert code != 200 

    def test_send_noexist_store(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        _, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        code = self.buyer.add_funds(10000)
        code = self.buyer.payment(order_id)
        code = self.seller.send_book('1',order_id)
        assert code != 200

    def test_receive_book_ok(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        _, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        code = self.buyer.add_funds(10000)
        code = self.buyer.payment(order_id)
        code = self.seller.send_book(self.store_id,order_id)
        code = self.seller.receive_book(self.store_id,order_id)
        assert code == 200

    def test_receive_noexist_order(self):
        order_id = '1'
        code = self.seller.receive_book(self.store_id,order_id)
        assert code != 200

    def test_receive_noexist_store(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        _, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        code = self.buyer.add_funds(10000)
        code = self.buyer.payment(order_id)
        code = self.seller.send_book(self.store_id,order_id)
        code = self.seller.receive_book('1',order_id)
        assert code != 200