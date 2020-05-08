import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgresql://{}/{}".format('postgres:1234@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_error_404_not_found(self):
        response = self.client().get('/')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_error_422_unprocessable(self):
        response = self.client().get('/questions?page=100')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_error_500_Internal_Server(self):
        response = self.client().post('/questions', json={'seahTerm': 'what'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Internal Server Error')

    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    def test_get_questions(self):
        response = self.client().get('/questions?page=1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(data['categories'])

    def test_post_question(self):
        response = self.client().post('/questions/add', json={
            'question': 'What is the capital of Texas?',
            'answer': 'Austin',
            'difficulty': 1,
            'category': 5
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Question added successfully')

    def test_delete_question(self):
        s1 = Question.query.order_by(Question.id.desc()).limit(1).one_or_none()
        s1 = str(s1.id)
        response = self.client().delete('/questions/'+s1)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Removed question with ID '+s1)

    def test_get_questions_by_category(self):
        response = self.client().get('/categories/5/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['current_category'])

    def test_get_search_question(self):
        response = self.client().post('/questions', json={'searchTerm': 'what'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_play_quiz(self):
        response1 = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'type': 'Entertainment', 'type_id': 5}})
        data1 = json.loads(response1.data)
        response2 = self.client().post('/quizzes', json={'previous_questions':[data1['question']], 'quiz_category': {'type': 'Entertainment', 'type_id': 5}})
        data2 = json.loads(response2.data)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(data1['question']['category'], data2['question']['category'])
        self.assertEqual(data1['question']['id'], data2['question']['id'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()