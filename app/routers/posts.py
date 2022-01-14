# Modules/Library Imports and initialization

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional

# Setting the Prefix to reduce typing when creating individual paths and
# also adding "tags" for API Documentation grouping
router = APIRouter(prefix="/posts", tags=["Posts"])


# Creating the GET Requests to fetch the Posts
@router.get("/", response_model=List[schemas.PostVote])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                    limit: int = 100, offset: int = 0, search: Optional[str] = ""):
    # Using the SQL ALCHEMY
    print(f"User Account Accessing the API: {current_user.email}")  # Printing the user attributes from the "Depends"

    # This would filter out the posts based on the User ID

    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id)
    # .filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()

    # This would fetch all the posts
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()
    vote_posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).\
        join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).\
        filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()

    # Using MYSql Queries Manually
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # return {"data": posts} # Return it with data JSON format
    return vote_posts


# Creating the GET Requests to fetch the latest Post
@router.get("/latest", response_model=List[schemas.PostVote])
def get_posts_id(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(f"User Account Accessing the API: {current_user.email}")  # Printing the user attributes from the "Depends"
    # new_post = db.query(models.Post).filter(models.Post.owner_id == current_user.id)\
    #     .order_by(desc(models.Post.id)).first()

    new_post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")). \
        join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id).filter(models.Post.owner_id == current_user.id)\
        .order_by(desc(models.Post.id)).first()

    # cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1 """)
    # new_post = cursor.fetchone()
    return {new_post}


# Creating the GET Requests to fetch the Posts using POST ID
@router.get("/{identity}",  response_model=schemas.PostVote)
def get_posts_id(identity: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Using the SQL ALCHEMY
    print(f"User Account Accessing the API: {current_user.email}")  # Printing the user attributes from the "Depends"
    # post = db.query(models.Post).filter(models.Post.id == identity).first()

    post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).\
        join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id).filter(models.Post.id == identity).first()

    # Using MYSql Queries Manually
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (identity,))
    # post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with ID: {identity} does not exist")

    # Using this logic to User Specific Filtering
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not allowed to view this post")

    # return {"data": post} # Return it with data JSON format
    return post


# Creating the POST Request
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.Post, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # Using the SQL ALCHEMY
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    print(f"User Account Accessing the API: {current_user.email}")  # Printing the user attributes from the "Depends"

    # Using MYSql Queries Manually
    # cursor.execute("""INSERT INTO posts (title, content, published) values (%s, %s, %s) """,
    #                (post.title, post.content, post.published))
    # cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1 """)
    # new_post = cursor.fetchone()
    # connection.commit()
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # return {"data": new_post} # Return it with data JSON format
    return new_post


# Creating the DELETE Request to delete Post with specific identity
@router.delete("/{identity}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(identity: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Using the SQL ALCHEMY
    print(f"User Account Accessing the API: {current_user.email}")
    post_query = db.query(models.Post).filter(models.Post.id == identity)

    post = post_query.first()
    # Using MYSql Queries Manually
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (identity,))
    # response = cursor.fetchone()
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with ID: {identity} does not exist")

    # Using this logic to User Specific Filtering
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not allowed to delete this post")

    # Using the SQL ALCHEMY
    post_query.delete(synchronize_session=False)
    db.commit()

    # Using MYSql Queries Manually
    # cursor.execute("""DELETE FROM posts WHERE id = %s """, (identity,))
    # connection.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Creating the PUT Requests to update the Post using ID
@router.put("/{identity}", response_model=schemas.PostResponse)
def put_posts_id(identity: int, post: schemas.Post, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # Using the SQL ALCHEMY
    print(f"User Account Accessing the API: {current_user.email}")
    post_query = db.query(models.Post).filter(models.Post.id == identity)
    post_fetched = post_query.first()

    # Using MYSql Queries Manually
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (identity,))
    # response = cursor.fetchone()
    if post_fetched is None:
        raise HTTPException(status_code=404, detail=f"Post with ID: {identity} does not exist")

    # Using this logic to User Specific Filtering
    if post_fetched.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not allowed to update this post")

    # Using the SQL ALCHEMY
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    # Using MYSql Queries Manually
    #     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s """,
    #                    (post.title, post.content, post.published, identity))
    #     connection.commit()
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (identity,))
    # post_dict = cursor.fetchone()
    # return {"data": post_query.first()} # Return it with data JSON format
    return post_query.first()
