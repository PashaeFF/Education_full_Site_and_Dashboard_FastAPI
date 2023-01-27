from fastapi import APIRouter, Request, Depends, Response
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from sqlalchemy.orm import Session
from configurations import models, database
from starlette.status import HTTP_303_SEE_OTHER, HTTP_201_CREATED
from utils.helper import templates
from utils.hashing import Hasher
from configurations.token import create_access_token
from sections import default_site_language, default_dashboard_language
from sections.languages import dashboard_english, dashboard_russian, english, russian

installer = APIRouter(
    prefix= ("/install")
)


@installer.get("/")
def select_language(request: Request, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    if site_settings:
        return RedirectResponse("/")
    else:
        languages = db.query(models.DashboardLanguages).all()
        if languages:
            return RedirectResponse("/install/2", HTTP_303_SEE_OTHER)
        return templates.TemplateResponse("select_language.html", {"request":request})


@installer.post("/")
async def select_language_post(request: Request, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    if site_settings:
        return RedirectResponse("/")
    else:
        form = await request.form()
        if form.get('set_dashboard_language') == "1":
            default_dashboard_language.set_azerbaijan_language()
            return RedirectResponse("/install/2", HTTP_303_SEE_OTHER)
        elif form.get('set_dashboard_language') == "2":
            dashboard_english.set_english()
            return RedirectResponse("/install/2", HTTP_303_SEE_OTHER)
        elif form.get('set_dashboard_language') == "3":
            dashboard_russian.set_russian()
            return RedirectResponse("/install/2", HTTP_303_SEE_OTHER)
        else:
            return RedirectResponse("/install", HTTP_303_SEE_OTHER)



@installer.get("/2")
def installer_page(request: Request, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    languages = [default_site_language.lang_name[0], russian.lang_name[0], english.lang_name[0]]
    dashboard_language = db.query(models.DashboardLanguages).filter_by(id=1).first()
    if site_settings:
        return RedirectResponse("/")
    else:
        _flash_message = ""
        if request.session.get("flash_messsage"):
            _flash_message = request.session.get("flash_messsage")
            request.session.pop("flash_messsage") if "flash_messsage" in request.session else []
        return templates.TemplateResponse("installation_page.html", {"request":request, "flash":_flash_message, "languages":languages,
                                                                    "dashboard_language":dashboard_language})


@installer.post("/2")
async def post_installer_page(request: Request, response: Response, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    dashboard_language = db.query(models.DashboardLanguages).filter_by(id=1).first()
    if site_settings:
        return RedirectResponse("/")
    else:
        form = await request.form()
        email = form.get("email")
        password = form.get("password")
        name_surname = form.get("name_surname")
        site_url = form.get("site_url")
        site_title = form.get("site_title")
        site_logo = form.get("site_logo")
        site_slogan = form.get("site_slogan")
        set_site_language = form.get("set_site_language")
        request.session["flash_messsage"] = []
        if "@" not in email:
            request.session["flash_messsage"].append({"message": dashboard_language.correct_email_message, "category": "error"})
            request = RedirectResponse(url="/install/2",status_code=HTTP_303_SEE_OTHER)
            return request
        if len(password) < 8:
            request.session["flash_messsage"].append({"message": dashboard_language.password_minimum_8_character_message, "category": "error"})
            response = RedirectResponse(url="/install/2",status_code=HTTP_303_SEE_OTHER)
            return response
        if len(name_surname) < 1 and len(site_url) < 1 and len(site_title) < 1 and len(site_logo) < 1 and len(site_slogan) < 1:
            request.session["flash_messsage"].append({"message": dashboard_language.boxes_are_cannot_empty, "category": "error"})
            response = RedirectResponse(url="/install/2",status_code=HTTP_303_SEE_OTHER)
            return response
        user = models.User(
            email=email,
            password=Hasher.get_hash_password(password),
            name_surname=name_surname,
            super_user=True
            )
        site = models.SiteSettings(
            site_url=site_url,
            site_title=site_title,
            site_logo=site_logo,
            site_slogan=site_slogan
            )
        langs_all = db.query(models.DashboardLanguages).all()
        if set_site_language == '1':
            default_site_language.set_default_language()
        elif set_site_language == '2':
            russian.set_russian_language()
        elif set_site_language == '3':
            english.set_english_language()
            
        else:
            request.session["flash_messsage"].append({"message": dashboard_language.there_is_no_such_option, "category": "error"})
            response = RedirectResponse(url="/install/2",status_code=HTTP_303_SEE_OTHER)
            return response
        for i in langs_all:
            if i.dashboard_language_name != 'Azərbaycan dili':
                default_dashboard_language.set_azerbaijan_language()
            if i.dashboard_language_name != 'English':
                dashboard_english.set_english()
            if i.dashboard_language_name != 'Русский':
                dashboard_russian.set_russian()

        db.add(user)
        db.add(site)
    
        db.commit()
        db.refresh(user)
        db.refresh(site)

        data = {
                "sub": email,
                "id": user.id,
            }
        request.session["flash_messsage"].append({"message": dashboard_language.the_site_is_ready_for_use, "category": "success"})
        response = RedirectResponse(url=f"/admin",status_code=HTTP_303_SEE_OTHER)
        response.set_cookie(key="access_token", value=f"Bearer {create_access_token(data=data)}", httponly=True)
        return response