import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category
from helpers import get_paginated_questions
from constants import MESSAGE_NOT_FOUND, MESSAGE_UNPROCESSABLE


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/*": {"origin": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]
        return jsonify({
            "success": True,
            "categories": formatted_categories,
            "total_categories": len(formatted_categories)
        })

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_in_category(category_id):
        questions = Question.query.filter(
            Question.category == category_id).all()
        paginated_questions = get_paginated_questions(request, questions)

        return jsonify({
            "success": True,
            "questions": paginated_questions,
            "total_questions": len(questions),
            "current_category": category_id
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():
        questions = Question.query.all()
        paginated_questions = get_paginated_questions(request, questions)

        categories = Category.query.all()

        if len(paginated_questions) < 1:
            return abort(404)

        return jsonify({
            "success": True,
            "questions": paginated_questions,
            "total_questions": len(questions),
            "categories": [category.format() for category in categories],
            "current_category": None
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(
            Question.id == question_id).one_or_none()
        if question == None:
            return abort(404)

        question.delete()
        return jsonify({
            "success": True,
            "deleted": question_id
        })

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        if 'searchTerm' in body.keys():
            return search_questions(request, body['searchTerm'])

        for key in ['question', 'answer', 'difficulty', 'category']:
            if key not in body.keys() or body[key] == None or body[key] == '':
                return abort(422)

        question = Question(
            question=body['question'],
            answer=body['answer'],
            difficulty=body['difficulty'],
            category=body['category'],
        )
        question.insert()

        return jsonify({
            "success": True,
            "created": question.format()
        })

    def search_questions(request, search_term):
        questions = Question.query.filter(
            Question.question.ilike('%'+search_term+'%')
        ).all()
        paginated_questions = get_paginated_questions(request, questions)

        return jsonify({
            "success": True,
            "questions": paginated_questions,
            "total_questions": len(questions),
            "current_category": None
        })

    '''

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": MESSAGE_NOT_FOUND
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": MESSAGE_UNPROCESSABLE
        }), 422

    return app
