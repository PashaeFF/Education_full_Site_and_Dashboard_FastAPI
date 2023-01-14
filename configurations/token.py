from datetime import timedelta, datetime
from jose import JWTError, jwt, ExpiredSignatureError

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
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
        