from fastapi import APIRouter, Request, Depends, Response
from sqlalchemy.orm import Session
from configurations import models, database
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from utils.helper import templates, check_user_in_site, site_default_variables, default_variables
from utils.hashing import Hasher
from configurations.token import create_access_token, create_reset_password_token, send_mail, verify_reset_password_token


authorization = APIRouter(
    tags=['Site / Authorization']
)

@authorization.get("/logout")
def logout(response: Response, request: Request):
    response = RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
    response.delete_cookie('access_token')
    return response


@authorization.get("/login")
async def login_page(request: Request):
    check_site_user = check_user_in_site(request)
    lang = check_user_in_site(request)['site_language']
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        if check_site_user['current_user']:
            return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
        else:
            variables = site_default_variables(request)
            page_title = check_site_user['site_settings'].site_title +" - "+check_site_user['site_language'].login_page_title
        return templates.TemplateResponse("site/route/login.html", {"request":request, "site_settings":check_site_user['site_settings'],
                                            "current_user":check_site_user['current_user'], "page_title":page_title, "categories":variables['categories'],
                                            "news_category":variables['news_category'], "user":check_site_user['user'], "flash":variables['_flash_message'],
                                            "language":lang})


@authorization.post("/login")
@authorization.post("/admin/login")
async def post_login(response: Response, request: Request, db: Session = Depends(database.get_db)):
    lang = check_user_in_site(request)['site_language']
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    user = db.query(models.User).filter_by(email=email).first()
    request.session["flash_messsage"] = []
    if user:
        if user.is_active == True:
            if Hasher.verify_password(password,user.password) == True:
                data = {
                    "sub": email,
                    "id": user.id,
                }
                request.session["flash_messsage"].append({"message": lang.user_logged_message, "category": "success"})
                response = RedirectResponse(url=request.headers['referer'], status_code=HTTP_303_SEE_OTHER)
                response.set_cookie(key="access_token", value=f"Bearer {create_access_token(data=data)}", httponly=True)
                return response
            
            else:
                request.session["flash_messsage"].append({"message": lang.wrong_password_message, "category": "error"})
                request = RedirectResponse(url=request.headers['referer'], status_code=HTTP_303_SEE_OTHER)
                return request
        request.session["flash_messsage"].append({"message": 'Deaktiv user', "category": "error"})
        request = RedirectResponse(url=request.headers['referer'], status_code=HTTP_303_SEE_OTHER)
        return request
    else:
        request.session["flash_messsage"].append({"message": lang.user_does_not_exist_message, "category": "error"})
        request = RedirectResponse(url=request.headers['referer'], status_code=HTTP_303_SEE_OTHER)
        return request
    

@authorization.get("/registration")
def registration(request: Request):
    check_site_user = check_user_in_site(request)
    lang = check_user_in_site(request)['site_language']
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        if check_site_user['current_user']:
            return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
        else:
            variables = site_default_variables(request)
            page_title = check_site_user['site_settings'].site_title +" - "+lang.registration_page_title
            return templates.TemplateResponse("site/route/register.html",{"request":request, "site_settings":check_site_user['site_settings'],
                                                "current_user":check_site_user['current_user'], "page_title":page_title, "categories":variables['categories'],
                                                "news_category":variables['news_category'], "flash":variables['_flash_message'], "user":check_site_user['user'], "language":lang})


@authorization.post("/registration")
async def post_registration(request: Request, response: Response, db:Session = Depends(database.get_db)):
    lang = check_user_in_site(request)['site_language']
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    name_surname = form.get("name_surname")
    check_email = db.query(models.User).filter_by(email=email).first()
    request.session["flash_messsage"] = []
    if "@" not in email:
        request.session["flash_messsage"].append({"message": lang.correct_email_message, "category": "error"})
        request = RedirectResponse(url="/registration",status_code=HTTP_303_SEE_OTHER)
        return request
    if len(password) < 8:
        request.session["flash_messsage"].append({"message": lang.password_minimum_8_character_message, "category": "error"})
        request = RedirectResponse(url="/registration",status_code=HTTP_303_SEE_OTHER)
        return request
    if len(name_surname) < 1:
        request.session["flash_messsage"].append({"message": lang.name_not_added_message, "category": "error"})
        request = RedirectResponse(url="/registration",status_code=HTTP_303_SEE_OTHER)
        return request
    if check_email:
        request.session["flash_messsage"].append({"message": lang.email_is_available_message, "category": "error"})
        request = RedirectResponse(url="/registration",status_code=HTTP_303_SEE_OTHER)
        return request
        
    user = models.User(email=email, password=Hasher.get_hash_password(password), name_surname=name_surname)
    db.add(user)
    db.commit()
    db.refresh(user)
    change = db.query(models.User).filter_by(email=email).first()
    data = {
            "sub": email,
            "id": user.id,
        }
    request.session["flash_messsage"].append({"message": lang.registration_success, "category": "success"})
    response = RedirectResponse(url=f"/update_profile/{change.id}", status_code=HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=f"Bearer {create_access_token(data=data)}", httponly=True)
    return response


@authorization.get("/forgot-password")
def forgot_password_page(request: Request):
    check_site_user = check_user_in_site(request)
    lang = check_user_in_site(request)['site_language']
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        if check_site_user['current_user']:
            return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
        else:
            variables = site_default_variables(request)
            page_title = check_site_user['site_settings'].site_title +" - "+ lang.forgot_password
        return templates.TemplateResponse("site/route/forgot_password.html", {"request":request, "site_settings":check_site_user['site_settings'],
                                            "current_user":check_site_user['current_user'], "page_title":page_title, "categories":variables['categories'],
                                            "news_category":variables['news_category'], "user":check_site_user['user'], "flash":variables['_flash_message'],
                                            "language":lang})


@authorization.post("/forgot-password")
async def forgot_password_check_mail_user(request: Request, db: Session = Depends(database.get_db)):
    form = await request.form()
    lang = check_user_in_site(request)['site_language']
    subject_title = check_user_in_site(request)['site_settings'].site_title
    site_url = check_user_in_site(request)['site_settings'].site_url
    check_mail = db.query(models.User).filter_by(email=form.get('email')).first()
    request.session["flash_messsage"] = []
    if check_mail:
        data = {
                "sub": check_mail.email,
                "id": check_mail.id
            }
        create_password_reset_url = site_url+f"/reset-password/{create_reset_password_token(data=data)}"
        send_mail(check_mail.email, subject_title+" - "+ lang.forgot_password, create_password_reset_url, request)
        request.session["flash_messsage"].append({"message": lang.email_sent, "category": "success"})
        request = RedirectResponse(url="/forgot-password",status_code=HTTP_303_SEE_OTHER)
        return request
    else:
        request.session["flash_messsage"].append({"message": lang.email_is_not_registere, "category": "success"})
        request = RedirectResponse(url="/forgot-password",status_code=HTTP_303_SEE_OTHER)
        return request


@authorization.get("/reset-password/{new_token}")
def check_token_for_new_password(new_token: str, request: Request, db: Session = Depends(database.get_db)):
    if type(verify_reset_password_token(new_token, request=request)) == int:
        user = db.query(models.User).filter_by(id=verify_reset_password_token(new_token, request=request)).first()
        if user:
            data = {
                "sub": user.email,
                "id": user.id,
                }
            response = RedirectResponse(url="/change-password", status_code=HTTP_303_SEE_OTHER)
            response.set_cookie(key="access_token", value=f"Bearer {create_access_token(data=data)}", httponly=True)
            return response
        else:
            return RedirectResponse("/forgot-password", HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse("/forgot-password", HTTP_303_SEE_OTHER)


@authorization.get("/change-password")
def check_token_for_new_password(request: Request):
    check_site_user = check_user_in_site(request)
    lang = check_user_in_site(request)['site_language']
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        if check_site_user['current_user']:
            variables = site_default_variables(request)
            page_title = check_site_user['site_settings'].site_title +" - "+lang.change_password
            return templates.TemplateResponse("site/route/reset-password.html", {"request":request, "site_settings":check_site_user['site_settings'],
                                                "current_user":check_site_user['current_user'], "page_title":page_title, "categories":variables['categories'],
                                                "news_category":variables['news_category'], "user":check_site_user['user'], "flash":variables['_flash_message'],
                                                "language":lang})
    else:
        return templates.TemplateResponse("site/closed.html", {"request":request})

@authorization.post("/change-password")
async def set_new_password(request: Request, db: Session = Depends(database.get_db)):
    check_site_user = check_user_in_site(request)
    lang = check_user_in_site(request)['site_language']
    request.session["flash_messsage"] = []
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        if check_site_user['current_user']:
            update_password = db.query(models.User).filter_by(id=check_site_user['current_user'])
            form = await request.form()
            password = form.get('password')
            re_password = form.get('re_password')
            if password != re_password:
                request.session["flash_messsage"].append({"message": lang.password_not_same_confirm_password, "category": "error"})
                request = RedirectResponse(url="/change-password",status_code=HTTP_303_SEE_OTHER)
                return request
            if len(password) < 8:
                request.session["flash_messsage"].append({"message": lang.password_minimum_8_character_message, "category": "error"})
                request = RedirectResponse(url="/change-password",status_code=HTTP_303_SEE_OTHER)
                return request
            update_password.update({'password':Hasher.get_hash_password(password)})
            db.commit()
            request.session["flash_messsage"].append({"message": lang.password_changed, "category": "success"})
            request = RedirectResponse(url="/",status_code=HTTP_303_SEE_OTHER)
            return request
        else:
            return RedirectResponse(url="/",status_code=HTTP_303_SEE_OTHER)
    else:
        return templates.TemplateResponse("site/closed.html", {"request":request})