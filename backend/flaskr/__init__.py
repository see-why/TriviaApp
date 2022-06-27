import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy import desc

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginated_questions(questions,page):
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_questions = [ question.format() for question in questions ]
    return formatted_questions[start:end]

def current_category(id, categories):
    for category in categories:
        if category.id == id:
            return category.type

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS"
        )
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(desc(Category.id)).all()
        formatted_categories = [ category.format() for category in categories]

        return jsonify({
            "success": True,
            "categories": formatted_categories
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        categories = Category.query.order_by(desc(Category.id)).all()
        questions = Question.query.order_by(desc(Question.id)).all()
        page = request.args.get('page', 1, type=int)

        formatted_questions = paginated_questions(questions,page)
        formatted_categories = [category.format() for category in categories]

        if len(formatted_questions) == 0:
                    abort(404)

        current_category_type = current_category(formatted_questions[0]['category'], categories)

        return jsonify({
            "success": True,
            "questions" : formatted_questions,
            "total_questions" : len(questions),
            "current_category" : current_category_type,
            "categories" : formatted_categories
        })
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify(
                {
                    "success": True
                }
            )

        except:
            print (sys.exc_info())
            abort(422)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def create_questions():
        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)

        try:
            question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
            question.insert()

            return jsonify(
                {
                    "success": True
                }
            )

        except:
            print (sys.exc_info())
            abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        try:                
            body = request.get_json()
            search_item = body.get("search",None)

            if search_item:
                questions = Question.query.order_by(desc(Question.id)).filter(
                Question.question.ilike('%{}%'.format(search_item))).all()
                categories = Category.query.order_by(desc(Category.id)).all()
                
                page = request.args.get('page', 1, type=int)
                formatted_questions = paginated_questions(questions,page)
                print(f"questions {questions}")

                return jsonify({
                    "success": True,
                    "questions" : formatted_questions,
                    "current_category" : current_category(formatted_questions[0]['category'], categories) if formatted_questions else "",
                    "total_questions" : len(questions),
                })
        except:
            print (sys.exc_info())
            abort(422)
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        category = Category.query.filter(Category.id == category_id).one_or_none()

        if category is None:
                abort(404)

        questions = Question.query.filter(Question.category == category.id).all()
        formatted_questions = [question.format() for question in questions]

        if len(formatted_questions) == 0:
                    abort(404)


        return jsonify({
            "success": True,
            "questions" : formatted_questions,
            "total_questions" : len(questions),
            "current_category" : category.type,
        })
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def get_quizzes():
        try:                
            body = request.get_json()
            previous_questions = body.get("previous_questions",None)
            quiz_category = body.get("quiz_category",None)

            if quiz_category:
                question = Question.query.order_by(desc(Question.id)).filter(
                Question.id.notin_(previous_questions)).filter(Question.category == quiz_category['id']).first()

                if question is None:
                    abort(404)

                if previous_questions is None:
                    previous_questions = []

                previous_questions.append(question.id)
                
                return jsonify({
                    "success": True,
                    "previousQuestions" : previous_questions,
                    "question" : question.format()
                })
        except:
            print (sys.exc_info())
            abort(422)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Not found"
            }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "Bad request"
            }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False, 
            "error": 405,
            "message": "Method not allowed"
            }), 405

    @app.errorhandler(422)
    def cannot_process(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "Cannot process request"
            }), 422
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False, 
            "error": 500,
            "message": "Server Error"
            }), 500

    return app

