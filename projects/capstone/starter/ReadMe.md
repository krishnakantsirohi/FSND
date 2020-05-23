# The Casting Agency

https://the-casting-agency.herokuapp.com/

## Full Stack Nano - Capstone Project

The Casting Agency models a company that is responsible 
for creating movies and managing and assigning actors to 
those movies. 

You are an Executive Producer within the 
company and are creating a system to simplify and streamline 
your process.


## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

In the warranty-tracker directory, run the following to install all necessary dependencies:

```bash
pip install -r requirements.txt
```

This will install all of the required packages.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 


## Models:
The schema for the database and helper methods to simplify API behavior are in models.py:
- There are two tables created: Actors and Movies 
- The Actors table is used by the roles 'Casting Director' and 'Executive Producer' to add new Actors in the database.
- The Movies table is used by the role 'Executive Producer' to add new Movies in the database.
- The Actors and Movies table can be modified by roles 'Casting Director' and 'Executive Producer'.
- Each table has an insert, update, delete, and format helper functions.

## API ARCHITECTURE
### Endpoint Library
 
 @app.errorhandler decorators were used to format error responses as JSON objects. Custom @requires_auth decorator were used for Authorization based
 on roles of the user. Three roles are assigned to this API: 'Casting Assistant', 'Casting Director' and 'Executive Producer'.
 
####GET /actors
Returns a list of all the available actors in the database.

sample request:

curl http://localhost:5000/actors/  
-H "Authorization: Bearer {Insert Token here}" 

sample response:

{
  "actors": [
    {
      "age": 27,
      "gender": "Female",
      "id": 3,
      "image_link": "https://scontent-dfw5-1.xx.fbcdn.net/v/t1.0-9/p960x960/82940549_10156952642670975_7287561067444568064_o.jpg?_nc_cat=1&_nc_sid=85a577&_nc_ohc=OM0J51vtaGIAX_Pfs6z&_nc_ht=scontent-dfw5-1.xx&_nc_tp=6&oh=eb955796a7458bf4c4edacb4ac117dfc&oe=5EEDCD02",
      "name": "Selena Gomez"
    }
  ],
  "success": true,
  "total": 1
}

 
####GET /movies
Returns a list of all the movies in database

sample request:

curl http://localhost:5000/movies/  
-H "Authorization: Bearer {Insert Token here}" 

sample response:

{
  "movies": [
    {
      "id": 2,
      "image_link": "https://pbs.twimg.com/media/EDEsh0gU4AUTO3P?format=jpg&name=900x900",
      "release_date": "Fri, 04 Oct 2019 00:00:00 GMT",
      "title": "Joker 2019"
    }
  ],
  "success": true,
  "total": 1
} 

####GET /actors/<int:actor_id>
Returns a list of all the available actors in the database.

sample request:

curl http://localhost:5000/actors/4  
-H "Authorization: Bearer {Insert Token here}" 

sample response:

{
  "actor": {
    "age": 25,
    "gender": "Female",
    "id": 4,
    "image_link": "",
    "name": "Halsey"
  },
  "success": true
}

 
####GET /movies/<int:movie_id>
Returns a list of all the movies in database

sample request:

curl http://localhost:5000/movies/3  
-H "Authorization: Bearer {Insert Token here}" 

sample response:

{
  "movie": {
    "id": 3,
    "image_link": "",
    "release_date": "Thu, 20 Oct 2016 00:00:00 GMT",
    "title": "Robocop"
  },
  "success": true
}

####POST /actors
Adds a new actor into the database

sample request:

curl http://localhost:5000/actors/ 
-X POST 
-H "Content-Type: application/json" 
-H "Authorization: Bearer {Insert Token here}" 
-d 
'{
	"name": "Halsey",
	"age": 22,
	"image_link":"",
	"gender": "Female"
}'

sample response:

{
  "id": 4,
  "message": "Actor Halsey added successfully.",
  "success": true
}
 
####POST /movies
Adds a new movie into the database

sample request:

curl http://localhost:5000/movies/ 
-X POST 
-H "Content-Type: application/json" 
-H "Authorization: Bearer {Insert Token here}" 
-d 
'{
    "title": "Robocop",
    "release_date": "2016-05-20",
    "image_link":""
}'

sample response:

{
  "id": 3,
  "message": "Movie Robocop added successfully.",
  "success": true
}

####PATCH /actors/<int:actor_id>
Modify an actor with actor_id

sample request:

curl http://localhost:5000/actors/4 
-X PATCH 
-H "Content-Type: application/json" 
-H "Authorization: Bearer {Insert Token here}" 
-d 
'{
 	"name": "Halsey",
 	"age": 25,
 	"image_link":"",
 	"gender": "Female"
 }'

sample response:

{
  "message": "Actor Halsey updated successfully.",
  "success": true
}
 
####PATCH /movies/<int:movie_id>
Modify a movie with movie_id

sample request:

curl http://localhost:5000/movies/3 
-X PATCH 
-H "Content-Type: application/json" 
-H "Authorization: Bearer {Insert Token here}" 
-d 
'{
    "title": "Robocop",
    "release_date": "2016-10-20",
    "image_link":""
}'

sample response:

{
  "message": "Movie updated successfully.",
  "success": true
}

#### DELETE /actors/<int:actor_id>
Deletes an actor with actor_id from the database

sample request:

curl http://localhost:5000/actors/4 
-X DELETE 
-H "Content-Type: application/json" 
-H "Authorization: Bearer {Insert Token here}"

sample response:

{
  "message": "Actor Halsey deleted successfully.",
  "success": true
}

#### DELETE /movies/<int:movie_id>
Deletes a movie with movie_id from the database

sample request:

curl http://localhost:5000/movies/3 
-X DELETE 
-H "Content-Type: application/json" 
-H "Authorization: Bearer {Insert Token here}" 

sample response:

{
  "message": "Movie Robocop deleted successfully",
  "success": true
}

## Roles:
### Casting Assistant
Can view actors and movies

### Casting Director
All permissions a Casting Assistant has 

Add or delete an actor from the database

Modify actors or movies

### Executive Producer

All permissions a Casting Director has 

Add or delete a movie from the database


## THIRD-PARTY AUTHENTICATION
#### auth.py
Auth0 is set up and running. The following configurations are in a .env file which is exported by the app:
- The Auth0 Domain Name
- The JWT code signing secret
- The Auth0 Client ID

## Testing
There are 34 unittests in test_app.py. To run this file:

python test_app.py

The tests include one test for expected success and error behavior for each endpoint, and tests demonstrating role-based access control, 
where all endpoints are tested with and without the correct authorization.


## Credentials for Testing
### Casting Assistant

Email: assistant@ca.com

Password: Assist@2020

### Casting Director

Email: director@ca.com

password: Direct@2020

### Executive Producer

Email: test@ca.com

password: Test@2020