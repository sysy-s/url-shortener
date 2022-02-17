from fastapi import status, HTTPException, Depends, Response, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .. import schemas, models, utils
from .. database import get_db

router = APIRouter(
    tags=['Users']
)

@router.post("/register", response_model=schemas.UserOut, responses={409: {"model": schemas.Message}})
def create_user(response: Response, user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    
    db.add(new_user)
    try:
        db.commit()
    except:
        response.status_code = status.HTTP_409_CONFLICT
        return JSONResponse(content={"message": f"User with email '{user.email}' exists or email not valid"})
    db.refresh(new_user)
    return new_user

@router.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return user