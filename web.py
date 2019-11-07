
from flask import Flask
import logging
import urllib.request

app = Flask(__name__)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@app.route('/hello')
def hello():
    logger.debug("================test")
    res = urllib.request.urlopen("https://www.github.com")
    ret = res.read()
    print(ret)
    return ret


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3999)
