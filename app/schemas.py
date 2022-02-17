from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class Message(BaseModel):
    message: str

class UrlRetrieve(BaseModel):
    id: int
    long: str
    short: str
    created: datetime
    last_clicked: Optional[datetime]
    click_count: int
    user_id: Optional[int] = None

    class Config:
        orm_mode = True

class UrlCreateDefault(BaseModel):
    long: str

class UrlCreatePremium(BaseModel):
    long: str
    short: str
    user_id: Optional[int] = None

class UrlOut(BaseModel):
    short: str

    class Config:
        orm_mode = True
        
class UrlDelete(UrlOut):
    pass

class UrlUpdate(BaseModel):
    long: str
    short: str

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserLogin(UserBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created = datetime

    class Config:
        orm_mode = True
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Visit(BaseModel):
    client_host: str
    headers: str

    class Config:
        orm_mode = True