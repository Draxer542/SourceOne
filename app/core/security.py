from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
import bcrypt
from app.core.config import settings

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # bcrypt.checkpw requires bytes
    """
    Check whether a plaintext password matches a bcrypt hash.
    
    Parameters:
        plain_password (str): The plaintext password to verify.
        hashed_password (str): The bcrypt-hashed password to compare against.
    
    Returns:
        `true` if the plaintext password matches the hashed password, `false` otherwise.
    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

def get_password_hash(password: str) -> str:
    # bcrypt.hashpw returns bytes, decode to store as string
    """
    Create a bcrypt hash of the given plaintext password.
    
    Parameters:
        password (str): The plaintext password to hash.
    
    Returns:
        str: The bcrypt hash of the password, decoded to a UTF-8 string for storage.
    """
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token containing the provided payload and an expiration claim.
    
    Parameters:
        data (dict): Claims to include in the token payload.
        expires_delta (Optional[timedelta]): Time span until the token expires; if omitted, expires in 15 minutes.
    
    Returns:
        str: Encoded JWT signed with the configured secret key and algorithm.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt