from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.core import security
from app.core.database import get_db
from app.core.config import settings
from app.core.logging import logger
from app.models import User
from app.api.schemas import UserCreate, UserResponse, Token, TokenData

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Retrieve the authenticated User associated with the provided JWT access token.
    
    Returns:
        The matching User model instance.
    
    Raises:
        HTTPException: 401 Unauthorized with detail "Could not validate credentials" and header "WWW-Authenticate: Bearer" when the token is invalid, missing the subject (`sub`), or no user is found for the token's subject.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

def mask_email(email: str) -> str:
    """
    Mask an email address for privacy-safe logging.
    
    Returns:
        masked_email (str): The masked email where the local part is replaced with its first character plus '***' when the local part has more than one character (e.g., 'u***@example.com'). If the local part has one or zero characters, or the input is malformed or lacks an '@', returns '***' (no domain).
    """
    try:
        if "@" not in email:
            return "***"
        user, domain = email.split("@")
        if len(user) > 1:
            masked_user = user[0] + "***"
        else:
            masked_user = "***"
        return f"{masked_user}@{domain}"
    except:
        return "***"


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account from the provided registration data and persist it to the database.
    
    Parameters:
        user (UserCreate): Registration data containing at least `email` and `password`.
    
    Returns:
        UserResponse: The newly created user's public fields (for example `id` and `email`).
    
    Raises:
        HTTPException: With status 400 if the email is already registered.
        HTTPException: With status 500 if a database error occurs during creation.
    """
    logger.info(f"Attempting to register user with email: {mask_email(user.email)}")
    
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        logger.warning(f"Registration failed: Email {mask_email(user.email)} already registered.")
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = security.get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"User registered successfully: ID {new_user.id}, Email {mask_email(new_user.email)}")
        return new_user
    except Exception as e:
        logger.error(f"Database error during registration for email {mask_email(user.email)}: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Internal server error during registration"
        )

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate a user using credentials from the OAuth2 password form and issue a JWT access token.
    
    Parameters:
    	form_data (OAuth2PasswordRequestForm): Form containing `username` (user email) and `password`.
    	db (Session): Database session (injected dependency).
    
    Returns:
    	dict: A dictionary with keys `access_token` (the JWT string) and `token_type` (`"bearer"`).
    
    Raises:
    	HTTPException: If the user is not found or the password is incorrect (401 Unauthorized).
    """
    logger.info(f"Login attempt for email: {mask_email(form_data.username)}")
    
    # Authenticate user
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        logger.warning(f"Login failed: User {mask_email(form_data.username)} not found.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found. Please sign up first.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not security.verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Login failed: Incorrect password for email {mask_email(form_data.username)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create Access Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email},expires_delta=access_token_expires
    )
    
    logger.info(f"Login successful for user: {mask_email(user.email)}. Token generated.")
    return {"access_token": access_token, "token_type": "bearer"}