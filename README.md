#  Casting Agency Models API

## Introduction
This is the capstone project for Udacity's FULL-STACK DEVELOPER NANODEGRE I've use all of the concepts and the skills that I gained from Nanodegree's courses.

Nowadays, technology solutions are very important to make work and life easier. Casting Agency Models is an API designed to management system that is responsible for creating movies and managing and assigning actors to those movies. The API shows list of actors and movies and providing features for managing them.

the app link
https://castingagencymodels.herokuapp.com


## Getting Started

To get started you must clone the repository to your device by running this command:
```
git clone https://github.com/AlaaAlhelal-hub/Capstone.git
```

### Installing Dependencies

1. To install Python 3.8 follow the instructions here (https://docs.python.org/3/)

2. install dependencies by running this command:
```
pip install -r requirements.txt
```

3. Make sure to editing the DATABASE_URL variable in the setup.sh file to database url of your database, after that run:
```
source setup.sh
```
This will setup the environment variables and run database migrations.


4. To run the server use the command below:
```
flask run
```



## API ARCHITECTURE AND TESTING

### Testing
To run tests, first you need to edit the DATABASE_URL_TEST variable in the test_app.sh file to your test database url, then run:
```
source test_app.sh
```
This will setup the test environment variables and run the tests.




### The Endpoints
A third-party authentication service Auth0 is used to handle authentication needs in the application and Role-Based-Access-Control is implemented in the app, which means authentication headers which contain JWT tokens and the required permissions will be used to access the endpoints.

There are three roles:

#### 1. Casting Assistant
    - Can view actors and movies

#### 2. Casting Director
    - Can view actors and movies
    - Add or delete an actor from the database
    - Modify actors or movies

#### 3. Executive Producer
    - Can view actors and movies
    - Add or delete an actor from the database
    - Add or delete a movie from the database
    - Modify actors or movies


### API Reference

### Endpoints

GET '/actors' \
GET '/movies' \
POST '/actors' \
POST '/movies' \
PATCH '/actors/<id>' \
PATCH '/movies/<id>' \
DELETE '/movies/<id>' \
DELETE '/movies/<id>'



GET '/actors'
- Returns the list of actors
- Request Arguments: None
- Response:
```
{
    "actors": [
        {
            "age": 48,
            "gender": "Male",
            "name": "The Rock"
        },
        {
            "age": 51,
            "gender": "Female",
            "name": "Jennifer Aniston"
        }
    ],
    "success": true
}
```

GET '/movies'
- Returns the list of movies
- Request Arguments: None
- Response:
```
{
    "movies": [
        {
            "release date": "18-07-2008",
            "title": "THE DARK KNIGHT"
        },
        {
            "release date": "22-11-1995",
            "title": "Toy Story"
        }
    ],
    "success": true
}
```

POST '/actors'
- Add actor to the database
- Request json format:
{
        "name":"Johnny Depp",
        "age" : 57,
        "gender" : "Male"
}
- Response:
```
{
    "created": {
        "age": 57,
        "gender": "Male",
        "name": "Johnny Depp"
    },
    "success": true
}
```

POST '/movies'
- Add movie to the database
- Request json format:
{
    "title":"Pirates of the Caribbean",
    "release_date":"28-06-2003"
}
- Response:
```
{
    "created": {
        "release date": "28-06-2003",
        "title": "Pirates of the Caribbean"
    },
    "success": true
}
```

PATCH '/actors/<id>'
- Update an actor in the database
- Request parameter: id
- Request json format: {
    "age": 59
  }
- Response:
```
{
    "success": true,
    "updated": {
        "age": 59,
        "gender": "Male",
        "name": "Johnny Depp"
    }
}
```

PATCH '/movies/<id>'
- Update a movie in the database
- Request Parameter: id
- Request json format: {
    "title": "Pirates of the Caribbean: The Curse of the Black Pearl"
  }
- Response:
```
{
    "success": true,
    "updated": {
        "release date": "28-06-2003",
        "title": "Pirates of the Caribbean: The Curse of the Black Pearl"
    }
}
```

DELETE '/actors/<id>'
- Deletes an actor with the specified id
- Request Parameter: id
- Response:
```
{
    "deleted": 4,
    "success": true
}
```

DELETE '/movies/<id>'
- Deletes a movie with the specified id
- Request Parameter: id
- Response:
```
{
    "deleted": 4,
    "success": true
}
```


The server returns these types of errors

400 - Bad Request
  {
    "success": false,
    "error": 400,
    "message": "bad request"
  }

404 - Resource Not Found
  {
    "success": false,
    "error": 404,
    "message": "resource not found"
  }

405 - Method not allowed
  {
    "success": false,
    "error": 405,
    "message": "Method not allowed"
  }

422 - Unprocessable
  {
    "success": false,
    "error": 422,
    "message": "unprocessable
  }
