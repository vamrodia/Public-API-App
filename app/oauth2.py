# Modules/Library Imports and initialization
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import os

# Component needed for the OAuth2 functionality with the API Path "login"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Setting up the CONSTANTS declaration
SECRET_KEY = os.environ.get("API_APP_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# Function to create an Access Token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# Function to Decode the Hash and compares with ID Value in the payload
def verify_access_token(token: str, credential_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_identity: str = payload.get("user_id")

        if user_identity is None:
            raise credential_exception
        token_data = schemas.TokenData(id=user_identity)

    except JWTError:
        raise credential_exception

    return token_data


# Function to fetch the DB Values which are in turn being used for auditing and other purposes
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail=f"Could not validate your credentials",
                                         headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credential_exception)
    fetched_user = db.query(models.User).filter(models.User.id == token.id).first()

    return fetched_user
    # return verify_access_token(token, credential_exception)





