from datetime import timedelta, datetime
from jose import JWTError, jwt, ExpiredSignatureError
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str):
    try:
        if token:
            payload = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=ALGORITHM)
            return payload["id"]
        else:
            return ""
    except JWTError as err:
        if ExpiredSignatureError:
            print("Tokenin Vaxti bitib...")
        else:
            print(err)
        