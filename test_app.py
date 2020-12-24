import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie


CASTING_ASSISTANT =
'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IngyRHp5b2VmdjJBNEdBOHdLZGJvbCJ9.eyJpc3MiOiJodHRwczovL2FsYWEtZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZhZmUzYzc1NzdkY2EwMDY5YTg4ZGNhIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeU1vZGVscyIsImlhdCI6MTYwODgyODU4OCwiZXhwIjoxNjA4ODM1Nzg4LCJhenAiOiJ5WnpJT3VPbk80NVcxWXQ3dTFuZnVxcXVjWTJlVk9qayIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.WT7EZzS56HGUHZAu0vdu4fwYX0K2FE0WtycS251oS4uIteST_6S1tAwe06HBe15X1I_26c0YGZxCdW-CIJqBtUNAn78K1orFMN5OmwavCfLG6kN90vWRUP6FUwRpJ_S6eaw2jPd_ZUX_4Yc3m3RgqMAkGFJBH1uHqpE4khVYe5q0Ib9Z2VgdjTOzf6NxzW11AeHGoXWXNjyg31gOPlSZWnqk9g4hD4jimzn1HFO0zDcy2oT9ydQK0_0lpkxai_XTLuKjzQPxKIHBdm2Wvm2-3TPnyywOlvlHfT0d1IshZIC015T_oIu0mM4DR6KvMN_zaWdfSFDg_nDPtSLgA2-YNw'

CASTING_DIRECTOR ='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IngyRHp5b2VmdjJBNEdBOHdLZGJvbCJ9.eyJpc3MiOiJodHRwczovL2FsYWEtZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZhMmVhNzA4OGEyNmYwMDZmNzQyYTJiIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeU1vZGVscyIsImlhdCI6MTYwODgyODY5OSwiZXhwIjoxNjA4ODM1ODk5LCJhenAiOiJ5WnpJT3VPbk80NVcxWXQ3dTFuZnVxcXVjWTJlVk9qayIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciJdfQ.LVq_f1WJPk2vpzCAIlDYl6w8zs_Copvm6_lIXg_DfEUvNwUXEufDkqjJqFjzWY1fqMZu2gLDReBsEqTu5Ezf3Suv7uI1T88yQJo7CHmZfMaZbxUxBC3vAkPDLZF6FOW-1g2N4Ulmii2tn3D-r-AE6S0FPTIY_ql6Ac6oqPQXyQRtVvEncRD4LYDJYxmvI722KS1D8IjHcbNTy2YSy4DKMcTM1jGWO9bTSQ6Q66V_hyKLBzQpWpSEOqAwptHHpWnoKtxwVNc8j6qzYcVBlXerZJZ3fmpfWCN7FaKiz-Fmrglags8UdBdhFTNuIWpB00V8QlE4g0VLeCaXFVTfjWSlQw'

EXECUTIVE_PRODUCER ='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IngyRHp5b2VmdjJBNEdBOHdLZGJvbCJ9.eyJpc3MiOiJodHRwczovL2FsYWEtZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZlMjI2Yzc4MTYzN2IwMDY4NWM5NzBkIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeU1vZGVscyIsImlhdCI6MTYwODgyODU5MiwiZXhwIjoxNjA4ODM1NzkyLCJhenAiOiJ5WnpJT3VPbk80NVcxWXQ3dTFuZnVxcXVjWTJlVk9qayIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.Dz0dic1kxt4_aOYvi_wVmKTMksn82uhWnVFHRCl5cFarAui58JouPxmEKzCQRSysEqfGSRHjtwrPcHHn7S1YOCgJn7PdZXUq9CFXKDbhNyut8wpcgfZBZ249SGWNbXAcKG3wSi4Y7DpS4Yw_vDskgxy5lct9Bgyi0po6sOU6pxVR-Ffy85rpRxUqMYZZl0cco_Xx8ygTrr4-zvmOKB6foj3nmX5t2faOV9dKuOr0IWGlGpi8R6AYLM9yZHs_-5xmuUExG_RivL3sDpnMy6ctJqMDrYnM46X1XnFoDmrMYAmj7XueXigFWr6Wh41PbJZzBhkYkyN8fjm8GAbgn7aCBA'


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
