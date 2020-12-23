import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor, db
from auth import AuthError, requires_auth
from datetime import datetime


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE')
    return response


# GET /actors
  @app.route('/actors')
  @requires_auth('get:actors')
  def get_actors(payload):
      try:
          all_actors= Actor.query.order_by(Actor.id).all()
          all_actors_formatted = [actor.format() for actor in all_actors]
          return jsonify({
          'success' : True,
          'actors' : all_actors_formatted
          })
      except BaseException:
          abort(422)

# GET /movies
  @app.route('/movies')
  @requires_auth('get:movies')
  def get_movies(payload):
      try:
          all_movies= Movie.query.order_by(Movie.id).all()
          all_movies_formatted = [movie.format() for movie in all_movies]
          return jsonify({
          'success' : True,
          'movies' : all_movies_formatted
          })
      except BaseException:
          abort(422)


# POST /actors
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actor')
  def new_actor(payload):
      body = request.get_json()
      name = body.get('name', None)
      age = body.get('age', None)
      gender = body.get('gender', None)

      if name is None or age is None or gender is None:
          abort(400)

      try:
          new_actor = Actor(name=name, age=age, gender=gender)
          new_actor.insert()
          return jsonify({
          'success' : True,
          'created' : new_actor.format()
          }), 201
      except BaseException as e:
          abort(422)

# POST /movies
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movie')
  def new_movie(payload):
      body = request.get_json()
      title = body.get('title', None)
      release_date = body.get('release_date', None)

      if title is None or release_date is None:
          abort(400)

      try:
          date = datetime.strptime(release_date, "%d-%m-%Y")
          new_movie = Movie(title=title, release_date=date)
          new_movie.insert()
          return jsonify({
          'success' : True,
          'created' : new_movie.format()
          }), 201
      except BaseException as e:
          abort(422)


# PATCH /actors
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actor')
  def update_actor(payload, actor_id):
      error_code = None
      body = request.get_json()
      name = body.get('name', None)
      age = body.get('age', None)
      gender = body.get('gender', None)

      if name is None and age is None and gender is None:
          abort(400)

      try:
          actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
          if actor is None:
              error_code=404

          if name is not None:
              actor.name = name
          if age is not None:
              actor.age = age
          if gender is not None:
              actor.gender = gender

          actor.update()
          return jsonify({
          'success' : True,
          'updated' : actor.format()
          }), 200
      except BaseException as e:
          if error_code == 404 :
              abort(404)
          abort(422)

# PATCH /movies
  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movie')
  def update_movie(payload, movie_id):
      error_code = None
      body = request.get_json()
      title = body.get('title', None)
      release_date = body.get('release_date', None)

      if title is None and release_date is None:
          abort(400)

      try:
          movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

          if movie is None:
              error_code = 404

          if title is not None:
              movie.title = title
          if release_date is not None:
              movie.release_date = release_date

          movie.update()
          return jsonify({
          'success' : True,
          'updated' : movie.format()
          }), 200
      except BaseException as e:
          if error_code == 404:
              abort(404)
          abort(422)


# DELETE /actors
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actor')
  def delete_actor(payload, actor_id):
      try:
          actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
          if actor is None:
              abort(404)
          else:
              actor.delete()
              return jsonify({
                'success' : True,
                'deleted' :actor_id
                }), 200
      except BaseException:
          db.session.rollback()
          abort(422)

# DELETE /movies
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movie')
  def delete_movie(payload, movie_id):
      try:
          movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
          if movie is None:
              abort(404)
          else:
              movie.delete()
              return jsonify({
              'success' : True,
              'deleted' :movie_id
              }), 200
      except BaseException:
          db.session.rollback()
          abort(422)


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
