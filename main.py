# -*- coding: utf-8 -*-
# filename: main.py
import web
from handle import Handle

asked_qna = dict()

urls = (
    '/wx', 'Handle',
)


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()

