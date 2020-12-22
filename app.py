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

'''
GET /actors and /movies
DELETE /actors/ and /movies/
POST /actors and /movies and
PATCH /actors/ and /movies/
'''
# GET /actors and /movies
  @app.route('/actors')
  def get_actors():
      return jsonify({'success' : True})

  @app.route('/movies')
  def get_movies():
      return jsonify({'success' : True})


# POST /actors and /movies and
  @app.route('/actors/<int:actor_id>', methods=['POST'])
  def new_actor(actor_id):
      return jsonify({'success' : True})

  @app.route('/movies/<int:movie_id>', methods=['POST'])
  def new_movie(movie_id):
      return jsonify({'success' : True})


# PATCH /actors/ and /movies/
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  def update_actor(actor_id):
      return jsonify({'success' : True})

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  def update_movie(movie_id):
      return jsonify({'success' : True})


# DELETE /actors/ and /movies/
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  def delete_actor(actor_id):
      return jsonify({'success' : True})

  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  def delete_movie(movie_id):
      return jsonify({'success' : True})



  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
