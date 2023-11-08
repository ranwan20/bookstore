import pytest

from fe.access import buyer
from fe.access.new_buyer import register_new_buyer
from fe.test.gen_book_data import GenBook
import uuid
from fe import conf


class TestSearch:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_search_book_in_store_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_search_book_in_store_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_search_book_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.buyer_id
        self.buyer = register_new_buyer(self.buyer_id, self.password)
        self.gen_book = GenBook(self.seller_id, self.store_id)
        yield

    def test_search_ok(self):
        code, result = self.buyer.search_book("三毛", 0)
        assert code == 200

    def test_search_ok_all(self):
        code, result = self.buyer.search_book("三毛", 1)
        assert code == 200

    def test_search_ok_empty(self):
        code, result = self.buyer.search_book("三毛", 1000)
        assert result == []

    def test_search_ok_noexist(self):
        code, result = self.buyer.search_book("+++", 0)
        assert result == []

    def test_search_in_store_ok(self):
        ok, buy_book_id_list, book_search_title = self.gen_book.gen_search(
            non_exist_book_id=False, low_stock_level=False
        )
        assert ok
        store_id=self.store_id
        key = book_search_title
        code, result = self.buyer.search_book_in_store(store_id,key)
        assert code == 200
