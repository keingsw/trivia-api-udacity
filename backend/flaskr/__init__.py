import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category
from helpers import get_paginated_questions
from constants import MESSAGE_NOT_FOUND, MESSAGE_UNPROCESSABLE, MESSAGE_SERVER_ERROR


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

        if len(paginated_questions) < 1:
            return abort(404)

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

        if 'search_term' in body.keys():
            return search_questions(request, body['search_term'])

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

        if len(questions) > 0 and len(paginated_questions) < 1:
            return abort(404)

        return jsonify({
            "success": True,
            "questions": paginated_questions,
            "total_questions": len(questions),
            "current_category": None
        })

    @app.route('/quizzes', methods=['POST'])
    def get_guesses():
        body = request.get_json()

        if body == None or 'quiz_category' not in body.keys():
            return abort(422)

        previous_questions = []
        if 'previous_questions' in body.keys():
            previous_questions = body['previous_questions']

        question = Question.query.filter(
            Question.category == body['quiz_category']['id'], Question.id.notin_(previous_questions)).first()

        return jsonify({
            "success": True,
            "question": question.format() if question != None else None
        })

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

    @app.errorhandler(500)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": MESSAGE_SERVER_ERROR
        }), 500

    return app
