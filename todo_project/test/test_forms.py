import unittest
from flask import Flask
from flask_login import LoginManager, login_user, logout_user
from todo_project import db
from todo_project.models import User
from todo_project.forms import RegistrationForm, LoginForm, UpdateUserInfoForm, UpdateUserPassword, TaskForm, UpdateTaskForm

class TestForms(unittest.TestCase):

    def setUp(self):
        # Set up a basic Flask app and in-memory SQLite database
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = 'test_secret_key'  # Required for Flask-Login
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        # Initialize extensions
        self.login_manager = LoginManager(self.app)  # Set up Flask-Login
        db.init_app(self.app)
        
        # Create an application context
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_registration_form(self):
        # Create a registration form with valid data
        form = RegistrationForm(username='testuser', password='password123', confirm_password='password123')
        self.assertTrue(form.validate())

        # Create a user in the database
        user = User(username='testuser', password='password123')
        db.session.add(user)
        db.session.commit()

        # Check if the form raises a validation error for existing username
        form = RegistrationForm(username='testuser', password='password123', confirm_password='password123')
        self.assertFalse(form.validate())

    def test_login_form(self):
        # Create a login form with valid data
        form = LoginForm(username='testuser', password='password123')
        self.assertTrue(form.validate())

    def test_update_user_info_form(self):
        # Simulate a logged-in user
        user = User(username='testuser', password='password123')
        db.session.add(user)
        db.session.commit()
        with self.app.test_request_context():
            login_user(user)

            # Form with a different username, should be invalid
            form = UpdateUserInfoForm(username='existinguser')
            self.assertFalse(form.validate())

            # Form with the same username, should be valid
            form = UpdateUserInfoForm(username='testuser')
            self.assertTrue(form.validate())

            logout_user()

    def test_update_user_password_form(self):
        # Create a form for changing password
        form = UpdateUserPassword(old_password='oldpass', new_password='newpass')
        self.assertTrue(form.validate())

    def test_task_form(self):
        # Create a task form with valid data
        form = TaskForm(task_name='Test Task')
        self.assertTrue(form.validate())

    def test_update_task_form(self):
        # Create an update task form with valid data
        form = UpdateTaskForm(task_name='Updated Task Description')
        self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main()