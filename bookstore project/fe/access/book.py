import os
import simplejson as json
from bson import json_util
from pymongo import MongoClient, ReturnDocument
from bson.json_util import dumps
from random import randint
import base64
import json


class Book:
    # id: str
    # title: str
    # author: str
    # publisher: str
    # original_title: str
    # translator: str
    # pub_year: str
    # pages: int
    # price: int
    # binding: str
    # isbn: str
    # author_intro: str
    # book_intro: str
    # content: str
    # tags: [str]
    # pictures: [bytes]

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.title = kwargs.get('title')
        self.author = kwargs.get('author')
        self.publisher = kwargs.get('publisher')
        self.original_title = kwargs.get('original_title')
        self.translator = kwargs.get('translator')
        self.pub_year = kwargs.get('pub_year')
        self.pages = kwargs.get('pages')
        self.price = kwargs.get('price')
        self.currency_unit = kwargs.get('currency_unit')
        self.binding = kwargs.get('binding')
        self.isbn = kwargs.get('isbn')
        self.author_intro = kwargs.get('author_intro')
        self.book_intro = kwargs.get('book_intro')
        self.content = kwargs.get('content')
        self.tags = kwargs.get('tags', [])
        self.pictures = kwargs.get('pictures', [])

    def __repr__(self):
        return dumps(self.__dict__)

        # self.tags = []
        # self.pictures = []


class BookDB:
    def __init__(self, large: bool = True):
        parent_path = os.path.dirname(os.path.dirname(__file__))
        self.db_s = os.path.join(parent_path, "data/book.db")
        self.db_l = os.path.join(parent_path, "data/book_lx.db")

        self.client = MongoClient('127.0.0.1', 27017)
        self.db = self.client['bookstore']
        self.collection_books = self.db["book"]

        if large:
            self.book_db = self.db_l
        else:
            self.book_db = self.db_s
    # def __init__(self):
    #     self.client = MongoClient('127.0.0.1', 27017)
    #     self.db = self.client['bookstore']
    #     self.collection_books = self.db["book"]

    # def get_book_count(self):
    #     conn = sqlite.connect(self.book_db)
    #     cursor = conn.execute("SELECT count(id) FROM book")
    #     row = cursor.fetchone()
    #     return row[0]

    def get_book_count(self):
        self.collection_books = self.db["book"]
        count = self.collection_books.count_documents({})
        return count

    # def get_book_info(self, start=0, size=10) -> [Book]:
    def get_book_info(self, start, size):

        # book_id = str(book["_id"])
        # code = self.seller.add_book(self.store_id, 0, {"book_id": book_id})
        # query = self.db.find().skip(start).limit(size)
        # query = self.db.list(self.db.find({}).skip(start).limit(size))
        # query =  list(self.db.find({}).skip(start).limit(size))
        query = list(self.db.book.find({}).skip(start).limit(size))
        # query = self.db.find(skip=start).limit(
        #     size)  # Mongo equivalent of LIMIT and OFFSET to fetch books based on start and size.
        books = []
        for book_doc in query:
            book = Book(**book_doc)  # Create a Book object from the document in MongoDB
            books.append(book)
        return books

    def to_json(self, data):
        return json_util.dumps(data)

    def from_json(self, data):
        return json_util.loads(data)

    # def get_book_info(self, start, size) -> [Book]:
    #     books = []
    #     conn = sqlite.connect(self.book_db)
    #     cursor = conn.execute(
    #         "SELECT id, title, author, "
    #         "publisher, original_title, "
    #         "translator, pub_year, pages, "
    #         "price, currency_unit, binding, "
    #         "isbn, author_intro, book_intro, "
    #         "content, tags, picture FROM book ORDER BY id "
    #         "LIMIT ? OFFSET ?",
    #         (size, start),
    #     )
    #     for row in cursor:
    #         book = Book()
    #         book.id = row[0]
    #         book.title = row[1]
    #         book.author = row[2]
    #         book.publisher = row[3]
    #         book.original_title = row[4]
    #         book.translator = row[5]
    #         book.pub_year = row[6]
    #         book.pages = row[7]
    #         book.price = row[8]
    #
    #         book.currency_unit = row[9]
    #         book.binding = row[10]
    #         book.isbn = row[11]
    #         book.author_intro = row[12]
    #         book.book_intro = row[13]
    #         book.content = row[14]
    #         tags = row[15]
    #
    #         picture = row[16]
    #
    #         for tag in tags.split("\n"):
    #             if tag.strip() != "":
    #                 book.tags.append(tag)
    #         for i in range(0, random.randint(0, 9)):
    #             if picture is not None:
    #                 encode_str = base64.b64encode(picture).decode("utf-8")
    #                 book.pictures.append(encode_str)
    #         books.append(book)
    #         # print(tags.decode('utf-8'))
    #
    #         # print(book.tags, len(book.picture))
    #         # print(book)
    #         # print(tags)
    #
    #     return books
