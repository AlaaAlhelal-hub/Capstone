import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie


CASTING_ASSISTANT =
'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IngyRHp5b2VmdjJBNEdBOHdLZGJvbCJ9.eyJpc3MiOiJodHRwczovL2FsYWEtZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZhZmUzYzc1NzdkY2EwMDY5YTg4ZGNhIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeU1vZGVscyIsImlhdCI6MTYwODgwNjg1OCwiZXhwIjoxNjA4ODE0MDU4LCJhenAiOiJ5WnpJT3VPbk80NVcxWXQ3dTFuZnVxcXVjWTJlVk9qayIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.mr4cnqzG-SKugHbsLNdB37r_0ESddOQqL-1QL8xW4YUfdz62vcjzVgsQeaN8VaUPEpomeIq0aIbR0E-pOYMsRH26u4ZfgcWpqGtiBr0vP4MxluHd8HEipja8eouSgHv63bKxDyJRZBBW4XdUJMbaKj-WvfQ6Un6Zs7dDJqdv-Qv1WkY_L03SnYQufmo-u5gAPavirLI9rc9Cd2doyHQE6EfSzdNichn6eYoNt5m_hb2lJc-7Pa_k1Nz0UCY9bs4Sh3BxxmLd2YZ7ZEUi2M2szmwfBgEIMVWMOFlWVs50AOzcHGrnXn6xSFzy3ErEmsrbhSvpUTsbtcvcsiF4Vo7KfQ'

CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IngyRHp5b2VmdjJBNEdBOHdLZGJvbCJ9.eyJpc3MiOiJodHRwczovL2FsYWEtZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZhMmVhNzA4OGEyNmYwMDZmNzQyYTJiIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeU1vZGVscyIsImlhdCI6MTYwODgwNzExMCwiZXhwIjoxNjA4ODE0MzEwLCJhenAiOiJ5WnpJT3VPbk80NVcxWXQ3dTFuZnVxcXVjWTJlVk9qayIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciJdfQ.haAYVwHSn8yoqneLbOIf-0_MDA2QDnQNcWbj5brYeOoRaZJhrS58Hx_EwKY2PMnqEqOuMAdFTfmUcPLaaddUxSKB434Vr7PVh7ejFUnske9v21SmEeLhVt5OUsZecLwDsLe9KRyXgyWf0a89w3h06vTDb2lIcJPYEe7ENCNRAnM7_MKZupzcAOe6EaosWo5RhTgKafbSl43tZXSLD_RBuIgZYvDa-WKfFLw-tgkzGU1HQwjH6SuhrU5hRQYfQH7v-FSFAu7b-ZdAlnsBPLndusxaGe12k3gS2z6mPE1VWZ6NtNRFb7TEdFh3DFlo5DWBqjGGSNjTfqhpxkkouyV2Aw'

EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IngyRHp5b2VmdjJBNEdBOHdLZGJvbCJ9.eyJpc3MiOiJodHRwczovL2FsYWEtZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZlMjI2Yzc4MTYzN2IwMDY4NWM5NzBkIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeU1vZGVscyIsImlhdCI6MTYwODgwNzAzNSwiZXhwIjoxNjA4ODE0MjM1LCJhenAiOiJ5WnpJT3VPbk80NVcxWXQ3dTFuZnVxcXVjWTJlVk9qayIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.OH46JKQDrj100S26USW8LVHU7GmRPb_I5UxiXDWUyF87_htQ6N_EPx2UEzrQccFCLjsXtKsPllVqGqGuDvrVjsDgD26GJlb1R1572v65OWMvgD42s5xvFSzlifIcMdL6APCgtyA0phz_qTTBPpWE0ZyU5P6iiA0DWF2vtcidnX8yBnwQGDAaSE6dvadDnnpD14CpRoRcAXDw7kCj-LKpc9yObNxefpenxgjBuTOacOXvY9KkS3wKfhtOqTiHMcRuIDMOvO5eEyTlsisPamuzyU6I-MkrR45jAjl1sUbwlL5Mj2TkvoUatyBWAzLh7QLCAOb3091zgMcyf4Z3Oo4i2w'


class CastingAgencyModelsTestCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castingagency_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', '1234', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # set data for testing
        self.actor = {
            'name': 'Jennifer Aniston',
            'age': 51,
            'gender': 'Female'
        }
        self.actor2 = {
            'name': 'Leonardo DiCaprio',
            'age': 56,
            'gender': 'Male'
        }

        self.movie = {
            'title': 'Titanic',
            'release_date': '18-11-1997'}

        self.movie2 = {
            'title': 'The Intouchables',
            'release_date': '02-11-2011'}

        self.invalid_actor = {
            "name": "John"
        }

        self.invalid_movie = {
            "title": "The ring"
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


# POST:ACTOR
    ''' Test post new actor '''

    def test_new_actor(self):
        res = self.client().post(
            '/actors',
            json=self.actor,
            headers={
                "Authorization": f'Bearer {CASTING_DIRECTOR}'})
        data = json.loads(res.data)
        # make sure the status code is created (201)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    ''' Test post new actor with invalid data'''

    def test_400_new_invalid_actor(self):
        res = self.client().post(
            '/actors',
            json=self.invalid_actor,
            headers={
                "Authorization": f'Bearer {CASTING_DIRECTOR}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    ''' Test post new actor with 403 unauthorized error'''

    def test_403_new_actor(self):
        res = self.client().post(
            '/actors',
            json=self.actor,
            headers={
                "Authorization": f'Bearer {CASTING_ASSISTANT}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')


# POST:MOVIE
    ''' Test post new movie '''

    def test_new_movie(self):
        res = self.client().post(
            '/movies',
            json=self.movie,
            headers={
                "Authorization": f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(res.data)
        # make sure the status code is created (201)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    ''' Test post new movie with invalid data'''

    def test_400_new_invalid_movie(self):
        res = self.client().post(
            '/movies',
            json=self.invalid_movie,
            headers={
                "Authorization": f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    ''' Test post new movie with 403 unauthorized error'''

    def test_403_new_movie(self):
        res = self.client().post(
            '/movies',
            json=self.movie,
            headers={
                "Authorization": f'Bearer {CASTING_ASSISTANT}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')


# GET:ACTORS
    ''' Test get_actors '''

    def test_get_actors(self):
        res = self.client().get(
            '/actors',
            headers={
                "Authorization": f'Bearer {CASTING_ASSISTANT}'})
        # load te data from response
        data = json.loads(res.data)
        # make sure the status code is ok (200)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    ''' Test get actors failure without token'''

    def test_401_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'No Authorization header supplied')


# GET:MOVIES
    ''' Test get_movies '''

    def test_get_movies(self):
        res = self.client().get(
            '/movies',
            headers={
                "Authorization": f'Bearer {CASTING_ASSISTANT}'})
        # load te data from response
        data = json.loads(res.data)
        # make sure the status code is ok (200)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    ''' Test get movies failure without token'''

    def test_401_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'No Authorization header supplied')


# PATCH:ACTOR
    ''' Test update actor '''

    def test_update_actor(self):
        res = self.client().patch(
            '/actors/3',
            json={
                "name": "John"},
            headers={
                "Authorization": f'Bearer {CASTING_DIRECTOR}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    ''' Test update non exist actor'''

    def test_404_upadte_invalid_actor(self):
        res = self.client().patch(
            '/actors/100',
            json={
                "name": "John"},
            headers={
                "Authorization": f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    ''' Test update actor with 403 unauthorized error'''

    def test_403_update_actor(self):
        res = self.client().patch(
            '/actors/3',
            json={
                "name": "John"},
            headers={
                "Authorization": f'Bearer {CASTING_ASSISTANT}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')


# PATCH:MOVIE
    ''' Test update movie '''

    def test_update_movie(self):
        res = self.client().patch(
            '/movies/4',
            json={
                "title": "Joker"},
            headers={
                "Authorization": f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    ''' Test update non exist movies'''

    def test_404_upadte_invalid_movie(self):
        res = self.client().patch(
            '/movies/100',
            json={
                "title": "Joker"},
            headers={
                "Authorization": f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    ''' Test update actor with 403 unauthorized error'''

    def test_403_update_movie(self):
        res = self.client().patch(
            '/movies/4',
            json={
                "title": "Joker"},
            headers={
                "Authorization": f'Bearer {CASTING_ASSISTANT}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')


# DELETE:ACTOR
    ''' Test Delete actor '''

    def test_delete_movie(self):
        response = self.client().delete('/actors/3',
                                        headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 3)

    ''' Test Delete actor '''

    def test_403_delete_actor(self):
        response = self.client().delete('/actors/3',
                                        headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

# DELETE:MOVIE
    ''' Test Delete movie '''

    def test_delete_movie(self):
        response = self.client().delete('/movies/6',
                                        headers={"Authorization": f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 6)

    ''' Test Delete movie '''

    def test_403_delete_movie(self):
        response = self.client().delete('/movies/7',
                                        headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
