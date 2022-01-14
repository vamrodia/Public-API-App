# Details for this Project - app - Public Version

## Description

This application is meant to deliver API capabilities. 

The objective is to use Fast API as the API Frontend and MySql as the Database Backend

We are using SQL Alchemy as the ORM(Object Relational Mapper)

## Workflow

Users can create posts with the following attributes: "Title", "Content", "Published" and do other CRUD operations for the same

We have JWT Token OAuth2 Authentication configured for the end users.

We have User Operations also available for scalability

## Usage

Under the folder scope for the application, run the following CLI: ```uvicorn app.main:app --reload```

## Requirements

1. pip install SQLAlchemy # SQL Alchemy
2. pip install "fastapi[all]" # Fast API
3. pip install "python-jose[cryptography]" # Python Jose and other Cryptography
4. pip install "passlib[bcrypt]" # PassLib
5. pip3 install mysql-connector-python # MySQL Connector
6. pip3 install urllib3 # URL Lib
7. pip3 install alembic # Alembic DB Migration https://alembic.sqlalchemy.org/en/latest/

All the required modules/package are listed under the "requirements.txt" file and can be installed on your target machine as:

```pip freeze > requirements.txt```

```pip install -r requirements.txt```

## Components

1. database.py - Module for creating the MySQL Database attributes
2. main.py - Module which is the main function used to initialize Fast API, API Router configuration. 
This includes some functions as well for some complementary functionality.
3. models.py - Module to define the MySQL Tables models for SQL Alchemy
4. oauth2.py - Module used to Create, Validate OAuth2 Token and collect User DB Attributes
5. schemas.py - Module defining Pydantic Models for all the different API Paths
6. utils.py - Module to separate Password Hashing and comparing password input for "users.py" module
7. routers[Directory]
   1. auth.py - Lists the API Path for User Login and Authentication path in the API Application
   2. posts.py - Lists the API Paths for posts operation for the API Application
   3. users.py - Lists the API Paths for user operation for the API Application

## Documentation URLs

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc
- fetch('http://localhost:8000/').then(res=>res.json()).then(console.log) $ Running API Calls from Browser


## Reference URLs

1. https://www.youtube.com/watch?v=0sOvCWFmrtA - Project Walkthrough
2. https://docs.sqlalchemy.org/en/14/orm/session_basics.html?highlight=opening%20closing%20session - SQL Alchemy
3. https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ - Fast API