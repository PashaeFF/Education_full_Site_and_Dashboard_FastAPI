from fastapi import APIRouter, Request, Depends, UploadFile, File
from typing import Optional
from PIL import Image
from sqlalchemy.orm import Session
from sqlalchemy import and_
import models, database, paginate, time_calculate, secrets
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from sqlalchemy.exc import IntegrityError
from routers import admin
from utils.helper import templates, flash, get_flashed_messages

education_panel = APIRouter(
    tags=['Dashboard / Education Panel'],
)

###########     educations     ###########
@education_panel.get("/educations")
def educations(request: Request, db:Session = Depends(database.get_db), page: int = 1, page_size: int = 10):
    unread = db.query(models.AdminMessages).filter_by(readed=0).all()
    users = db.query(models.User).all()
    education = db.query(models.Education).all()
    education_category = db.query(models.EduCategory).all()
    data_length = len(education)
    response = paginate.paginate(data=education, data_length=data_length,page=page, page_size=page_size)
    
    #mesajin gelme zamanini hesablayir
    messages_time = time_calculate.messages_time()

    counts = admin.return_count()
    return templates.TemplateResponse("dashboard/educations.html",{"request":request, "response":response, "unread":unread, 
                                        "education_category":education_category, "counts":counts, "count":len(users), "messages_time": messages_time})

@education_panel.post("/educations")
async def create_educations(request: Request, db:Session = Depends(database.get_db),file: Optional[UploadFile] = File(None)):
    FILEPATH = "static/education_images/"
    form = await request.form()
    name = form.get("name")
    city = form.get("city")
    photos = form.get("file")
    about_education = form.get("about_education")
    education_type = form.get("education_type")
    edu_name = form.get("edu_name")
    
    if photos is None:
        pass
    else:
        filename = file.filename
        if len(filename) > 0:
            extension = filename.split(".")[1]
            if extension not in ["png","jpg","jpeg"]:
                flash(request,'PNG, JPG, JPEG ola biler', 'error')
                return RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
            else:
                token_name = secrets.token_hex(12)+"."+extension
                print(token_name)
                generated_name = FILEPATH + token_name
                file_content = await file.read()
                with open(generated_name, "wb") as file:
                    file.write(file_content)
                img = Image.open(generated_name)
                img.save(generated_name)
                file.close()
                new_education = models.Education(name=name,education_type=education_type,about_education=about_education, photos=token_name, city=city)
        else:
            new_education = models.Education(name=name,education_type=education_type,about_education=about_education)
    try:
        if edu_name == None:
            db.add(new_education)
            db.commit()
            db.refresh(new_education)
        elif name == None:
            new_edu_category = models.EduCategory(name=edu_name)
            db.add(new_edu_category)
            db.commit()
            db.refresh(new_edu_category)
        flash(request,f'"{name}" elave olundu', 'success')
        return RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
    except IntegrityError:
        flash(request,f'"{name}" artiq movcuddur...', 'error')
        return RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)

@education_panel.get("/educations/{id}")
def get_education(id:int, request: Request, db:Session = Depends(database.get_db)):
    unread = db.query(models.AdminMessages).filter_by(readed=0).all()
    users = db.query(models.User).all()
    user_in_edu = db.query(models.User).filter_by(select_university_id = id).all()
    edu = db.query(models.Education).filter_by(id=id).first()

    #mesajin gelme zamanini hesablayir
    messages_time = time_calculate.messages_time()

    counts = admin.return_count()
    return templates.TemplateResponse("dashboard/get_education.html",{"request":request, "unread":unread,
                                        "counts":counts, "edu":edu, "user_in_edu":user_in_edu, "count":len(users), "messages_time": messages_time})

@education_panel.get("/educations/{id}/update")
def update_education(id:int, request: Request, db:Session = Depends(database.get_db)):
    unread = db.query(models.AdminMessages).filter_by(readed=0).all()
    users = db.query(models.User).all()
    edu = db.query(models.Education).filter_by(id=id).first()
    education_category = db.query(models.EduCategory).all()

    #mesajin gelme zamanini hesablayir
    messages_time = time_calculate.messages_time()

    counts = admin.return_count()
    return templates.TemplateResponse("dashboard/update_education.html",{"request":request, "education_category":education_category, 
                                                                        "unread":unread, "edu":edu,"counts":counts, "count":len(users),
                                                                        "messages_time": messages_time})

@education_panel.post("/educations/{id}/update")
async def update_post_education(id:int, request: Request, db:Session = Depends(database.get_db)):
    edu = db.query(models.Education).filter_by(id=id)
    form = await request.form()
    name = form.get("name")
    city = form.get("city")
    about_education = form.get("about_education")
    education_type = form.get("education_type")
    try:
        if name == edu.first().name:
            edu.update({"about_education":about_education, "education_type":education_type, "city":city},synchronize_session=False)
            db.commit()
            flash(request,f'"{name}" yenilendi', 'success')
            return RedirectResponse(url=f"/admin/educations",status_code=HTTP_303_SEE_OTHER)
        edu.update({"name":name, "about_education":about_education, "education_type":education_type, "city":city},synchronize_session=False)
        db.commit()
        flash(request,f'"{name}" yenilendi', 'success')
        return RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
    except IntegrityError:
        flash(request,f'"{name}" movcuddur', 'error')
        return RedirectResponse(url=f"/admin/educations/{id}/update",status_code=HTTP_303_SEE_OTHER)

@education_panel.get("/educations/{id}/delete")
def delete_education(id:int, request: Request, db:Session = Depends(database.get_db)):
    delete_option = db.query(models.Education).filter_by(id=id)
    name = delete_option.first().name
    delete_option.delete()
    db.commit()
    flash(request,f'"{name}" silindi', 'success')
    return RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
