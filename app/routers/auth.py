from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, utils, oauth2, schemas

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', status_code=status.HTTP_200_OK)
def login(user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email==user_data.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Invalid credentials')
    
    if not utils.verify(user_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Invalid credentials')
    
    access_token = oauth2.create_access_token(data={'user_id': user.id})

    return {'access_token': access_token, 'token_type': 'bearer'}
