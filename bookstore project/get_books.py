import logging
import os
from pymongo import MongoClient
from pymongo.database import Database
import sqlite3 as sqlite

def read_sqlite_file():
    # 连接到 SQLite 数据库
    conn = sqlite.connect("./fe/data/book_lx.db")
    cursor = conn.cursor()

    # 从 SQLite 数据库中读取数据
    # 可根据需要执行 SQL 查询语句
    cursor.execute("SELECT * FROM book")
    rows = cursor.fetchall()

    # 转换数据为适用于 MongoDB 的格式
    data = []
    for row in rows:
        # 根据具体情况进行适当的转换
        # 示例中假设每一行数据的字段顺序为：book_id, book_name, author, publication_date, ...
        book_data = {
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "publisher": row[3],
            "original_title": row[4],
            "translator": row[5],
            "pub_year": row[6],
            "pages": row[7],
            "price": row[8],
            "currency_unit": row[9],
            "binding": row[10],
            "isbn": row[11],
            "author_intro": row[12],
            "book_intro": row[13],
            "content": row[14],
            "tags": row[15],
            "picture": row[16],
            # ... 其他字段
        }
        data.append(book_data)

    conn.close()

    return data

def insert_data_to_mongodb(data):
    # 连接到 MongoDB 数据库
    client = MongoClient('127.0.0.1', 27017)
    db = client['bookstore']  # 修改为你要使用的数据库名称
    collection = db['book']  # 修改为你要使用的集合名称

    # 插入数据到 MongoDB
    collection.insert_many(data)
    collection.create_index([("title", "text"), ("tags", "text"), ("content", "text")], name="myindex")

book_data = read_sqlite_file()
insert_data_to_mongodb(book_data)