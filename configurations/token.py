from datetime import timedelta, datetime
from starlette.responses import RedirectResponse
from fastapi import Request
from starlette.status import HTTP_303_SEE_OTHER
from jose import JWTError, jwt, ExpiredSignatureError
from email.message import EmailMessage
import os, smtplib
from dotenv import load_dotenv
from utils import helper

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
MAIL_SENDER = os.getenv("MAIL_SENDER")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_SERVER = os.getenv("MAIL_SERVER")

####################################################
##############        SEND MAIL       ##############
####################################################
def send_mail(email, subject_title, url, request: Request):
    language = helper.check_user_in_site(request)['site_language']
    msg = EmailMessage()
    msg['Subject'] = subject_title
    msg['From'] = MAIL_SENDER
    msg['To'] = email
    msg.set_content(f"""{language.visit_the_link_reset_password}:\n
    {url}""")

    with smtplib.SMTP_SSL(MAIL_SERVER, 465) as smtp:
        smtp.login(MAIL_SENDER, MAIL_PASSWORD)
        smtp.send_message(msg)
####################################################
##############     END SEND MAIL      ##############
####################################################

####################################################
##############     RESET PASSWORD     ##############
####################################################
def create_reset_password_token(data:dict):
    expire = datetime.utcnow() + timedelta(minutes=1)
    data.update({"exp":expire})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_reset_password_token(token:str,request: Request):
    request.session["flash_messsage"] = []
    language = helper.check_user_in_site(request)['site_language']
    try:
        if token:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            return payload["id"]
    except JWTError as err:
        if ExpiredSignatureError:
            request.session["flash_messsage"].append({"message": f"{language.link_timed_out}", "category": "error"})
            return RedirectResponse(url="/forgot-password",status_code=HTTP_303_SEE_OTHER)
        else:
            print(err)
                                   
####################################################
##############   END RESET PASSWORD  ###############
####################################################

####################################################
###############         AUTH         ###############
####################################################
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
####################################################
###############       END AUTH       ###############
####################################################
        