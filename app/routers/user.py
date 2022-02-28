from fastapi import HTTPException, status, Depends, Response, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .. import schemas, models, utils
from .. database import get_db

router = APIRouter(
    tags=['Users']
)


@router.post("/register", response_model=schemas.UserOut, responses={409: {"model": schemas.Message}}, status_code=status.HTTP_201_CREATED)
def create_user(response: Response, user: schemas.UserCreate, db: Session = Depends(get_db)):

    if user.password1 != user.password2:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Passwords do not match')

    user.password1 = utils.hash(user.password1)
    user_dict = {'email': user.email, 'password': user.password1}
    new_user = models.User(**user_dict)
    db.add(new_user)

    try:
        db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User with email <{user.email}> exists or email not valid')
    db.refresh(new_user)
    return new_user
