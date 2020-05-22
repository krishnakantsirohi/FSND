import unittest
import json

from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Actors, Movies
from app import app, db
import requests


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.test_user = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikw5VlZGcHdrTTV3dXhmbXFZQ29aciJ9.eyJpc3MiOiJodHRwczovL2FnZWQtYnJlYWQtMDIzNy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVjODBjMzQ1MTAxOWUwY2NmNTg4OTA4IiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU5MDE2ODY1MSwiZXhwIjoxNTkwMTc1ODUxLCJhenAiOiJXMlppQ1FoSm1OdExHWDhSOHFrMTY5U1VuS1RWMDRjRiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOltdfQ.h6NoW_4ATu1kwamigPeexQonCgoTr4jiFXRFvm5rgereM2KJjl-bszrPuZ0lbcG74zr2HYgjGbEQUW4veFdH014xLGHJMLW9GdVlZZyZT00LcwIq4kTBV0ZIoJk6YC8vy3pZYZW6pxOND3jdy15R5cKOzSD9RGWf3msrh5FzDQWO4nlJVUcvJ6qrVZrWFgMoAAqvgOpNQk4Qe1jq73lV8rXwkYi_1ihdsgxXc8hAheiuec9jv6m4CepHTFAz-p16AoYMloG9c1TuTlI6AqONj40bSwZC4V2qnDoNsbZyWqWt7GpXITrrpgi_dYPTRFsd95w8SzjiCAvv2uJoaWr7vw'
        self.exec_prod = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikw5VlZGcHdrTTV3dXhmbXFZQ29aciJ9.eyJpc3MiOiJodHRwczovL2FnZWQtYnJlYWQtMDIzNy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVjNzczNDdlNmY0ZTAwYmYyMDI1MGFhIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU5MDE2ODkyOSwiZXhwIjoxNTkwMTc2MTI5LCJhenAiOiJXMlppQ1FoSm1OdExHWDhSOHFrMTY5U1VuS1RWMDRjRiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwibW9kaWZ5OmFjdG9ycyIsIm1vZGlmeTptb3ZpZXMiXX0.e822WnvnDB70NqdAlJRsoBwfDJWgKJMhhZh7oSm1BbEcixqff31zzKQ7bqsTOnZ36GMqfvlOknoCHptG_arBXtkgcb-StyaQ3TUV9xotd2a9efqQkb3xFP1diOYlTg_eMQq9ZW2pdDRjR3CEFMVr3-7nyQ5KG-t_Kef6yyMmKj7W6ZZxtFYmvnbfVct2QVRbN-9MN3B7ixdfk7Cfu_l-FaIRs6VVMnsXNc2zLmILxhL9rH5zURJosYrst-UsinIjbSKI_VAQdx_86sU_NRrDNRrwah6z00fCa5Lzp6_C2ox623A2fpSWJ7aPA_LuGWNoZrkkkz4aAGpzI-Lp2CrD2A'
        self.cast_direct = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikw5VlZGcHdrTTV3dXhmbXFZQ29aciJ9.eyJpc3MiOiJodHRwczovL2FnZWQtYnJlYWQtMDIzNy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVjNzczNzBlNmY0ZTAwYmYyMDI1MTRiIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU5MDE2ODg3NSwiZXhwIjoxNTkwMTc2MDc1LCJhenAiOiJXMlppQ1FoSm1OdExHWDhSOHFrMTY5U1VuS1RWMDRjRiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsIm1vZGlmeTphY3RvcnMiLCJtb2RpZnk6bW92aWVzIl19.czQ8iozFnNHPQkPcv0RRiAeXs_GkFT5sjpwy_7lZipmn1kNjl_CwmItfccAI-UIpu0EiDlJvgzi36bMBJKEZl8zbCH_50zOPQtXWmPWt1AsS4guGr79IlM8GSMWwRmBXbRAnWJZ5TTtcG2IPkqsT7O4aXy4CEMk0wYIJ_byZDj3Lon1cohpJpxlbf4gf41k_3QUwr51MaJi05lj_dTtAlqdGAZuw6NV7APle16yDRPreq2m7tO_tdW8A5QbeZ2Xe6O7rcEoAG0R2t0k6go9_R8bA9WUHULDCpUmJGfem8Fgjh6cwanldJR8385XDs7hnsiF36P1gYC7NNdffuAnfZw'
        self.cast_assist = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikw5VlZGcHdrTTV3dXhmbXFZQ29aciJ9.eyJpc3MiOiJodHRwczovL2FnZWQtYnJlYWQtMDIzNy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVjNzczNWVmOGQ2YWYwYmZiZThiYWU1IiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU5MDE2ODk4NCwiZXhwIjoxNTkwMTc2MTg0LCJhenAiOiJXMlppQ1FoSm1OdExHWDhSOHFrMTY5U1VuS1RWMDRjRiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.D-Y9g6_Aa3bz4g7lqDolanpNoUslmSsJoDsbe0T5xjuIQ6F85LqEOS_vhrIzyq4umcIUsqzyo4iSC4piXCwb4YIPDlvTLhDKfdAny7tJzzhRh5nZAe858iR9luLi0Xcyv78kFPESqiJmktixFbPEqXYs9vzer_lWDpdNO7gxMuJ63CVpy3YOR_5H-fQwDPzDhiO5CdJWRbEN3F5NpvVqtYIilVEGVHDgmBBh9nkvd40wRQr766n2P5KeAq1BhQW0u96GQoan_EYNRn_I0fNh2KSoGQHJuIqHJQm-XEnes4dgLDYbRarHBe0bm-C5V-tbfGi5Fshihwh38_n-h0N7uA'
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    # Adding new actor as Executive Producer
    def test_post_actors_as_producer(self):
        response = self.app.post('/actors', json={
            'name': 'Halsey',
            'age': '27',
            'gender': 'Female',
            'image_link': 'https://scontent-dfw5-1.xx.fbcdn.net/v/t1.0-9/p960x960/82940549_10156952642670975_7287561067444568064_o.jpg?_nc_cat=1&_nc_sid=85a577&_nc_ohc=7auHZ3Zvq3cAX9Q65oY&_nc_ht=scontent-dfw5-1.xx&_nc_tp=6&oh=11bf212b2ec507fc194d906c6ed203ed&oe=5EE5E402'
        }, headers={'Authorization': 'Bearer ' + self.exec_prod})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    # Adding new actor as Casting Director
    def test_post_actors_as_director(self):
        response = self.app.post('/actors', json={
            'name': 'Halsey',
            'age': '27',
            'gender': 'Female',
            'image_link': 'https://scontent-dfw5-1.xx.fbcdn.net/v/t1.0-9/p960x960/82940549_10156952642670975_7287561067444568064_o.jpg?_nc_cat=1&_nc_sid=85a577&_nc_ohc=7auHZ3Zvq3cAX9Q65oY&_nc_ht=scontent-dfw5-1.xx&_nc_tp=6&oh=11bf212b2ec507fc194d906c6ed203ed&oe=5EE5E402'
        }, headers={'Authorization': 'Bearer ' + self.cast_direct})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    # Adding new actor as Casting Assistant
    def test_post_actors_as_assistant(self):
        response = self.app.post('/actors', json={
            'name': 'Halsey',
            'age': '27',
            'gender': 'Female',
            'image_link': 'https://scontent-dfw5-1.xx.fbcdn.net/v/t1.0-9/p960x960/82940549_10156952642670975_7287561067444568064_o.jpg?_nc_cat=1&_nc_sid=85a577&_nc_ohc=7auHZ3Zvq3cAX9Q65oY&_nc_ht=scontent-dfw5-1.xx&_nc_tp=6&oh=11bf212b2ec507fc194d906c6ed203ed&oe=5EE5E402'
        }, headers={'Authorization': 'Bearer ' + self.cast_assist})
        self.assertEqual(401, response.status_code)

    # Adding new movie as Executive Producer
    def test_post_movies_as_producer(self):
        response = self.app.post('/movies', json={
            'title': 'Joker',
            'release_date': '2019-10-04',
            'image_link': 'https://pbs.twimg.com/media/EDEsh0gU4AUTO3P?format=jpg&name=900x900'
        }, headers={'Authorization': 'Bearer ' + self.exec_prod})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    # Adding new movie as Casting Director
    def test_post_movies_as_director(self):
        response = self.app.post('/movies', json={
            'title': 'Joker',
            'release_date': '2019-10-04',
            'image_link': 'https://pbs.twimg.com/media/EDEsh0gU4AUTO3P?format=jpg&name=900x900'
        }, headers={'Authorization': 'Bearer ' + self.cast_direct})
        self.assertEqual(401, response.status_code)

    # Adding new actor as Casting Assistant
    def test_post_movies_as_assistant(self):
        response = self.app.post('/movies', json={
            'title': 'Joker',
            'release_date': '2019-10-04',
            'image_link': 'https://pbs.twimg.com/media/EDEsh0gU4AUTO3P?format=jpg&name=900x900'
        }, headers={'Authorization': 'Bearer ' + self.cast_assist})
        self.assertEqual(401, response.status_code)

    # Get actors as Executive Producer
    def test_get_actors_as_producer(self):
        response = self.app.get('/actors', headers={'Authorization': 'Bearer ' + self.exec_prod})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    # Get actors as Casting Director
    def test_get_actors_as_director(self):
        response = self.app.get('/actors', headers={'Authorization': 'Bearer ' + self.cast_direct})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    # Get actors as Casting Assistant
    def test_get_actors_as_assistant(self):
        response = self.app.get('/actors', headers={'Authorization': 'Bearer ' + self.cast_assist})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    # Get actors as Test user
    def test_get_actors_as_test(self):
        response = self.app.get('/actors', headers={'Authorization': 'Bearer ' + self.test_user})
        self.assertEqual(401, response.status_code)

    # Get actor as Executive Producer
    def test_get_actor_as_producer(self):
        response = self.app.get('/actors/2', headers={'Authorization': 'Bearer ' + self.exec_prod})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    # Get actor as Casting Director
    def test_get_actor_as_director(self):
        response = self.app.get('/actors/2', headers={'Authorization': 'Bearer ' + self.cast_direct})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    # Get actor as Casting Assistant
    def test_get_actor_as_assistant(self):
        response = self.app.get('/actors/2', headers={'Authorization': 'Bearer ' + self.cast_assist})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    # Get actor as Test user
    def test_get_actor_as_test(self):
        response = self.app.get('/actors/2', headers={'Authorization': 'Bearer ' + self.test_user})
        self.assertEqual(401, response.status_code)

    # Get movies as Executive Producer
    def test_get_movies_as_producer(self):
        response = self.app.get('/movies', headers={'Authorization': 'Bearer ' + self.exec_prod})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    # Get movies as Casting Director
    def test_get_movies_as_director(self):
        response = self.app.get('/movies', headers={'Authorization': 'Bearer ' + self.cast_direct})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    # Get movies as Casting Assistant
    def test_get_movies_as_assistant(self):
        response = self.app.get('/movies', headers={'Authorization': 'Bearer ' + self.cast_assist})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    # Get movies as Test user
    def test_get_movies_as_test(self):
        response = self.app.get('/movies', headers={'Authorization': 'Bearer ' + self.test_user})
        self.assertEqual(401, response.status_code)

    # Get movie as Executive Producer
    def test_get_movie_as_producer(self):
        movie = Movies.query.first()
        response = self.app.get('/movies/'+str(movie.id), headers={'Authorization': 'Bearer ' + self.exec_prod})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    # Get movie as Casting Director
    def test_get_movie_as_director(self):
        movie = Movies.query.first()
        response = self.app.get('/movies/'+str(movie.id), headers={'Authorization': 'Bearer ' + self.cast_direct})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    # Get movie as Casting Assistant
    def test_get_movie_as_assistant(self):
        movie = Movies.query.first()
        response = self.app.get('/movies/'+str(movie.id), headers={'Authorization': 'Bearer ' + self.cast_assist})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    # Get movies as Test user
    def test_get_movie_as_test(self):
        response = self.app.get('/movies/2', headers={'Authorization': 'Bearer ' + self.test_user})
        self.assertEqual(401, response.status_code)

    # Patch actor as Executive Producer
    def test_patch_actors_as_producer(self):
        actor = Actors.query.order_by(Actors.id.desc()).first()
        response = self.app.patch('/actors/'+str(actor.id), json={
            'name': actor.name,
            'age': actor.age,
            'gender': actor.gender,
            'image_link': ''
        }, headers={'Authorization': 'Bearer ' + self.exec_prod})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    # Patch actor as Casting Director
    def test_patch_actors_as_director(self):
        actor = Actors.query.order_by(Actors.id.desc()).first()
        response = self.app.patch('/actors/'+str(actor.id), json={
            'name': actor.name,
            'age': actor.age,
            'gender': actor.gender,
            'image_link': ''
        }, headers={'Authorization': 'Bearer ' + self.cast_direct})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    # Patch actor as Casting Assistant
    def test_patch_actors_as_assistant(self):
        actor = Actors.query.order_by(Actors.id.desc()).first()
        response = self.app.patch('/actors/'+str(actor.id), json={
            'image_link': ''
        }, headers={'Authorization': 'Bearer ' + self.cast_assist})
        self.assertEqual(401, response.status_code)

    # Patch movie as Executive Producer
    def test_patch_movies_as_producer(self):
        movie = Movies.query.order_by(Movies.id.desc()).first()
        response = self.app.patch('/movies/'+str(movie.id), json={
            'title': movie.title,
            'release_date': movie.release_date,
            'image_link': ''
        }, headers={'Authorization': 'Bearer ' + self.exec_prod})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    # Patch movie as Casting Director
    def test_patch_movies_as_director(self):
        movie = Movies.query.order_by(Movies.id.desc()).first()
        response = self.app.patch('/movies/'+str(movie.id), json={
            'title': movie.title,
            'release_date': movie.release_date,
            'image_link': ''
        }, headers={'Authorization': 'Bearer ' + self.cast_direct})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    # Patch movie as Casting Assistant
    def test_patch_movies_as_assistant(self):
        response = self.app.patch('/movies/3', json={
            'image_link': ''
        }, headers={'Authorization': 'Bearer ' + self.cast_assist})
        self.assertEqual(401, response.status_code)

    # Delete actor as Executive Producer
    def test_delete_actors_as_producer(self):
        actor = Actors.query.order_by(Actors.id.desc()).first()
        response = self.app.delete('/actors/'+str(actor.id), headers={'Authorization': 'Bearer ' + self.exec_prod})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    # Delete actor as Casting Director
    def test_delete_actors_as_director(self):
        actor = Actors.query.order_by(Actors.id.desc()).first()
        print(actor.id)
        response = self.app.delete('/actors/'+str(actor.id), headers={'Authorization': 'Bearer ' + self.cast_direct})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    # Delete actor as Casting Assistant
    def test_delete_actors_as_assistant(self):
        actor = Actors.query.order_by(Actors.id.desc()).first()
        response = self.app.delete('/actors/'+str(actor.id), headers={'Authorization': 'Bearer ' + self.cast_assist})
        self.assertEqual(401, response.status_code)

    # Delete movie as Executive Producer
    def test_delete_movies_as_producer(self):
        movie = Movies.query.order_by(Movies.id.desc()).first()
        response = self.app.delete('/movies/'+str(movie.id), headers={'Authorization': 'Bearer ' + self.exec_prod})
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    # Delete movie as Casting Director
    def test_delete_movies_as_director(self):
        movie = Movies.query.order_by(Movies.id.desc()).first()
        response = self.app.delete('/movies/'+str(movie.id), headers={'Authorization': 'Bearer ' + self.cast_direct})
        self.assertEqual(401, response.status_code)

    # Delete movie as Casting Assistant
    def test_delete_movies_as_assistant(self):
        movie = Movies.query.order_by(Movies.id.desc()).first()
        response = self.app.delete('/movies/'+str(movie.id), headers={'Authorization': 'Bearer ' + self.cast_assist})
        self.assertEqual(401, response.status_code)


if __name__ == "__main__":
    unittest.main()
