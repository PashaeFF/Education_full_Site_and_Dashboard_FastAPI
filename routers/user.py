from fastapi import APIRouter, Request, UploadFile, Depends, File
from typing import Optional
from PIL import Image
from sqlalchemy.orm import Session
import models, database, secrets, pathlib
from configurations.token import verify_token
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from utils.helper import templates


user = APIRouter(
    tags=['Site / User']
)

@user.get("/profile/{id}")
def update_profile(id: int, request: Request, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    if access_token:
        current_user = verify_token(access_token)
        user = db.query(models.User).filter_by(id=current_user).first()
    else:
        current_user = ""
        user = ""
    #######     end    ##########
    if site_settings.is_active is None:
        return templates.TemplateResponse("site/closed.html", {"request":request, "site_settings":site_settings})
    else:
        if user:
            if id == user.id or user.admin_user == True or user.super_user == True:
                edu = db.query(models.Education).all()
                categories = db.query(models.EduCategory).all()
                news_category = db.query(models.NewsCategory).all()
                profile = db.query(models.User).filter_by(id=id).first()
                if profile.name_surname:
                    page_title = profile.name_surname +" - Profil məlumatları"
                else:
                    page_title = "Profil məlumatları"
                return templates.TemplateResponse("site/route/profile.html", {"request":request, "user":user, "edu":edu, "categories":categories,
                                                                            "current_user":current_user, "profile":profile, "news_category":news_category,
                                                                            "page_title":page_title, "site_settings":site_settings})
            else:
                return RedirectResponse("/",status_code=HTTP_303_SEE_OTHER)
        else:
                return RedirectResponse("/",status_code=HTTP_303_SEE_OTHER)


@user.get("/update_profile/{id}")
def update_profile(id: int, request: Request, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    if access_token:
        current_user = verify_token(access_token)
        user = db.query(models.User).filter_by(id=current_user).first()
        check_id = db.query(models.User).filter_by(id=id).first()
    else:
        current_user = ""
        user = ""
        check_id = ""
    #######     end    ##########
    if site_settings.is_active is None:
        return templates.TemplateResponse("site/closed.html", {"request":request, "site_settings":site_settings})
    else:
        ########## flash message
        _flash_message = ""
        if request.session.get("flash_messsage"):
            _flash_message = request.session.get("flash_messsage")
            request.session.pop("flash_messsage") if "flash_messsage" in request.session else []
        if user:
            if id == user.id or user.admin_user == True or user.super_user == True:
                edu = db.query(models.Education).all()
                categories = db.query(models.EduCategory).all()
                news_category = db.query(models.NewsCategory).all()
                page_title = site_settings.site_title +" - Profil məlumatları"
                return templates.TemplateResponse("site/route/update_profile.html", {"request":request, "user":user, "edu":edu, "categories":categories, "current_user":current_user,
                                                                                    "news_category":news_category, "page_title":page_title, "site_settings":site_settings,
                                                                                    "flash":_flash_message,"check_id":check_id})
            else:
                return RedirectResponse("/",status_code=HTTP_303_SEE_OTHER)
        if check_id:
            edu = db.query(models.Education).all()
            categories = db.query(models.EduCategory).all()
            news_category = db.query(models.NewsCategory).all()
            page_title = site_settings.site_title +" - Profil məlumatları"
            return templates.TemplateResponse("site/route/update_profile.html", {"request":request, "user":user, "edu":edu, "categories":categories, "current_user":current_user,
                                                                                "news_category":news_category, "page_title":page_title, "site_settings":site_settings,
                                                                                "flash":_flash_message,"check_id":check_id})
        else:
                return RedirectResponse("/",status_code=HTTP_303_SEE_OTHER)


@user.post("/update_profile/{id}")
async def post_update_profile(id:int, request: Request, db:Session = Depends(database.get_db), file: UploadFile = File(...)):
    user = db.query(models.User).filter_by(id=id)
    FILEPATH = "static/profile_pictures/"
    old_profile_picture = user.first().profile_picture
    form = await request.form()
    name_surname = form.get("name_surname")
    phone = form.get("phone")
    age = form.get("age")
    city = form.get("city")
    education = form.get("education")
    certificate_points = form.get("certificate_points")
    about = form.get("about")
    select_university_id = form.get("select_university_id")
    profile_picture = form.get("file")
    request.session["flash_messsage"] = []
    if profile_picture:
        filename = file.filename
        if len(filename) > 0:
            extension = filename.split(".")[1]
            if extension not in ["png","jpg","jpeg"]:
                request.session["flash_messsage"].append({"message": "Yalnız JPG, PNG, JPEG", "category": "error"})
                request = RedirectResponse(url=f"/update_profile/{id}",status_code=HTTP_303_SEE_OTHER)
                return request
            else:
                token_name = secrets.token_hex(12)+"."+extension
                generated_name = FILEPATH + token_name
                file_content = await file.read()
                with open(generated_name, "wb") as file:
                    file.write(file_content)
                img = Image.open(generated_name)
                img.save(generated_name)
                file.close()
                if old_profile_picture:
                    old = pathlib.Path(FILEPATH+old_profile_picture)
                    try:
                        old.unlink()
                    except:
                        pass
                user.update({'name_surname':name_surname, 'age':age, 'city':city, 'profile_picture':token_name, 'phone':phone, 'education':education,
                            'certificate_points':certificate_points, 'about':about, 'select_university_id':select_university_id},synchronize_session=False)
                db.commit()
                request.session["flash_messsage"].append({"message": "Profil tamamlandı", "category": "success"})
                request = RedirectResponse(url=f"/",status_code=HTTP_303_SEE_OTHER)
                return request
    user.update({'name_surname':name_surname, 'age':age, 'city':city, 'phone':phone, 'education':education, 'certificate_points':certificate_points,
                'about':about, 'select_university_id':select_university_id},synchronize_session=False)
    db.commit()
    request.session["flash_messsage"].append({"message": "Profil tamamlandı", "category": "success"})
    request = RedirectResponse(url=f"/",status_code=HTTP_303_SEE_OTHER)
    return request