from fastapi import APIRouter, Request, UploadFile, Depends, File
from typing import Optional
from PIL import Image
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import schemas, models, database, secrets, pathlib
from sqlalchemy.exc import IntegrityError
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from utils.helper import templates, closed, flash, get_flashed_messages
from passlib.context import CryptContext
from utils.hashing import Hasher

register = APIRouter(
    tags=['Site / Register']
)

@register.get("/login")
def login_page(request: Request, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    if site_settings:
        if site_settings.is_active is None:
            return closed()
        else:
            categories = db.query(models.EduCategory).all()
            news_category = db.query(models.NewsCategory).all()
            page_title = site_settings.site_title +" - İstifadəçi girişi"
    return templates.TemplateResponse("site/route/login.html", {"request":request, "site_settings":site_settings,
                                                "page_title":page_title, "categories":categories,"news_category":news_category})

@register.post("/login")
async def post_login(request: Request, db: Session = Depends(database.get_db)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    user = db.query(models.User).filter_by(email=email).first()
    if user:
        if Hasher.verify_password(password,user.password) == True:
            flash(request,"Daxil oldunuz", "success")
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
        else:
            flash(request,"Yanlish parol", "error")
            return RedirectResponse(url="/login", status_code=HTTP_303_SEE_OTHER)
    else:
        flash(request,"Beleistifadechi yoxdu", "error")
        return RedirectResponse(url="/login", status_code=HTTP_303_SEE_OTHER)


@register.get("/registration")
def registration(request: Request, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    if site_settings:
        if site_settings.is_active is None:
            return closed()
        else:
            categories = db.query(models.EduCategory).all()
            news_category = db.query(models.NewsCategory).all()
            page_title = site_settings.site_title +" - Qeydiyyat"
    return templates.TemplateResponse("site/route/register.html",{"request":request, "site_settings":site_settings,
                                                "page_title":page_title, "categories":categories,"news_category":news_category})

@register.post("/registration")
async def post_registration(request: Request, db:Session = Depends(database.get_db)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    if "@" not in email:
        flash(request,"Emaili düzgün qeyd edin", "error")
        return RedirectResponse(url="/registration",status_code=HTTP_303_SEE_OTHER)
    if len(password) < 8:
        flash(request,"Parol 8 simvol", "error")
        return RedirectResponse(url="/registration",status_code=HTTP_303_SEE_OTHER)
    user = models.User(email=email, password=Hasher.get_hash_password(password))
    print("userrr: ",user.email, user.password)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        change = db.query(models.User).filter_by(email=email).first()
        return RedirectResponse(url=f"/update_profile/{change.id}",status_code=HTTP_303_SEE_OTHER)
    except IntegrityError:
        flash(request,"Emaili mövcuddur", "error")
        return RedirectResponse(url="/registration",status_code=HTTP_303_SEE_OTHER)










