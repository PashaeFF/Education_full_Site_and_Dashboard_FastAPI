from fastapi import APIRouter, Request, UploadFile, Depends, File
from typing import Optional
from PIL import Image
from sqlalchemy.orm import Session
import models, database, secrets, pathlib
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from utils.helper import templates, closed, flash, get_flashed_messages
from passlib.context import CryptContext
from utils.hashing import Hasher

user = APIRouter(
    tags=['Site / User']
)


@user.get("/update_profile/{id}")
def update_profile(id: int, request: Request, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    if site_settings:
        if site_settings.is_active is None:
            return closed()
        else:
            user = db.query(models.User).filter_by(id=id).first()
            edu = db.query(models.Education).all()
            categories = db.query(models.EduCategory).all()
            news_category = db.query(models.NewsCategory).all()
            page_title = site_settings.site_title +" - Profil məlumatları"
            return templates.TemplateResponse("site/route/update_profile.html", {"request":request, "user":user, "edu":edu, "categories":categories,
                                                                                "news_category":news_category, "page_title":page_title, "site_settings":site_settings})

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
    if profile_picture:
        filename = file.filename
        if len(filename) > 0:
            extension = filename.split(".")[1]
            if extension not in ["png","jpg","jpeg"]:
                flash(request,"PNG, JPG, JPEG icaze verilir", "error")
                return RedirectResponse(url=f"/update_profile/{id}",status_code=HTTP_303_SEE_OTHER)
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
                flash(request,"Profil tamamlandı", "success")
                return RedirectResponse("/",status_code=HTTP_303_SEE_OTHER)
    user.update({'name_surname':name_surname, 'age':age, 'city':city, 'phone':phone, 'education':education, 'certificate_points':certificate_points,
                'about':about, 'select_university_id':select_university_id},synchronize_session=False)
    db.commit()
    flash(request,"Profil tamamlandı", "success")
    return RedirectResponse("/",status_code=HTTP_303_SEE_OTHER)