import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie



CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IngyRHp5b2VmdjJBNEdBOHdLZGJvbCJ9.eyJpc3MiOiJodHRwczovL2FsYWEtZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZhZmUzYzc1NzdkY2EwMDY5YTg4ZGNhIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeU1vZGVscyIsImlhdCI6MTYwODc0NDIxMywiZXhwIjoxNjA4NzUxNDEzLCJhenAiOiJ5WnpJT3VPbk80NVcxWXQ3dTFuZnVxcXVjWTJlVk9qayIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.KhvW2nQR_cNhJIZXlBxd0Z8diGVtzEXf4zKxZHVSPf6argzJE8PR_Q01Eihhrv_1N0cYTSlT-d4nzpTl5DEUHS_PlmUZdggUaOFIIEh-romRcidwLQKFEYmI7Xsi8UnTfxU3EMnbTG2b5w_U9Coz--pkLH5tEAQCe1GSXFytYbN5AOh4V4Uk0x0J9iqUeJF3Uh_OB335w3B_WCuFkMTwb0fXN_MupWRTOqYrhew-6YzhB24kdBxVKoCd3Q5_4rTgZ7IMmv0x9ntateMOmRN6aD_Rii3Rm20ribCU2K1_dahr3h1tbTZTaIEO0MdbMY0d7mosJcYAqmJfKKQh7129wQ'

CASTING_DIRECTOR ='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IngyRHp5b2VmdjJBNEdBOHdLZGJvbCJ9.eyJpc3MiOiJodHRwczovL2FsYWEtZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZhMmVhNzA4OGEyNmYwMDZmNzQyYTJiIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeU1vZGVscyIsImlhdCI6MTYwODc0NDcyMywiZXhwIjoxNjA4NzUxOTIzLCJhenAiOiJ5WnpJT3VPbk80NVcxWXQ3dTFuZnVxcXVjWTJlVk9qayIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciJdfQ.elthkptQFgY8q-x-oOKl1wNQqHYejBJxoL4JBXZEPLcuMtMjS3qr85wN_HNDG5V3J2Ycz-ZAeX1q8AZRKfLKm7MP9emNRQqdqT_jP34a-GUcGq-sNphbD3Y3rVCdTIZoKiPvRvatB8BuFtvtyeSQhZJM6EcRRaxVmgTBP8UAPVNOG4G3u-EtQLCbzBJTaP3DxiP48G4f3UH6N09yMeDfqkh3BbGnyWkIqW9cBTAHif3kOxmAqdNp1BWvmXG-cEVl92Daw8X78XR8UnsxCqR7XNY6ly9L0hzquA-Gq64VZM9q4hDp7CiokYNqIeSX7S1Hz2Q4n0TzdnGBhb4hezZj6Q'

EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IngyRHp5b2VmdjJBNEdBOHdLZGJvbCJ9.eyJpc3MiOiJodHRwczovL2FsYWEtZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZlMjI2Yzc4MTYzN2IwMDY4NWM5NzBkIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeU1vZGVscyIsImlhdCI6MTYwODc0NDI3OSwiZXhwIjoxNjA4NzUxNDc5LCJhenAiOiJ5WnpJT3VPbk80NVcxWXQ3dTFuZnVxcXVjWTJlVk9qayIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.YqMZ11UYZFIuKmXiUcx8j8G0vtMtCWg9AD8b7I3yHBqwfHADbB54jaNBTBEB0g7tV9iWzIPhGeMTMb3yq7iqPu6ejp0pcfG30JstIwYrNvc1KWj-8WT0NUJ5B2ENrgdBz1j-Q8lKR-S_WZBqDz1sZIgkyhawYXP5RSxuOrmqkKVl9qNJdV4gCoGANHYOPIamzyhMG_u9aHV4-5B5ZvbWJZjZSnHPKih27ct-eopgPJuZhQ9Q9t35Rx4E9KPu063vIpIOVB5w9E_2tbxOneeBVaIIWL4yRWoopWQ47cfPKIuFx_q88cRDFEq620l4RWV3e4sOGABRff_VsOCZrYq2tw'

class CastingAgencyModelsTestCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castingagency_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', '1234','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # set data for testing
        self.actor = {
        'name':'Jennifer Aniston',
        'age' : 51,
        'gender' : 'Female'
        }
        self.actor2 = {
        'name':'Leonardo DiCaprio',
        'age' : 56,
        'gender' : 'Male'
        }

        self.movie = {
        'title':'Titanic',
        'release_date' : '18-11-1997'}

        self.movie2 = {
        'title':'The Intouchables',
        'release_date' : '02-11-2011'}

        self.invalid_actor={
        "name" : "John"
        }

        self.invalid_movie={
        "title" : "The ring"
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
        res = self.client().post('/actors',
            json=self.actor,
            headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'})
        data = json.loads(res.data)
        # make sure the status code is created (201)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    ''' Test post new actor with invalid data'''
    def test_400_new_invalid_actor(self):
        res = self.client().post('/actors',
            json=self.invalid_actor,
            headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'})
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    ''' Test post new actor with 403 unauthorized error'''
    def test_403_new_actor(self):
        res = self.client().post('/actors',
            json=self.actor,
            headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'})
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')


# POST:MOVIE
    ''' Test post new movie '''
    def test_new_movie(self):
        res = self.client().post('/movies',
            json=self.movie,
            headers={"Authorization": f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(res.data)
        # make sure the status code is created (201)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    ''' Test post new movie with invalid data'''
    def test_400_new_invalid_movie(self):
        res = self.client().post('/movies',
            json=self.invalid_movie,
            headers={"Authorization": f'Bearer {EXECUTIVE_PRODUCER}'})
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    ''' Test post new movie with 403 unauthorized error'''
    def test_403_new_movie(self):
        res = self.client().post('/movies',
            json=self.movie,
            headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'})
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')


# GET:ACTORS
    ''' Test get_actors '''
    def test_get_actors(self):
        res = self.client().get('/actors', headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'})
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
        res = self.client().get('/movies', headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'})
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
        res = self.client().patch('/actors/3',
            json={"name":"John"},
            headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    ''' Test update non exist actor'''
    def test_404_upadte_invalid_actor(self):
        res = self.client().patch('/actors/100',
            json={"name":"John"},
            headers={"Authorization": f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    ''' Test update actor with 403 unauthorized error'''
    def test_403_update_actor(self):
        res = self.client().patch('/actors/3',
            json={"name":"John"},
            headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'})
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')



# PATCH:MOVIE
    ''' Test update movie '''
    def test_update_movie(self):
        res = self.client().patch('/movies/4',
            json={"title":"Joker"},
            headers={"Authorization": f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    ''' Test update non exist movies'''
    def test_404_upadte_invalid_movie(self):
        res = self.client().patch('/movies/100',
            json={"title":"Joker"},
            headers={"Authorization": f'Bearer {EXECUTIVE_PRODUCER}'})
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    ''' Test update actor with 403 unauthorized error'''
    def test_403_update_movie(self):
        res = self.client().patch('/movies/4',
            json={"title":"Joker"},
            headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'})
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')





# DELETE:ACTOR
    ''' Test Delete actor '''
    def test_delete_movie(self):
        response = self.client().delete('/actors/3',headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 3)

    ''' Test Delete actor '''
    def test_403_delete_actor(self):
        response = self.client().delete('/actors/3',headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

# DELETE:MOVIE
    ''' Test Delete movie '''
    def test_delete_movie(self):
        response = self.client().delete('/movies/6',headers={"Authorization": f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 6)

    ''' Test Delete movie '''
    def test_403_delete_movie(self):
        response = self.client().delete('/movies/7',headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
