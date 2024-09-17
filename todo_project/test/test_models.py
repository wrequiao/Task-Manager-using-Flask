import unittest
from todo_project import app, db
from todo_project.models import User, Task  # Adjust the import path as needed

class TestTodoModels(unittest.TestCase):

    def setUp(self):
        # Set up the Flask app for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite database for testing

        # Create an application context
        self.app_context = app.app_context()
        self.app_context.push()

        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        # Clean up after each test
        db.session.remove()
        db.drop_all()
        self.app_context.pop()  # Pop the application context

    def test_user_creation(self):
        # Test user creation
        user = User(username='testuser', password='password123')
        db.session.add(user)
        db.session.commit()

        # Retrieve user from the database
        retrieved_user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, 'testuser')
        self.assertEqual(retrieved_user.password, 'password123')
    
    def test_task_creation(self):
        # Create a user and a task associated with that user
        user = User(username='testuser', password='password123')
        db.session.add(user)
        db.session.commit()

        task = Task(content='Test Task', author=user)
        db.session.add(task)
        db.session.commit()

        # Retrieve task from the database
        retrieved_task = Task.query.filter_by(content='Test Task').first()
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.content, 'Test Task')
        self.assertEqual(retrieved_task.author.username, 'testuser')

    def test_load_user(self):
        # Test the user loader function
        user = User(username='testuser', password='password123')
        db.session.add(user)
        db.session.commit()

        loaded_user = User.query.get(int(user.id))
        self.assertIsNotNone(loaded_user)
        self.assertEqual(loaded_user.username, 'testuser')

if __name__ == '__main__':
    unittest.main()