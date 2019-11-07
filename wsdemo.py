import json
import sys
import os
from flask_sockets import Sockets
import time
from gevent import monkey
from flask import Flask
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from pymysql import connect

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")
monkey.patch_all()

app = Flask(__name__)
sockets = Sockets(app)



@sockets.route('/test')
def echo_socket(ws):
    db = MySQL()
    while True:
        now = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        k = "k" + now
        v = "v" + now
        db.insert_sql(k, v)
        msg = {"k": k, "v": v}
        ws.send(json.dumps(msg))
        time.sleep(2)


@app.route('/')
def hello():
    return 'Hello World! server start！'


class MySQL(object):
    def __init__(self):
        self.conn = connect(host='172.16.0.31', port=3306, user='root', password='deakingreport', database='report', charset='utf8')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def execute_sql(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except IOError:
            print("Error sql:" + sql)
            self.conn.rollback()

    def insert_sql(self, name, key):
        sql = "insert into test(k, v) values('%s', '%s');" % (name, key)
        print(sql)
        self.execute_sql(sql)


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    print('server start')
    server.serve_forever()