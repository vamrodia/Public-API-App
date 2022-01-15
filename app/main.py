# Modules/Library Imports and initialization

# from typing import Optional, List
# from fastapi.params import Body
# from random import randrange
# from sqlalchemy.orm import Session
from fastapi import FastAPI  # Response, status, HTTPException, Depends
import os

from starlette.middleware.cors import CORSMiddleware

from . import models  # schemas, utils
from .database import engine  # get_db
from .routers import posts, users, auth, votes

# Environment Variables initialization
mysql_user = os.environ.get("MYSQL_USER")
mysql_pass = os.environ.get("MYSQL_PASS")


# CONSTANTS Declaration
DATABASE_NAME = "fastapi"
origins = ["*"]

# Declaring the Fast API Application Name
app = FastAPI()


# Allowlist for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQL Alchemy requirement for creating MySQL Tables

# models.Base.metadata.create_all(bind=engine)


# Some functions needed for logical functionality. MIGHT NOT BE needed after using SQL Alchemy
def find_post(identity):
    for post in my_posts:
        if post["id"] == identity:
            return post


def find_post_index(identity):
    for index, post in enumerate(my_posts):
        if post["id"] == identity:
            return index


my_posts = [{"title": "This is the first test post", "content": "This is the first test post content", "id": 100}]

# Initialization for all the child Router Paths for Fast API
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


# Creating the GET Requests to fetch the Root Path
@app.get("/")
async def root():
    return {"message": "Welcome to this Basic API Application created by Vibhor Amrodia"}
