
import unittest
import urllib
from flask import Flask
from flask_testing import TestCase
from flask_testing import LiveServerTestCase

#from application import say_hello

# def test_hello():
#     print('hello')
#
# if __name__ == "__main__":
#     say_hello()
#     test_hello()


class MyTest(LiveServerTestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def test_server_is_up_and_running(self):
        print('running server test')
        response = urllib.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)

if __name__ == "__main__":
    unittest.main()






