from fastapi import APIRouter, Request, UploadFile, Depends, File
from PIL import Image
import os
from typing import List
from sqlalchemy.orm import Session
from configurations import models, database
import secrets, pathlib
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from utils.helper import templates, check_user_in_site, site_default_variables


user_panel = APIRouter(
    tags=['Site / User']
)

@user_panel.get("/profile/{id}")
def update_profile(id: int, request: Request, db: Session = Depends(database.get_db)):
    check_site_user = check_user_in_site(request)
    lang = check_user_in_site(request)['site_language']
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        else:
            if check_site_user['user']:
                if id == check_site_user['user'].id or check_site_user['user'].admin_user == True or check_site_user['user'].super_user == True:
                    edu = db.query(models.Education).all()
                    categories = db.query(models.EduCategory).all()
                    news_category = db.query(models.NewsCategory).all()
                    profile = db.query(models.User).filter_by(id=id).first()
                    variables = site_default_variables(request)
                    if profile:
                        page_title = profile.name_surname +" - "+lang.user_profile_info_page_title
                        if profile.education_files:
                            user_education_files = profile.education_files.split(',')
                        else:
                            user_education_files = ""
                    else:
                        return RedirectResponse("/",status_code=HTTP_303_SEE_OTHER)
                    return templates.TemplateResponse("site/route/profile.html", {"request":request, "user":check_site_user['user'], "edu":edu, "categories":categories,
                                                                                "current_user":check_site_user['current_user'], "profile":profile, "news_category":news_category,
                                                                                "page_title":page_title, "site_settings":check_site_user['site_settings'],"language":lang,
                                                                                "user_education_files":user_education_files, "flash":variables['_flash_message']})
                else:
                    return RedirectResponse("/",status_code=HTTP_303_SEE_OTHER)
            else:
                return RedirectResponse("/",status_code=HTTP_303_SEE_OTHER)


@user_panel.get("/user/{id}/upload")
def user_upload(id: int, request: Request, db: Session = Depends(database.get_db)):
    check_site_user = check_user_in_site(request)
    lang = check_user_in_site(request)['site_language']
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        else:
            if check_site_user['user']:
                if id == check_site_user['user'].id or check_site_user['user'].admin_user == True or check_site_user['user'].super_user == True:
                    edu = db.query(models.Education).all()
                    categories = db.query(models.EduCategory).all()
                    news_category = db.query(models.NewsCategory).all()
                    profile = db.query(models.User).filter_by(id=id).first()
                    variables = site_default_variables(request)
                    if profile:
                        page_title = profile.name_surname +" - "+lang.file_upload
                        if profile.education_files:
                            return RedirectResponse("/",status_code=HTTP_303_SEE_OTHER)
                    else:
                        return RedirectResponse("/",status_code=HTTP_303_SEE_OTHER)
                    return templates.TemplateResponse("site/route/upload_files.html", {"request":request, "user":check_site_user['user'], "edu":edu, "categories":categories,
                                                                                "current_user":check_site_user['current_user'], "profile":profile, "news_category":news_category,
                                                                                "page_title":page_title, "site_settings":check_site_user['site_settings'],"language":lang,
                                                                                "flash":variables['_flash_message']})
                else:
                    return RedirectResponse("/",status_code=HTTP_303_SEE_OTHER)
            else:
                return RedirectResponse("/",status_code=HTTP_303_SEE_OTHER)


@user_panel.post("/user/{id}/upload")
async def user_upload_file(id: int, request: Request, db: Session = Depends(database.get_db), files: List[UploadFile] = File(...)):
    check_site_user = check_user_in_site(request)
    lang = check_user_in_site(request)['site_language']
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        else:
            request.session["flash_messsage"] = []
            if check_site_user['user']:
                user = db.query(models.User).filter_by(id=check_site_user['current_user'])
                if id == check_site_user['user'].id:
                    if len(files) > 4:
                        request.session["flash_messsage"].append({"message": lang.max_4_file, "category": "error"})
                        request = RedirectResponse(url=f"/user/{user.first().id}/upload",status_code=HTTP_303_SEE_OTHER)
                        return request
                    directory = check_site_user['user'].id
                    FILEPATH = f"static/user_files/{directory}/"
                    if not os.path.exists(FILEPATH):
                        os.makedirs(FILEPATH)
                    user_files = ''
                    if files:
                        for file in files:
                            filename = file.filename
                            extension = filename.split(".")[1]
                            if extension not in ["png","jpg","jpeg"]:
                                request.session["flash_messsage"].append({"message": lang.image_extension_error_message, "category": "error"})
                                request = RedirectResponse(url=f"/user/{id}/upload",status_code=HTTP_303_SEE_OTHER)
                                return request
                            else:
                                token_name = secrets.token_hex(12)+"."+extension
                                generated_name = FILEPATH + token_name
                                file_content = await file.read()
                                with open(generated_name, "wb") as file:
                                    file.write(file_content)
                                img = Image.open(generated_name)
                                img.save(generated_name)
                                user_files += token_name+","
                                file.close()
                        user.update({'education_files':user_files[:-1]},synchronize_session=False)
                        db.commit()
                        request.session["flash_messsage"].append({"message": lang.files_uploaded, "category": "success"})
                        request = RedirectResponse(url=f"/profile/{id}",status_code=HTTP_303_SEE_OTHER)
                        return request


@user_panel.get("/update_profile/{id}")
def update_profile(id: int, request: Request, db: Session = Depends(database.get_db)):
    check_site_user = check_user_in_site(request)
    lang = check_user_in_site(request)['site_language']
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        else:
            variables = site_default_variables(request)
            if check_site_user['user']:
                if id == check_site_user['user'].id or check_site_user['user'].admin_user == True or check_site_user['user'].super_user == True:
                    check_id = db.query(models.User).filter_by(id=id).first()
                    page_title = check_id.name_surname +" - "+lang.user_profile_info_page_title
                    return templates.TemplateResponse("site/route/update_profile.html", {"request":request, "user":check_site_user['user'], "edu":variables['educations'], "categories":variables['categories'], "current_user":check_site_user['current_user'],
                                                                                        "news_category":variables['news_category'], "page_title":page_title, "site_settings":check_site_user['site_settings'],
                                                                                        "flash":variables['_flash_message'], "check_id":check_id,"language":lang})
                else:
                    return RedirectResponse("/",status_code=HTTP_303_SEE_OTHER)
            if  check_site_user['current_user']:
                check_id = db.query(models.User).filter_by(id=id).first()
                page_title = check_id.name_surname +" - "+lang.profile_info
                return templates.TemplateResponse("site/route/update_profile.html", {"request":request, "user":check_site_user['user'], "edu":variables['educations'], "categories":variables['categories'], "current_user":check_site_user['current_user'],
                                                                                    "news_category":variables['news_category'], "page_title":page_title, "site_settings":check_site_user['site_settings'],
                                                                                    "flash":variables['_flash_message'], "check_id":check_id,"language":lang})
            else:
                return RedirectResponse("/",status_code=HTTP_303_SEE_OTHER)


@user_panel.post("/update_profile/{id}")
async def post_update_profile(id:int, request: Request, db:Session = Depends(database.get_db), file: UploadFile = File(...)):
    check_site_user = check_user_in_site(request)
    lang = check_user_in_site(request)['site_language']
    if check_site_user['user']:
        if id == check_site_user['user'].id or check_site_user['user'].admin_user == True or check_site_user['user'].super_user == True:
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
                        request.session["flash_messsage"].append({"message": lang.image_extension_error_message, "category": "error"})
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
                        request.session["flash_messsage"].append({"message": lang.profile_success_message, "category": "success"})
                        request = RedirectResponse(url=f"/",status_code=HTTP_303_SEE_OTHER)
                        return request
            user.update({'name_surname':name_surname, 'age':age, 'city':city, 'phone':phone, 'education':education, 'certificate_points':certificate_points,
                        'about':about, 'select_university_id':select_university_id},synchronize_session=False)
            db.commit()
            request.session["flash_messsage"].append({"message": lang.profile_success_message, "category": "success"})
            request = RedirectResponse(url=f"/",status_code=HTTP_303_SEE_OTHER)
            return request


@user_panel.post("/files/{id}/delete")
def delete_user_files(id:int, request: Request, db:Session = Depends(database.get_db)):
    check_site_user = check_user_in_site(request)
    lang = check_user_in_site(request)['site_language']
    if check_site_user['user']:
        profile = db.query(models.User).filter_by(id=id)
        user_education_files = profile.first().education_files.split(',')
        FILEPATH = f"static/user_files/{profile.first().id}/"
        request.session["flash_messsage"] = []
        if id == check_site_user['user'].id or check_site_user['user'].admin_user == True or check_site_user['user'].super_user == True: 
            profile.update({"education_files":""})
            db.commit()
            if len(user_education_files) > 0:
                for image in user_education_files:
                    delete_image = pathlib.Path(FILEPATH+image)
                    delete_image.unlink()
            request.session["flash_messsage"].append({"message": lang.deleted, "category": "success"})
            request = RedirectResponse(url=f"/profile/{profile.first().id}",status_code=HTTP_303_SEE_OTHER)
            return request