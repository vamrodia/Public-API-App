# Modules/Library Imports and initialization
from passlib.context import CryptContext

# Component used as an element for the OAuth2 Functionality
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Function to create Hashed Password
def hashed_password(password: str):
    return pwd_context.hash(password)


# Function to verify Hashed Password
def verify_hash(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password)
