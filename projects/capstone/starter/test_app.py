import unittest
import json

from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Actors, Movies
from app import create_app


class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.database_path = "postgresql://{}/{}".format('postgres:1234@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        pass

    def test_post_actors(self):
        response = self.client().post('/actors', json={
            'name': 'Selena Gomez',
            'age': '27',
            'gender': 'Female',
            'image_link': 'https://scontent-dfw5-1.xx.fbcdn.net/v/t1.0-9/p960x960/82940549_10156952642670975_7287561067444568064_o.jpg?_nc_cat=1&_nc_sid=85a577&_nc_ohc=7auHZ3Zvq3cAX9Q65oY&_nc_ht=scontent-dfw5-1.xx&_nc_tp=6&oh=11bf212b2ec507fc194d906c6ed203ed&oe=5EE5E402'
        })
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    def test_post_movies(self):
        response = self.client().post('/movies', json={
            'title': '',
            'release_date': '',
            'image_link': ''
        })
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    def test_get_actors(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, data['success'])
        self.assertTrue(data['actors'])

    def test_get_movies(self):
        response = self.client.get('/actors')
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, data['success'])
        self.assertTrue(data['movies'])

    def test_patch_actors(self):
        response = self.client().patch('/actors/1/', json={
            'name': '',
            'age': '',
            'gender': '',
            'image_link': ''
        })
        data = json.loads(response.data)
        self.assertTrue(200, response.status_code)
        self.assertTrue(data['success'])

    def test_patch_movies(self):
        response = self.client().patch('/movies/1/', json={
            'title': '',
            'release_date': '',
            'image_link': ''
        })
        data = json.loads(response.data)
        self.assertTrue(200, response.status_code)
        self.assertTrue(data['success'])

    def test_delete_actors(self):
        response = self.client().delete('/actors/1')
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])

    def test_delete_movies(self):
        response = self.client().delete('/movies/1')
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['success'])


if __name__ == "__main__":
    unittest.main()
