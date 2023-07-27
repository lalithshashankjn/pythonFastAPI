from fastapi import status as HTTPStatus, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["Authentication"])

@router.post("/login", status_code = HTTPStatus.HTTP_200_OK, response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session=Depends((get_db))):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() # our user name is the email here.

    if not user:
        raise HTTPException(status_code= HTTPStatus.HTTP_403_FORBIDDEN, details={"Invalid Credentials"})
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code= HTTPStatus.HTTP_403_FORBIDDEN, details={"Invalid Credentials"})
    
    # create a JWT token
    token = oauth2.create_access_token(data={"user_id": user.id})
    # return token
    return {"access_token" : token, "token_type": "bearer" }




