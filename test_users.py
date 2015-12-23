import os
import unittest

from views import app, db
from _config import basedir
from models import User
import test.helper_functions as helper

TEST_DB = 'test.db'


class UserTests(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_form_is_present_on_register_page(self):
        response = self.app.get('register/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Please register to access the task list.',
                      response.data)

    def test_user_registration(self):
        self.app.get('register/', follow_redirects=True)
        response = helper.register(self, 'Michael', 'michael@realpython.com', 'python', 'python')
        self.assertIn(b'Thanks for registering. Please login.', response.data)

    def test_user_registration_error(self):
        self.app.get('register/', follow_redirects=True)
        helper.register(self, 'Michael', 'michael@realpython.com', 'python', 'python')
        self.app.get('register/', follow_redirects=True)
        response = helper.register(self,
                                   'Michael', 'michael@realpython.com', 'python', 'python')
        self.assertIn(
            b'That username and/or email already exist.',
            response.data)

    def test_invalid_form_data(self):
        helper.register(self, 'Michael', 'michael@realpython.com', 'python', 'python')
        response = helper.login(self, 'alert("alert box!");', 'foo')
        self.assertIn(b'Invalid username or password.', response.data)

    def test_form_is_present_on_login_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please sign in to access your task list', response.data)

    def test_users_can_login(self):
        helper.register(self, 'Michael', 'michael@realpython.com', 'python', 'python')
        response = helper.login(self, 'Michael', 'python')
        self.assertIn(b'Welcome!', response.data)

    def test_logged_in_users_can_logout(self):
        helper.register(self, 'Fletcher', 'fletcher@realpython.com', 'python101', 'python101')
        helper.login(self, 'Fletcher', 'python101')
        response = helper.logout(self)
        self.assertIn(b'Goodbye!', response.data)

    def test_users_cannot_login_unless_registered(self):
        response = helper.login(self, 'foo', 'bar')
        self.assertIn(b'Invalid username or password.', response.data)

    def test_not_logged_in_users_cannot_logout(self):
        response = helper.logout(self)
        self.assertNotIn(b'Goodbye!', response.data)

    def test_default_user_role(self):
        db.session.add(
            User(
                "Johnny",
                "john@doe.com",
                "johnny"
            )
        )

        db.session.commit()

        users = db.session.query(User).all()
        for user in users:
            self.assertEquals(user.role, 'user')


if __name__ == "__main__":
    unittest.main()
