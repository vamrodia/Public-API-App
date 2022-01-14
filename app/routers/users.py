# Modules/Library Imports and initialization
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

# Setting the Prefix to reduce typing when creating individual paths and
# also adding "tags" for API Documentation grouping
router = APIRouter(prefix="/users", tags=["Users"])


# Creating the API Path for adding a new user using a POST request
@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_pass = utils.hashed_password(user.password)  # Hash the Password
    user.password = hashed_pass
    new_user = models.User(**user.dict())  # Unpacking the dictionary to avoid declaring every key/value individually
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Creating the API Path for fetching a user using a the "id"
@router.get("/{identity}", response_model=schemas.UserResponse)
def get_user(identity: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == identity).first()

    if user_query is None:
        raise HTTPException(status_code=404, detail=f"User with ID: {identity} does not exist")

    else:
        return user_query
