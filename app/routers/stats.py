from typing import List, Optional
from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
import validators

from .. import models, schemas, oauth2
from ..database import get_db
from ..settings import BASE_URL

router = APIRouter(
    tags=['Statistics'],
    prefix='/stats'
)

@router.get("/", response_model=List[schemas.UrlRetrieve])
def get_user_url_statistics(search: Optional[str] = "", limit: int = 25,
                            current_user: str = Depends(oauth2.get_current_user),
                            db: Session = Depends(get_db)):

    current_user_urls = db.query(models.Url).filter(
                        and_(models.Url.user_id==current_user.id,
                        or_(models.Url.short.contains(search),
                            models.Url.long.contains(search)))).limit(limit).all()
    return current_user_urls

@router.get("/{short}")
def get_specific_url_statistics(response: Response, short: str,
                                current_user: str = Depends(oauth2.get_current_user),
                                db: Session = Depends(get_db)):

    url = db.query(models.Url).filter(models.Url.short==short).first()
    
    if url is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Url not found")
        
    if url.user_id is not current_user.id:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You're not the owner of this url")
    
    all_visits = db.query(models.Visit).filter(models.Visit.url_id==url.id).all()
    if all_visits:
        response.model = List[schemas.Visit]
        return all_visits

    return {"wow": "such empty"}

@router.put("/{short}")
def update_url(short: str,
                updated_url_data: schemas.UrlUpdate,
                current_user: str = Depends(oauth2.get_current_user),
                db: Session = Depends(get_db)):

    url_query = db.query(models.Url).filter(models.Url.short==short)
    url = url_query.first()
    
    """
    Three validators:
    * if it exists
    * if url is modifiable by the current user
    * if they're valid urls
    """

    if url is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Url not found")

    if url.user_id is not current_user.id:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You're not the owner of this url")

    if not validators.url(updated_url_data.long) or not updated_url_data.short.isalnum():
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Url '{updated_url_data.long}' or '{BASE_URL}/{updated_url_data.short}' is not a valid url")

    url_query.update(updated_url_data.dict())
    db.commit()
    db.refresh(url)
    
    return url

@router.delete("/{short}")
def delete_url_visits(short: str,
                    current_user: str = Depends(oauth2.get_current_user),
                    db: Session = Depends(get_db)):
    
    """
    Deletes all visits from url, and sets URL click count to 0 again
    """
    url_query = db.query(models.Url).filter(models.Url.short==short)
    url = url_query.first()

    if url is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Url not found")

    if url.user_id is not current_user.id:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You're not the owner of this url")

    visits_query = db.query(models.Visit).filter(models.Visit.url_id==url.id)
    visits_query.delete(synchronize_session=False)
    url_query.update({"click_count": 0})
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/")
def delete_url(url_to_delete: schemas.UrlDelete,
                current_user: str = Depends(oauth2.get_current_user),
                db: Session = Depends(get_db)):
    
    url_query = db.query(models.Url).filter(models.Url.short==url_to_delete.short)
    url = url_query.first()

    if url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Url {url_to_delete.short} was not found")
    
    if url.user_id is not current_user.id:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You're not the owner of this url")
    
    url_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)