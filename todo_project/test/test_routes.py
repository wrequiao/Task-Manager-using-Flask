import unittest
from todo_project import app, db, bcrypt
from todo_project.models import User, Task

class TestViews(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up a testing Flask application and in-memory SQLite database."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SECRET_KEY'] = 'test_secret_key'  # Required for Flask-Login
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        cls.app = app

    def setUp(self):
        # Set up an application context and initialize the database
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create a test user
        self.test_user = User(username='testuser', password=bcrypt.generate_password_hash('password123').decode('utf-8'))
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username, password):
        """Helper method to log in a test user."""
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        """Helper method to log out the current user."""
        return self.client.get('/logout', follow_redirects=True)

    def test_home_page(self):
        # Test that the home page loads successfully
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About', response.data)

    def test_registration(self):
        # Test user registration
        response = self.client.post('/register', data=dict(
            username='newuser',
            password='password123',
            confirm_password='password123'
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account Created For newuser', response.data)
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user)

    def test_login(self):
        # Test login functionality
        response = self.login('testuser', 'password123')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login Successfull', response.data)

    def test_failed_login(self):
        # Test login with incorrect credentials
        response = self.login('testuser', 'wrongpassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login Unsuccessful. Please check Username Or Password', response.data)

    def test_logout(self):
        # Test logout functionality
        self.login('testuser', 'password123')
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_add_task(self):
        # Test adding a new task
        self.login('testuser', 'password123')
        response = self.client.post('/add_task', data=dict(
            task_name='Test Task'
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task Created', response.data)
        task = Task.query.filter_by(content='Test Task').first()
        self.assertIsNotNone(task)

    def test_update_task(self):
        # Test updating an existing task
        self.login('testuser', 'password123')
        task = Task(content='Initial Task', author=self.test_user)
        db.session.add(task)
        db.session.commit()

        response = self.client.post(f'/all_tasks/{task.id}/update_task', data=dict(
            task_name='Updated Task'
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task Updated', response.data)
        updated_task = Task.query.get(task.id)
        self.assertEqual(updated_task.content, 'Updated Task')

    def test_delete_task(self):
        # Test deleting a task
        self.login('testuser', 'password123')
        task = Task(content='Task to Delete', author=self.test_user)
        db.session.add(task)
        db.session.commit()

        response = self.client.get(f'/all_tasks/{task.id}/delete_task', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task Deleted', response.data)
        deleted_task = Task.query.get(task.id)
        self.assertIsNone(deleted_task)

    def test_change_password(self):
        # Test changing user password
        self.login('testuser', 'password123')
        response = self.client.post('/account/change_password', data=dict(
            old_password='password123',
            new_password='newpassword'
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Password Changed Successfully', response.data)

if __name__ == '__main__':
    unittest.main()