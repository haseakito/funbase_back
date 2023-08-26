from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""
Function handling the password hashing
"""
def hash_password(password: str):
    return pwd_context.hash(password)

"""
Function handling verifying the password
"""
def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)