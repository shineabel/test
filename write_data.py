import time
import serial
from pymysql import connect


class MySQL(object):
    def __init__(self):
        self.conn = connect(host='172.16.0.31', user='root', password='test', database='test', charset='utf8')
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

    def insert_sql(self, name, key, current_time):
        sql = "insert into smp(name, key, current_time) values('%s', '%s','%s');" % (name, key, current_time)
        self.execute_sql(sql)


def main():
    db = MySQL()
    with serial.Serial('/dev/ttyACM2', 9600, timeout=1) as ser:
        while True:
            try:
                data = ser.readline('utf-8')
                time.sleep(0.5)
                if data == '':
                    continue
                else:
                    data = data.split()
                    current_time = data[0]
                    name = data[1]
                    key = data[2]
                    print("{} {} {}".format(name, key, current_time))
                    db.insert_sql(name, key, current_time)
            except IOError as e:
                print("error:", e)
                ser.close()
                ser.flush()


if __name__ == '__main__':
    main()
