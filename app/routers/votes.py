# Modules/Library Imports and initialization

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional


# Setting the Prefix to reduce typing when creating individual paths and
# also adding "tags" for API Documentation grouping
router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(votes: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_exist = db.query(models.Post).filter(models.Post.id == votes.post_id).first()
    if not post_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {votes.post_id} does not exist")

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == votes.post_id,
                                               models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if votes.dir:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on the post {votes.post_id}")
        new_vote = models.Votes(post_id=votes.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully Added your Vote"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully Deleted your Vote"}
