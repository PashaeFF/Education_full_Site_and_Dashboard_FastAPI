from fastapi import APIRouter, Request, Depends, Response
from typing import Optional
from PIL import Image
from sqlalchemy.orm import Session
import models, database
from sqlalchemy.exc import IntegrityError
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_301_MOVED_PERMANENTLY, HTTP_401_UNAUTHORIZED
from utils.helper import templates
from utils.hashing import Hasher
from configurations.token import verify_token, create_access_token


register = APIRouter(
    tags=['Site / Register']
)

@register.get("/logout")
def logout(response: Response, request: Request):
    response = RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
    response.delete_cookie('access_token')
    return response


@register.get("/login")
async def login_page(request: Request, response:Response, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = ""
    user = ""
    if access_token:
        current_user = verify_token(access_token)
        if current_user:
            user = db.query(models.User).filter_by(id=current_user).first()
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    #######     end    ##########
    if site_settings.is_active is None:
        return templates.TemplateResponse("site/closed.html", {"request":request, "site_settings":site_settings})
    else:
        categories = db.query(models.EduCategory).all()
        news_category = db.query(models.NewsCategory).all()
        page_title = site_settings.site_title +" - İstifadəçi girişi"
        _flash_message = ""
        if request.session.get("flash_messsage"):
            _flash_message = request.session.get("flash_messsage")
            request.session.pop("flash_messsage") if "flash_messsage" in request.session else []
    return templates.TemplateResponse("site/route/login.html", {"request":request, "site_settings":site_settings, "current_user":current_user, 
                                        "page_title":page_title, "categories":categories,"news_category":news_category, "user":user,
                                        "flash":_flash_message})

@register.post("/login")
async def post_login(response: Response, request: Request, db: Session = Depends(database.get_db)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    user = db.query(models.User).filter_by(email=email).first()
    request.session["flash_messsage"] = []
    if user:
        if Hasher.verify_password(password,user.password) == True:
            data = {
                "sub": email,
                "id": user.id,
            }
            request.session["flash_messsage"].append({"message": "Daxil oldunuz", "category": "success"})
            response = RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
            response.set_cookie(key="access_token", value=f"Bearer {create_access_token(data=data)}", httponly=True)
            return response
        else:
            request.session["flash_messsage"].append({"message": "Parol Səhvdir", "category": "error"})
            request = RedirectResponse(url="/login",status_code=HTTP_303_SEE_OTHER)
            return request
    else:
        request.session["flash_messsage"].append({"message": "İstifadəçi mövcud deyil", "category": "error"})
        request = RedirectResponse(url="/login",status_code=HTTP_303_SEE_OTHER)
        return request

@register.get("/registration")
def registration(request: Request, db: Session = Depends(database.get_db)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    if access_token:
        current_user = verify_token(access_token)
    else:
        current_user = ""
        user = ""
    if current_user:
        user = db.query(models.User).filter_by(id=current_user).first()
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    #######     end    ##########
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    if site_settings.is_active is None:
        return templates.TemplateResponse("site/closed.html", {"request":request, "site_settings":site_settings})
    else:
        categories = db.query(models.EduCategory).all()
        news_category = db.query(models.NewsCategory).all()
        page_title = site_settings.site_title +" - Qeydiyyat"
        _flash_message = ""
        if request.session.get("flash_messsage"):
            _flash_message = request.session.get("flash_messsage")
            request.session.pop("flash_messsage") if "flash_messsage" in request.session else []
        return templates.TemplateResponse("site/route/register.html",{"request":request, "site_settings":site_settings, "current_user":current_user,
                                            "page_title":page_title, "categories":categories,"news_category":news_category, "flash":_flash_message})


@register.post("/registration")
async def post_registration(request: Request, response: Response, db:Session = Depends(database.get_db)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    name_surname = form.get("name_surname")
    request.session["flash_messsage"] = []
    if "@" not in email:
        request.session["flash_messsage"].append({"message": "Emaili düzgün qeyd edin", "category": "error"})
        request = RedirectResponse(url="/registration",status_code=HTTP_303_SEE_OTHER)
        return request
    if len(password) < 8:
        request.session["flash_messsage"].append({"message": "Parol minimum 8 simvol olmalıdır", "category": "error"})
        request = RedirectResponse(url="/registration",status_code=HTTP_303_SEE_OTHER)
        return request
    if len(name_surname) < 1:
        request.session["flash_messsage"].append({"message": "Ad əlavə etməmisiniz", "category": "error"})
        request = RedirectResponse(url="/registration",status_code=HTTP_303_SEE_OTHER)
        return request
    user = models.User(email=email, password=Hasher.get_hash_password(password), name_surname=name_surname)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        change = db.query(models.User).filter_by(email=email).first()
        data = {
                "sub": email,
                "id": user.id,
            }
        request.session["flash_messsage"].append({"message": "Daxil oldunuz", "category": "success"})
        response = RedirectResponse(url=f"/update_profile/{change.id}", status_code=HTTP_303_SEE_OTHER)
        response.set_cookie(key="access_token", value=f"Bearer {create_access_token(data=data)}", httponly=True)
        return response
    except IntegrityError:
        request.session["flash_messsage"].append({"message": "Email mövcuddur", "category": "error"})
        request = RedirectResponse(url="/registration",status_code=HTTP_303_SEE_OTHER)
        return request










