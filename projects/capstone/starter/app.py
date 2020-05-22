"""Python Flask WebApp Auth0 integration example
"""
import os
from functools import wraps

import requests
import json
import auth as auth
from os import environ as env
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from forms import ActorForm, MovieForm
from dotenv import load_dotenv, find_dotenv
from flask import (Flask, jsonify, redirect, render_template,
                   session, url_for, request, abort, flash)
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
from config import BaseConfig

import constants

# noinspection PyUnresolvedReferences
from models import Movies, Actors

from models import setup_db

url = 'http://the-casting-agency.herokuapp.com'

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_CALLBACK_URL = env.get(constants.AUTH0_CALLBACK_URL)
AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = setup_db(app=app)
CORS(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin',
                         'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET, POST, PATCH, DELETE, OPTIONS')
    return response


@app.errorhandler(Exception)
def handle_auth_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response


oauth = OAuth(app)

is_loggedin = False

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


def requires_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if constants.PROFILE_KEY not in session:
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated


# Controllers API
@app.route('/')
def index():
    if session:
        return render_template('home.html', permissions=session['permissions'])
    return render_template('main.html', permissions=None)


app.add_url_rule('/', 'index', index)


@app.route('/callback')
def callback_handling():
    auth0.authorize_access_token()
    session['access_token'] = auth0.token['access_token']
    session['id_token'] = auth0.token['id_token']
    session['permissions'] = \
        auth.verify_decode_jwt(session['access_token'])['permissions']
    session['authorized'] = True
    resp = auth0.get('userinfo')
    userinfo = resp.json()
    session[constants.JWT_PAYLOAD] = userinfo
    session[constants.PROFILE_KEY] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    session['authorized'] = True
    return redirect('/home')


@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL,
                                    audience=AUTH0_AUDIENCE)


@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for(endpoint='index', _external=True),
              'client_id': AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


@app.route('/home')
def home():
    return render_template('home.html', permissions=session['permissions'])


@app.context_processor
def is_authorized():
    if 'authorized' in session:
        return dict(authorized=session['authorized'])
    return dict(authorized=False)


@app.route('/actors/show')
@requires_login
def show_actors():
    actors = json.loads(
        requests.get(url + '/actors',
                     headers={'Authorization':
                              'Bearer ' + session['access_token']}).text)
    return render_template('listitems.html', items=actors)


@app.route('/actors/<int:id>/show')
@requires_login
def show_actor(id):
    actor = json.loads(
        requests.get(url + '/actors/' + str(id),
                     headers={'Authorization':
                              'Bearer ' + session['access_token']}).text)
    return render_template('listdetails.html',
                           item=actor, permissions=session['permissions'])


@app.route('/actors/<int:id>/edit')
@requires_login
def edit_actor(id):
    actor = json.loads(
        requests.get(url + '/actors/' + str(id),
                     headers={'Authorization':
                              'Bearer ' +
                              session['access_token']}).text)['actor']
    form = ActorForm()
    form.name.data = actor['name']
    form.age.data = actor['age']
    form.gender.data = actor['gender']
    form.image_link.data = actor['image_link']
    return render_template('form_actors.html', form=form)


@app.route('/actors/<int:id>/edit', methods=['POST'])
@requires_login
def edit_actor_submission(id):
    data = request.form
    req = requests.patch(url + '/actors/' + str(id),
                         headers={'Authorization':
                                  'Bearer ' + session['access_token']},
                         json=data)
    return redirect(url_for('show_actor', id=id))


@app.route('/actors/add', methods=['GET'])
@requires_login
def new_actors_form():
    form = ActorForm()
    return render_template('form_actors.html', form=form)


@app.route('/actors/add', methods=['POST'])
@requires_login
def new_actors_submission():
    data = request.form.to_dict()
    resp = json.loads(
        requests.post(url + '/actors',
                      headers={'Authorization':
                               'Bearer ' + session['access_token']},
                      json=data).text)
    return redirect(url_for('show_actor', id=resp['id']))


@app.route('/actors/<int:id>/delete', methods=['GET'])
@requires_login
def remove_actor(id):
    resp = json.loads(requests.delete(url + '/actors/' + str(id),
                                      headers={'Authorization':
                                               'Bearer '
                                               +
                                               session['access_token']}).text)
    flash(resp['message'])
    return redirect(url_for('index'))


@app.route('/movies/show')
@requires_login
def show_movies():
    movies = json.loads(
        requests.get(url + '/movies',
                     headers={'Authorization':
                              'Bearer ' + session['access_token']}).text)
    return render_template('listitems.html', items=movies)


@app.route('/movies/<int:id>/show')
@requires_login
def show_movie(id):
    movie = json.loads(
        requests.get(url + '/movies/' + str(id),
                     headers={'Authorization':
                              'Bearer ' + session['access_token']}).text)
    return render_template('listdetails.html',
                           item=movie, permissions=session['permissions'])


@app.route('/movies/<int:id>/edit')
@requires_login
def movies_edit_form(id):
    movie = Movies.query.get(id)
    form = MovieForm()
    form.title.data = movie.title
    form.release_date.data = movie.release_date
    form.image_link.data = movie.image_link
    return render_template('form_movies.html', form=form)


@app.route('/movies/<int:id>/edit', methods=['POST'])
@requires_login
def movies_edit_submission(id):
    data = request.form
    req = requests.patch(url + '/movies/' + str(id),
                         headers={'Authorization':
                                  'Bearer ' + session['access_token']},
                         json=data)
    return redirect(url_for('show_movie', id=id))


@app.route('/movies/add')
@requires_login
def new_movie_form():
    form = MovieForm()
    return render_template('form_movies.html', form=form)


@app.route('/movies/add', methods=['POST'])
@requires_login
def new_movie_submission():
    form = request.form
    resp = json.loads(
        requests.post(url + '/movies',
                      headers={'Authorization':
                               'Bearer ' + session['access_token']},
                      json=form).text)
    return redirect(url_for('show_movie', id=resp['id']))


@app.route('/movies/<int:id>/delete')
@requires_login
def movies_delete(id):
    resp = json.loads(requests.delete(url + '/movies/' + str(id),
                                      headers={'Authorization':
                                               'Bearer ' +
                                               session['access_token']}).text)
    flash(resp['message'])
    return redirect(url_for('home'))


@app.route('/actors', methods=['GET'])
@auth.requires_auth('get:actors')
def get_actors(permissions):
    actors = Actors.query.order_by(Actors.id).all()
    actors = [a.format() for a in actors]
    return jsonify({
        'success': True,
        'actors': actors,
        'total': len(actors)
    })


@app.route('/actors/<int:id>', methods=['GET'])
@auth.requires_auth('get:actors')
def get_actor(permissions, id):
    actor = Actors.query.filter(Actors.id == id).one_or_none()
    if actor is None:
        abort(404)
    return jsonify({
        'success': True,
        'actor': actor.format()
    })


@app.route('/actors', methods=['POST'])
@auth.requires_auth('add:actors')
def add_actors(permission):
    data = request.get_json()
    actor = Actors(name=data['name'],
                   age=data['age'],
                   gender=data['gender'],
                   image_link=data['image_link'])
    actor.insert()
    actor = Actors.query.order_by(Actors.id.desc()).first()
    return jsonify({
        'success': True,
        'id': actor.id,
        'message': 'Actor ' + actor.name + ' added successfully.'
    })


@app.route('/actors/<int:id>', methods=['PATCH'])
@auth.requires_auth('modify:actors')
def update_actors(permission, id):
    actor = Actors.query.get(id)
    data = request.get_json()
    actor.name = data['name']
    actor.age = data['age']
    actor.gender = data['gender']
    actor.image_link = data['image_link']
    actor.update()
    return jsonify({
        'success': True,
        'message': 'Actor ' + actor.name + ' updated successfully.'
    })


@app.route('/actors/<int:id>', methods=['DELETE'])
@auth.requires_auth('delete:actors')
def delete_actor(permission, id):
    actor = Actors.query.get(id)
    if actor is None:
        abort(404)
    actor_name = actor.name
    actor.delete()
    return jsonify({
        'success': True,
        'message': 'Actor ' + actor_name + ' deleted successfully.'
    })


@app.route('/movies', methods=['GET'])
@auth.requires_auth('get:movies')
def get_movies(permissions):
    movies = Movies.query.order_by(Movies.id).all()
    movies = [m.format() for m in movies]
    return jsonify({
        'success': True,
        'movies': movies,
        'total': len(movies)
    })


@app.route('/movies/<int:id>', methods=['GET'])
@auth.requires_auth('get:movies')
def get_movie(permissions, id):
    movie = Movies.query.filter(Movies.id == id).one_or_none()
    if movie is None:
        abort(404)
    return jsonify({
        'success': True,
        'movie': movie.format()
    })


@app.route('/movies/<int:id>', methods=['DELETE'])
@auth.requires_auth('delete:movies')
def delete_movie(permissions, id):
    movie = Movies.query.get(id)
    movie_title = movie.title
    if movie is None:
        abort(404)
    movie.delete()
    return jsonify({
        'success': True,
        'message': 'Movie ' + movie_title + ' deleted successfully'
    })


@app.route('/movies', methods=['POST'])
@auth.requires_auth('add:movies')
def add_movie(permission):
    data = request.get_json()
    movie = Movies(title=data['title'],
                   release_date=data['release_date'],
                   image_link=data['image_link'])
    movie.insert()
    movie = Movies.query.order_by(Movies.id.desc()).first()
    return jsonify({
        'success': True,
        'id': movie.id,
        'message': 'Movie ' + movie.title + ' added successfully.'
    })


@app.route('/movies/<int:id>', methods=['PATCH'])
@auth.requires_auth('modify:movies')
def update_movies(permissions, id):
    movie = Movies.query.get(id)
    data = request.get_json()
    movie.title = data['title']
    movie.release_date = data['release_date']
    movie.image_link = data['image_link']
    movie.update()
    return jsonify({
        'success': True,
        'message': 'Movie updated successfully.'
    })


@app.errorhandler(400)
def error_400_bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
    }), 400


@app.errorhandler(401)
def error_401_unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    }), 401


@app.errorhandler(404)
def error_404_not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource not found'
    }), 404


@app.errorhandler(422)
def error_422_unprocessable(error):
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


@app.errorhandler(auth.AuthError)
def autherror(error):
    resp = jsonify(error.error)
    resp.status_code = error.status_code
    return resp


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='localhost', port=port, debug=True)
