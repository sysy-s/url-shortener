from fastapi import status, HTTPException, Depends, APIRouter, Request
import sqlalchemy
import validators
from fastapi.responses import RedirectResponse
import time
from sqlalchemy.orm import Session
import requests

from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    tags=['Urls']
)


@router.post("/", response_model=schemas.UrlOut, status_code=status.HTTP_201_CREATED, responses={409: {"model": schemas.Message}})
def post_long_url(
        url: schemas.UrlCreateDefault,
        db: Session = Depends(get_db)):
    """
    Takes in long url and gives back it's short version, also validates if url is valid, and if
    the short one doesn't collide with others in th database.
    """

    url_dict = url.dict()

    if not validators.url(url_dict['long']):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='Invalid url')

    while True:
        url_dict['short'] = utils.rand_str_gen(6)
        new_url = models.Url(**url_dict)
        db.add(new_url)
        try:
            db.commit()
            break
        except Exception as error:
            print(error)
            time.sleep(0.1)

    db.refresh(new_url)
    return new_url


@router.post("/premium",
             response_model=schemas.UrlOut,
             status_code=status.HTTP_201_CREATED,
             responses={409: {"model": schemas.Message}})
def create_short_url_premium(
        url: schemas.UrlCreatePremium,
        current_user: str = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db)):
    """
    Takes in long url and gives back it's ***customized*** short version, also validates if url is valid, and if
    the short one doesn't collide with others in th database.
    """

    url_dict = url.dict()
    url_dict['user_id'] = current_user.id
    if not validators.url(url_dict['long']) or not url_dict['short'].isalnum():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='Invalid URL')

    while True:
        new_url = models.Url(**url_dict)
        db.add(new_url)
        try:
            db.commit()
            break
        except:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail='URL already taken')

    db.refresh(new_url)
    return new_url


@router.get("/{short}")
def redirect_short_url(request: Request, short: str, db: Session = Depends(get_db)):
    """
    Redirects user to long url via db matching, if url given doesn't exist returns exception.
    Adds one to click count and get request headers and stores them in the visits table.
    """

    url_query = db.query(models.Url).filter(models.Url.short == short)
    url = url_query.first()

    if url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Url {short} was not found")

    url_query.update({"click_count": url.click_count+1,
                     "last_clicked": sqlalchemy.func.now()}, synchronize_session=False)
    db.commit()

    session = requests.Session()
    session.get(url.long)

    # Creates new visit log, and stores request data in db, also updates click count for url
    client_host = str(request.client.host)
    request_headers = str(request.headers)

    visit_dict = {"url_id": url.id, "client_host": client_host,
                  "headers": request_headers, "cookies": str(session.cookies.get_dict())}
    new_visit = models.Visit(**visit_dict)
    db.add(new_visit)
    db.commit()

    return RedirectResponse(url.long, status_code=status.HTTP_302_FOUND)
