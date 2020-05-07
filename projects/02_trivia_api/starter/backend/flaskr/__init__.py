import os
import sys

from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from random import seed, randint

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    db = setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app=app)
    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        categories = [c.format() for c in categories]
        return jsonify({
            'success': True,
            'categories': categories,
            'total_categories': len(categories)
        })

    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        category = request.args.get('category', 'All', type=str)
        start = (page - 1) * 10
        end = start + QUESTIONS_PER_PAGE
        questions = Question.query.all()
        if start > len(questions):
            abort(422)
        categories = Category.query.all()
        questions = [q.format() for q in questions]
        categories = [c.format() for c in categories]
        return jsonify({
            'success': True,
            'questions': questions[start: end],
            'total_questions': len(questions),
            'current_category': category,
            'categories': categories,
        })

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter_by(id=question_id).one_or_none()
        if question is None:
            abort(404)
        question.delete()
        return jsonify({
            'success': True,
            'message': 'Removed question with ID %s' % str(question_id)
        })

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

    @app.route('/questions/add', methods=['POST'])
    def post_questions():
        try:
            data = request.get_json()
            question = Question(question=data['question'], answer=data['answer'], category=data['category'],
                                difficulty=data['difficulty'])
            question.insert()
            return jsonify({
                'success': True,
                'message': 'Question added successfully'
            })
        except:
            print(sys.exc_info())
            abort(500)

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    @app.route('/questions', methods=['POST'])
    def get_search_question():
        query = ('%' + request.get_json()['searchTerm'] + '%')
        questions = Question.query.filter(Question.question.ilike(query)).all()
        if len(questions) == 0:
            abort(404)
        questions = [q.format() for q in questions]
        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(questions),
            'current_category': questions.category
        })

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_categories(category_id):
        category = Category.query.with_entities(Category.type).filter_by(id=category_id).one_or_none()
        if category is None:
            abort(404)
        questions = Question.query.with_entities(Question, Category.type).join(Category,
                                                                               Category.id == Question.category).filter(
            Category.id == category_id).all()
        if questions is None:
            abort(404)
        questions = [q.Question.format() for q in questions]
        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(questions),
            'current_category': category[0]
        })

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

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        args = request.get_json()
        pq = args['previous_questions']
        qc_type = args['quiz_category']['type']
        qc_id = args['quiz_category']['type_id']
        if qc_id == 0:
            questions = Question.query.all()
            seed(len(questions))
            while True:
                index = randint(0, len(questions))
                question = questions[index]
                if question.id in pq:
                    continue
                else:
                    break
        else:
            questions = Question.query.filter(Question.category == qc_id).all()
            seed(len(questions))
            while True:
                index = randint(0, len(questions)-1)
                question = questions[index]
                if len(pq) == len(questions):
                    question = ''
                    break
                elif question.id in pq:
                    continue
                else:
                    break
        print(pq)
        return jsonify({
            'success': True,
            'previousQuestions': pq,
            'question': False if question == '' else question.format()
        })

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
    @app.errorhandler(400)
    def error_400_bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def error_404_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(422)
    def error_422_Unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422

    @app.errorhandler(500)
    def error_500_internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
