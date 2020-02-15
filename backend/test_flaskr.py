import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from constants import QUESTIONS_PER_PAGE, MESSAGE_NOT_FOUND, MESSAGE_UNPROCESSABLE


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": 'Which planet has a moon named Phobos?',
            "answer": "Mars",
            "difficulty": 3,
            "category": 1
        }

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
      Endpoint: GET /categories
    """

    def test_get_categories_success(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_categories'])

    """
      Endpoint: GET /questions
    """

    def test_get_questions_success(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), QUESTIONS_PER_PAGE)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertIsNone(data['current_category'])

    def test_get_questions_error_page_not_exist_beyond_valid_page(self):
        response = self.client().get('/questions?page=10000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], MESSAGE_NOT_FOUND)

    def test_get_questions_error_page_not_exist_page_0(self):
        response = self.client().get('/questions?page=0')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], MESSAGE_UNPROCESSABLE)

    def test_get_questions_error_page_not_exist_page_below_zero(self):
        response = self.client().get('/questions?page=-1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], MESSAGE_UNPROCESSABLE)

    """
      Endpoint: POST /questions
    """

    # Create New Question
    def test_create_question_success(self):
        response = self.client().post('/questions', json=self.new_question.copy())
        data = json.loads(response.data)

        new_question = Question.query.order_by(Question.id.desc()).first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertEqual(data['created']['id'], new_question.id)
        self.assertEqual(data['created']['question'], new_question.question)
        self.assertEqual(data['created']['answer'], new_question.answer)
        self.assertEqual(data['created']['difficulty'],
                         new_question.difficulty)
        self.assertEqual(data['created']['category'],
                         new_question.category)

    def test_create_question_error_question_is_missing(self):
        request = self.new_question.copy()
        del request["question"]

        response = self.client().post('/questions', json=request)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], MESSAGE_UNPROCESSABLE)

    def test_create_question_error_question_is_empty(self):
        request = self.new_question.copy()
        request["question"] = ''

        response = self.client().post('/questions', json=request)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], MESSAGE_UNPROCESSABLE)

    def test_create_question_error_answer_is_missing(self):
        request = self.new_question.copy()
        del request["answer"]

        response = self.client().post('/questions', json=request)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], MESSAGE_UNPROCESSABLE)

    def test_create_question_error_answer_is_empty(self):
        request = self.new_question.copy()
        request["answer"] = ''

        response = self.client().post('/questions', json=request)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], MESSAGE_UNPROCESSABLE)

    def test_create_question_error_difficulty_is_missing(self):
        request = self.new_question.copy()
        del request["difficulty"]

        response = self.client().post('/questions', json=request)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], MESSAGE_UNPROCESSABLE)

    def test_create_question_error_category_is_missing(self):
        request = self.new_question.copy()
        del request["category"]

        response = self.client().post('/questions', json=request)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], MESSAGE_UNPROCESSABLE)

    # Search Questions
    def test_search_questions_success(self):
        response = self.client().post(
            '/questions', json={"searchTerm": 'title'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertIsNone(data['current_category'])

    def test_search_questions_success_no_results(self):
        response = self.client().post(
            '/questions', json={"searchTerm": 'QQQQQQQQ'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)
        self.assertIsNone(data['current_category'])

    # @QUESTION Is there any case to be tested when search_questions throws error?

    """
      Endpoint: DELETE /questions/<int:question_id>
    """

    def test_delete_question_success(self):
        question = Question.query.order_by(Question.id.desc()).first()
        question_id = question.id

        response = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(response.data)

        question = Question.query.get(question_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertIsNone(question)

    def test_delete_question_error_question_not_exist(self):
        question_id = 100000000
        response = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], MESSAGE_NOT_FOUND)

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
