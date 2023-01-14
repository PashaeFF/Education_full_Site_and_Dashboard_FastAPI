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
from configurations.token import verify_token
from utils.helper import templates

education_panel = APIRouter(
    tags=['Dashboard / Education Panel'],
)

###########     educations     ###########
@education_panel.get("/educations")
def educations(request: Request, db:Session = Depends(database.get_db), page: int = 1, page_size: int = 10):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    if user:
        if user.admin_user == True or user.super_user == True:
            unread = db.query(models.AdminMessages).filter_by(readed=0).all()
            users = db.query(models.User).all()
            education = db.query(models.Education).all()
            education_category = db.query(models.EduCategory).all()
            data_length = len(education)
            response = paginate.paginate(data=education, data_length=data_length,page=page, page_size=page_size)
            counts = admin.return_count()
            #mesajin gelme zamanini hesablayir
            messages_time = time_calculate.messages_time()
            ########## flash message
            _flash_message = ""
            if request.session.get("flash_messsage"):
                _flash_message = request.session.get("flash_messsage")
                request.session.pop("flash_messsage") if "flash_messsage" in request.session else []
            return templates.TemplateResponse("dashboard/educations.html",{"request":request, "response":response, "unread":unread, "users":users,
                                                "education_category":education_category, "counts":counts, "count":len(users), "messages_time": messages_time,
                                                "user":user, "flash":_flash_message})
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@education_panel.post("/educations/add/{id}")
async def create_educations(id:str, request: Request, db:Session = Depends(database.get_db),file: Optional[UploadFile] = File(None)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    if user:
        if user.admin_user == True or user.super_user == True:
            FILEPATH = "static/education_images/"
            form = await request.form()
            name = form.get("name")
            city = form.get("city")
            photos = form.get("file")
            about_education = form.get("about_education")
            education_type = form.get("education_type")
            edu_name = form.get("edu_name")
            request.session["flash_messsage"] = []
            if photos is None:
                pass
            else:
                filename = file.filename
                if len(filename) > 0:
                    extension = filename.split(".")[1]
                    if extension not in ["png","jpg","jpeg"]:
                        request.session["flash_messsage"].append({"message": "Yalnız JPG, PNG, JPEG", "category": "error"})
                        request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
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
                        new_education = models.Education(name=name,education_type=education_type,about_education=about_education, photos=token_name, city=city)
                else:
                    new_education = models.Education(name=name,education_type=education_type,about_education=about_education)
            try:
                if id == "add-education":
                    if len(name) and len(about_education) and len(city) == 0:
                        request.session["flash_messsage"].append({"message": "Ulduzlu sahələri mütləq doldurmalısınız...", "category": "error"})
                        request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                        return request
                    db.add(new_education)
                    db.commit()
                    db.refresh(new_education)
                    request.session["flash_messsage"].append({"message": f"'{name}' əlavə olundu", "category": "success"})
                elif id == "add-category":
                    if len(edu_name) == 0:
                        request.session["flash_messsage"].append({"message": "Ad boş ola bilməz...", "category": "error"})
                        request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                        return request
                    new_edu_category = models.EduCategory(name=edu_name)
                    db.add(new_edu_category)
                    db.commit()
                    db.refresh(new_edu_category)
                    request.session["flash_messsage"].append({"message": f"'{name}' əlavə olundu", "category": "success"})
                else:
                    request.session["flash_messsage"].append({"message": f"Belə funksiya yoxdur...", "category": "error"})
                request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                return request
            except IntegrityError:
                request.session["flash_messsage"].append({"message": f"'{name}' mövcuddur", "category": "error"})
                request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@education_panel.get("/educations/{id}")
def get_education(id:int, request: Request, db:Session = Depends(database.get_db), page: int = 1, page_size: int = 10):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    edu = db.query(models.Education).filter_by(id=id).first()
    request.session["flash_messsage"] = []
    if user:
        if user.admin_user == True or user.super_user == True:
            if edu:
                unread = db.query(models.AdminMessages).filter_by(readed=0).all()
                users = db.query(models.User).all()
                user_in_edu = db.query(models.User).filter_by(select_university_id = id).all()
                data_length = len(user_in_edu)
                edu_users = paginate.paginate(data=user_in_edu, data_length=data_length,page=page, page_size=page_size)
                #mesajin gelme zamanini hesablayir
                messages_time = time_calculate.messages_time()
                counts = admin.return_count()
                return templates.TemplateResponse("dashboard/get_education.html",{"request":request, "unread":unread, "user":user, "response":edu_users,
                                                    "counts":counts, "edu":edu, "user_in_edu":user_in_edu, "count":len(users), "messages_time": messages_time})
            else:
                request.session["flash_messsage"].append({"message": "Mövcud deyil...", "category": "error"})
                request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@education_panel.get("/educations/{id}/update")
def update_education(id:int, request: Request, db:Session = Depends(database.get_db)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    edu = db.query(models.Education).filter_by(id=id).first()
    request.session["flash_messsage"] = []
    if user:
        if user.admin_user == True or user.super_user == True:
            if edu:
                unread = db.query(models.AdminMessages).filter_by(readed=0).all()
                users = db.query(models.User).all()
                education_category = db.query(models.EduCategory).all()
                #mesajin gelme zamanini hesablayir
                messages_time = time_calculate.messages_time()
                counts = admin.return_count()
                return templates.TemplateResponse("dashboard/update_education.html",{"request":request, "education_category":education_category, 
                                                                                    "unread":unread, "edu":edu,"counts":counts, "count":len(users),
                                                                                    "messages_time": messages_time, "user":user})
            else:
                request.session["flash_messsage"].append({"message": f"Mövcud deyil...", "category": "error"})
                request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@education_panel.post("/educations/{id}/update")
async def update_post_education(id:int, request: Request, db:Session = Depends(database.get_db)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    if user:
        if user.admin_user == True or user.super_user == True:
            edu = db.query(models.Education).filter_by(id=id)
            form = await request.form()
            name = form.get("name")
            city = form.get("city")
            about_education = form.get("about_education")
            education_type = form.get("education_type")
            request.session["flash_messsage"] = []
            try:
                if len(name) and len(about_education) and len(city) and len(education_type) == 0:
                    request.session["flash_messsage"].append({"message": f"Ulduzlu sahələr boş ola bilməz...", "category": "success"})
                    request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                    return request
                else:
                    edu.update({"name":name, "about_education":about_education, "education_type":education_type, "city":city},synchronize_session=False)
                    db.commit()
                    request.session["flash_messsage"].append({"message": f"'{name}' update olundu", "category": "success"})
                    request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                    return request
            except IntegrityError:
                request.session["flash_messsage"].append({"message": f"'{name}' movcuddur", "category": "error"})
                request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
        

@education_panel.get("/educations/{id}/delete")
def delete_education(id:int, request: Request, db:Session = Depends(database.get_db)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    delete_option = db.query(models.Education).filter_by(id=id)
    request.session["flash_messsage"] = []
    if user:
        if user.admin_user == True or user.super_user == True:
            if delete_option.first():
                delete_option = db.query(models.Education).filter_by(id=id)
                name = delete_option.first().name
                delete_option.delete()
                db.commit()
                request.session["flash_messsage"].append({"message": f"{name} silindi", "category": "success"})
                request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                return request
            else:
                request.session["flash_messsage"].append({"message": "Mövcud deyil", "category": "error"})
                request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
