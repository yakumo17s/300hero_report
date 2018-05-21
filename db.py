import sqlite3
import pymysql


def db_handle():
    con = pymysql.connect(
        host='localhost',
        user='root',
        passwd=None,
        charset='utf8',
        database='heroes'
    )
    return con
