import flask
from flask import render_template, request
from os.path import abspath
import sqlite3
import logging

log = logging.getLogger('werkzeug')
log.setLevel(-1)
app = flask.Flask(__name__)


@app.get("/index")
def index():
    page = request.args.get('page') or 1
    page = int(page)
    limit = 20
    begin = (page - 1) * limit
    conn = sqlite3.connect("book.db")
    cur = conn.cursor()
    result = cur.execute(f"select * from book limit {begin},{limit}").fetchall()
    count = cur.execute("select count(*) from book").fetchall()[0][0]
    max_page = count // limit + int(count % limit != 0)
    last_page = page - 1 if page - 1 > 0 else 1
    next_page = page + 1 if page + 1 < max_page else max_page
    context = dict(data=result, total=count, max_page=max_page, now_page=page, last_page=last_page, next_page=next_page)
    return render_template("novel.html", **context)


def run():
    print("服务器运行中.......")
    app.run(host="127.0.0.1", port=8888)


if __name__ == '__main__':
    run()
