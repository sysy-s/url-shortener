from passlib.context import CryptContext
import string
import random


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str): 
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def rand_str_gen(length: int):
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(length)])
