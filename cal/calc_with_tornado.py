import tornado.ioloop
import tornado.web
from kwikapi.tornado import RequestHandler
from kwikapi import API


class Calculator(object):

    def add(self, a: int = 10, b: int = 20) -> int:
        return a + b

    def sub(self, a: int, b: int) -> int:
        return a - b

    def mul(self, a: float, b: float) -> float:
        return a * b

    def printNames(self, first_name: str, last_name: str) -> str:
        return f"Full name is {first_name} {last_name}"


class AppMaker:

    def __init__(self, app_name, version):
        self.api = API()
        self.api.register(app_name(), version)

    def make_app(self):
        return tornado.web.Application([(r'^/api/.*', RequestHandler, dict(api=self.api))])


if __name__ == "__main__":
    app_class = AppMaker(Calculator, 'v1')
    app = app_class.make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()




"""
api = API()
api.register(Calculator(), 'v1')


def make_app():
    return tornado.web.Application([(r'^/api/.*', RequestHandler, dict(api=api))])

"""