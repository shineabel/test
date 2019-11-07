import time
import serial
from pymysql import connect


class MySQL(object):
    def __init__(self):
        self.conn = connect(host='172.16.0.31', user='root', password='deakingreport', database='report', charset='utf8')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def execute_sql(self, sql):
        try:
            print(sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except IOError:
            print("Error sql:" + sql)
            self.conn.rollback()

    def insert_sql(self, name, key):
        sql = "insert into test(k, v) values('%s', '%s');" % (name, key)
        print(sql)
        self.execute_sql(sql)


def main():
    db = MySQL()
    db.insert_sql("test1", "test1")


if __name__ == '__main__':
    main()
