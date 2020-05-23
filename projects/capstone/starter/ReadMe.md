# The Casting Agency

https://the-casting-agency.herokuapp.com/

## Full Stack Nano - Capstone Project

The Casting Agency models a company that is responsible 
for creating movies and managing and assigning actors to 
those movies. You are an Executive Producer within the 
company and are creating a system to simplify and streamline 
your process.

## Models:

Movies with attributes title and release date
Actors with attributes name, age and gender

## Endpoints:
GET /actors and /movies

DELETE /actors/ and /movies/

POST /actors and /movies

PATCH /actors/ and /movies/

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