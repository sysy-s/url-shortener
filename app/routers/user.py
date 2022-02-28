from fastapi import HTTPException, status, Depends, APIRouter
from pydantic import ValidationError
from sqlalchemy.orm import Session
from email_validator import validate_email, EmailNotValidError

from .. import schemas, models, utils
from .. database import get_db

router = APIRouter(
    tags=['Users']
)


@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    if user.password1 is '':
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Password blank')

    if not user.password1 == user.password2:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Passwords do not match')
    try:
        user.password1 = utils.hash(user.password1)
        user_dict = {'email': user.email, 'password': user.password1}
        new_user = models.User(**user_dict)
        db.add(new_user)
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email is shit')

    try:
        db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')
    db.refresh(new_user)
    return new_user
