import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app, resources={r"*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE')
    return response


# GET /actors and /movies
  @app.route('/actors')
  @requires_auth('get:actors')
  def get_actors(payload):
      return jsonify({'success' : True})

  @app.route('/movies')
  @requires_auth('get:movies')
  def get_movies(payload):
      return jsonify({'success' : True})


# POST /actors and /movies and
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actor')
  def new_actor(payload):
      return jsonify({'success' : True})

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movie')
  def new_movie(payload):
      return jsonify({'success' : True})


# PATCH /actors/ and /movies/
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actor')
  def update_actor(payload, actor_id):
      return jsonify({'success' : True})

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movie')
  def update_movie(payload, movie_id):
      return jsonify({'success' : True})


# DELETE /actors/ and /movies/
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actor')
  def delete_actor(payload, actor_id):
      return jsonify({'success' : True})

  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movie')
  def delete_movie(payload, movie_id):
      return jsonify({'success' : True})


  # Error Handling
  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
        }), 422

  @app.errorhandler(404)
  def notfound(error):
      return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
        }), 404

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
        'success': False,
        'status': 400,
        'message': 'bad request'
        }), 400

  @app.errorhandler(AuthError)
  def auth_error(error):
      return jsonify({
        'success': False,
        'status': error.status_code,
        'message': error.error['description']
        }), error.status_code

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
