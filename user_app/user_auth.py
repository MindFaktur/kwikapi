
import tornado.ioloop
import tornado.web
from kwikapi.tornado import RequestHandler
from kwikapi import API

from psql_operations import PSQLOperations


class UserOperations(object):

    psql_object = PSQLOperations()

    def register(self, firstname: str, lastname: str, username: str, password: str) -> str:
        #id_query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND " \
                 #  "table_type = 'BASE TABLE';"
        #id_query = "SELECT current_database()"

        id_query = "SELECT id FROM user_model.users WHERE username=%s"
        try:
            user_id = self.psql_object.get_value_query_operation(id_query, (username,))
            print(user_id)
            if user_id is False:
                insert_query = "INSERT INTO users(username, password, firstname, lastname) " \
                               "VALUES(%s,%s,%s,%s)"
                self.psql_object.insert_query_operation(insert_query, (username, password, firstname, lastname,))
                return f"{username} created "
            else:
                return f"User with {user_id} already exists"
        except Exception as e:
            return f"error as {e}"

    def login(self, username: str, password: str) -> str:
        id_query = "SELECT id FROM user_table WHERE username=%s AND password=%s"
        try:
            user_id = self.psql_object.get_value_query_operation(id_query, (username, password,))
            if user_id is int:
                return "Logged in"
            else:
                return "Invalid credentials"
        except Exception:
            return "Please enter proper details"


class AppMaker:

    def __init__(self, app_name, version):
        self.api = API()
        self.api.register(app_name(), version)

    def make_app(self):
        return tornado.web.Application([(r'^/api/.*', RequestHandler, dict(api=self.api))])


if __name__ == "__main__":
    app_class = AppMaker(UserOperations, 'v1')
    app = app_class.make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()




"""
api = API()
api.register(Calculator(), 'v1')


def make_app():
    return tornado.web.Application([(r'^/api/.*', RequestHandler, dict(api=api))])

"""