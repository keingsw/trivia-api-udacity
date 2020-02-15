# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## Endpoints

### GET /categories

- Returns a list of all categories, success value, and total number of categories.

#### Sample

`curl -X GET http://127.0.0.1:5000/categories`

```
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    ...
  ], 
  "success": true, 
  "total_categories": 6
}
```

### GET /categories/`category_id`/questions

- Returns a list of questions in the given category, ID of the category, success value, and total number of questions
- Results are paginated in group of 10. Include a request argument to choose page number, starting from 1.
- Error of status code 404 is thrown when there is not question on the given page.

#### Sample

`curl -X GET http://127.0.0.1:5000/categories/1/questions?page=1`

```
{
  "current_category": 1, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
```

### GET /questions

- Returns a list of questions, success value, total number of questions, a list of categories, ID of current category (should be `null`), and success value
- Results are paginated in group of 10. Include a request argument to choose page number, starting from 1.
- Error of status code 404 is thrown when there is not question on the given page.

#### Sample

`curl -X GET http://127.0.0.1:5000/questions?page=1`

```
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    ...
  ], 
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    ...
  ], 
  "success": true, 
  "total_questions": 19
}
```

### POST /questions

- Creates a new question using the submitted question, answer, difficulty and category. All the parameters are required. Returns the created question and success value.

#### Sample

`curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question":"Which planet has a moon named Phobos?","answer":"Mars","difficulty":3,"category":1}'` 

```
{
  "created": {
    "answer": "Mars", 
    "category": 1, 
    "difficulty": 3, 
    "id": 25, 
    "question": "Which planet has a moon named Phobos?"
  }, 
  "success": true
}
```

- If `search_term` is included in request body, the result of search for questions based on the given search term is returned, which returns a list of matched questions, success value, total number of result, and current category as `null`
- Error of status code 404 is thrown when there is not question on the given page.

#### Sample

`curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"search_term":"title"}'` 

```
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```

### DELETE /questions/`question_id`

- Deletes the question of the given ID if it exists. Returns the id of the deleted question and success value
- If the question of the given ID does not exist, error of status code 404 is returned.

#### Sample

`curl -X DELETE http://127.0.0.1:5000/questions/25` 

```
{
  "deleted": 25, 
  "success": true
}
```

### POST /quizzes

- Returns one of the randomly chosen questions in the given category and success value.
- If `previous_questions` is provided in request body, they are excluded from selecting process. 
- `question` is returned as `null` if there is no more questions which has not previously played in the category. 

#### Sample

`curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"quiz_category":{"type":"Science","id":1},"previous_questions":[20]}'` 

```
{
  "question": {
    "answer": "Alexander Fleming", 
    "category": 1, 
    "difficulty": 3, 
    "id": 21, 
    "question": "Who discovered penicillin?"
  }, 
  "success": true
}
```
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
