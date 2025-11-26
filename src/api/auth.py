import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from utils.getSecrets import _get_secret

security = HTTPBasic()

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    # In a real application, you'd verify against a database
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, _get_secret("api_auth_secret"))

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username