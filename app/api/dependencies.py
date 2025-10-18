from ..database import SessionLocal
from jose import JWTError, jwt
from ..core.config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    This dependency decodes the JWT token, validates it, and returns the
    current user from the database.
    """
    # Define the exception to be raised if authentication fails.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT. This verifies the signature and expiration time.
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        # Extract the user ID (our 'sub' claim) from the payload.
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

    except JWTError:
        # If jwt.decode raises an error (bad signature, expired, etc.),
        # we raise our standard exception.
        raise credentials_exception

    # Now that we have the user_id, fetch the user from the database.
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()

    # If we didn't find a user with that ID in the database, it's an error.
    if user is None:
        raise credentials_exception

    # If all checks pass, return the complete User SQLAlchemy object.
    return user
