from fastapi import APIRouter, Request, Depends, UploadFile
from typing import Optional
from PIL import Image
from sqlalchemy.orm import Session
from configurations import models, database
import secrets, pathlib
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from utils.helper import templates, check_user, default_variables
from utils import paginate


education_panel = APIRouter(
    tags=['Dashboard / Education Panel'],
)


###########     educations     ###########
@education_panel.get("/educations")
def educations(request: Request, page: int = 1, page_size: int = 10):
    check = check_user(request)
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            variables = default_variables(request)
            page_title = check['dashboard_language'].educations_title
            response = paginate.paginate(data=variables['education'], data_length=len(variables['education']),page=page, page_size=page_size)
            return templates.TemplateResponse("dashboard/educations.html",{"request":request, "response":response, "unread":variables['unread'], "users":variables['users'],
                                                "education_category":variables['education_category'], "counts":variables['counts'], "count":len(variables['users']), 
                                                "messages_time": variables['messages_time'], "user":check['user'], "flash":variables['_flash_message'], 'page_title':page_title,
                                                "language":check['dashboard_language'], "dashboard_languages":check['dashboard_languages']})
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/admin/login", status_code=HTTP_303_SEE_OTHER)


@education_panel.post("/education/add/education")
async def create_educations(request: Request, db:Session = Depends(database.get_db), file: Optional[UploadFile] = None):
    check = check_user(request)
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            FILEPATH = "static/education_images/"
            form = await request.form()
            name = form.get("name")
            city = form.get("city")
            photos = form.get("file")
            about_education = form.get("about_education")
            education_type = form.get("education_type")
            request.session["flash_messsage"] = []
            if photos is None:
                pass
            else:
                filename = file.filename
                if len(filename) > 0:
                    extension = filename.split(".")[1]
                    if extension not in ["png","jpg","jpeg"]:
                        request.session["flash_messsage"].append({"message": check['dashboard_language'].image_extension_error, "category": "error"})
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
            check_name = db.query(models.Education).filter_by(name=name).first()
            if check_name:
                if name == check_name.name:
                    request.session["flash_messsage"].append({"message": check['dashboard_language'].conflict_error, "category": "error"})
                    request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                    return request
            else: 
                if len(name) == 0 and len(about_education) == 0 and len(city) == 0:
                    request.session["flash_messsage"].append({"message": check['dashboard_language'].required_boxes_error, "category": "error"})
                    request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                    return request
                db.add(new_education)
                db.commit()
                db.refresh(new_education)
                request.session["flash_messsage"].append({"message": f"'{name}' {check['dashboard_language'].was_added}", "category": "success"})
                request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/admin/login", status_code=HTTP_303_SEE_OTHER)


@education_panel.post("/education/add/category")
async def add_education_category(request: Request, db:Session = Depends(database.get_db)):
    check = check_user(request)
    request.session["flash_messsage"] = []
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            form = await request.form()
            edu_name = form.get("edu_name")
            check_name = db.query(models.EduCategory).filter_by(name=edu_name).first()
            if check_name:
                if edu_name == check_name.name:
                    request.session["flash_messsage"].append({"message": check['dashboard_language'].conflict_error, "category": "error"})
                    request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                    return request
            else:
                if len(edu_name) == 0:
                    request.session["flash_messsage"].append({"message": check['dashboard_language'].name_cannot_be_empty, "category": "error"})
                    request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                    return request
                new_edu_category = models.EduCategory(name=edu_name)
                db.add(new_edu_category)
                db.commit()
                db.refresh(new_edu_category)
                request.session["flash_messsage"].append({"message": f"'{edu_name}' {check['dashboard_language'].was_added}", "category": "success"})
                request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/admin/login", status_code=HTTP_303_SEE_OTHER)


@education_panel.get("/educations/{id}")
def get_education(id:int, request: Request, db:Session = Depends(database.get_db), page: int = 1, page_size: int = 10):
    check = check_user(request)
    edu = db.query(models.Education).filter_by(id=id).first()
    request.session["flash_messsage"] = []
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            if edu:
                variables = default_variables(request)
                user_in_edu = db.query(models.User).filter_by(select_university_id = id).all()
                edu_users = paginate.paginate(data=user_in_edu, data_length=len(user_in_edu), page=page, page_size=page_size)
                page_title = check['dashboard_language'].educations_title
                return templates.TemplateResponse("dashboard/get_education.html",{"request":request, "unread":variables['unread'], "user":check['user'], "response":edu_users, "edu_id":id,
                                                    "counts":variables['counts'], "edu":edu, "user_in_edu":user_in_edu, "count":len(variables['users']), "messages_time": variables['messages_time'],
                                                    "page_title":page_title, "language":check['dashboard_language'], "dashboard_languages":check['dashboard_languages']})
            else:
                request.session["flash_messsage"].append({"message": check['dashboard_language'].does_not_exist, "category": "error"})
                request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/admin/login", status_code=HTTP_303_SEE_OTHER)


@education_panel.get("/educations/{id}/update")
def update_education(id:int, request: Request, db:Session = Depends(database.get_db)):
    check = check_user(request)
    edu = db.query(models.Education).filter_by(id=id).first()
    request.session["flash_messsage"] = []
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            if edu:
                variables = default_variables(request)
                page_title = check['dashboard_language'].educations_title
                return templates.TemplateResponse("dashboard/update_education.html",{"request":request, "education_category":variables['education_category'], 
                                                                                    "unread":variables['unread'], "edu":edu,"counts":variables['counts'], "count":len(variables['users']),
                                                                                    "messages_time": variables['messages_time'], "user":check['user'], "page_title":page_title,
                                                                                    "language":check['dashboard_language'], "dashboard_languages":check['dashboard_languages']})
            else:
                request.session["flash_messsage"].append({"message": check['dashboard_language'].does_not_exist, "category": "error"})
                request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@education_panel.post("/educations/{id}/update")
async def update_post_education(id:int, request: Request, db:Session = Depends(database.get_db)):
    check = check_user(request)
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            edu = db.query(models.Education).filter_by(id=id)
            form = await request.form()
            name = form.get("name")
            city = form.get("city")
            about_education = form.get("about_education")
            education_type = form.get("education_type")
            request.session["flash_messsage"] = []
            check_name = db.query(models.Education).filter_by(name=name).first()
            if check_name:
                if name == check_name.name:
                    request.session["flash_messsage"].append({"message": check['dashboard_language'].conflict_error, "category": "error"})
                    request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                    return request
            else:
                if len(name) and len(about_education) and len(city) and len(education_type) == 0:
                    request.session["flash_messsage"].append({"message": check['dashboard_language'].required_boxes_error, "category": "success"})
                    request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                    return request
                else:
                    edu.update({"name":name, "about_education":about_education, "education_type":education_type, "city":city},synchronize_session=False)
                    db.commit()
                    request.session["flash_messsage"].append({"message": f"'{name}' {check['dashboard_language'].updated}", "category": "success"})
                    request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                    return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/admin/login", status_code=HTTP_303_SEE_OTHER)
        

@education_panel.get("/educations/{id}/delete")
def delete_education(id:int, request: Request, db:Session = Depends(database.get_db)):
    check = check_user(request)
    delete_option = db.query(models.Education).filter_by(id=id)
    request.session["flash_messsage"] = []
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            if delete_option.first():
                delete_option = db.query(models.Education).filter_by(id=id)
                name = delete_option.first().name
                delete_option.delete()
                db.commit()
                request.session["flash_messsage"].append({"message": f"{name} {check['dashboard_language'].deleted}", "category": "success"})
                request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                return request
            else:
                request.session["flash_messsage"].append({"message": check['dashboard_language'].does_not_exist, "category": "error"})
                request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/admin/login", status_code=HTTP_303_SEE_OTHER)

@education_panel.get("/educategory/{id}/delete")
def delete_edu_categoryy(id:int, request: Request, db:Session = Depends(database.get_db)):
    check = check_user(request)
    delete_option = db.query(models.Education).filter_by(id=id)
    request.session["flash_messsage"] = []
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            delete_option = db.query(models.EduCategory).filter_by(id=id)
            name = delete_option.first().name
            same_category = db.query(models.Education).filter_by(education_type=name)
            same_category.delete()
            delete_option.delete()
            db.commit()
            request.session["flash_messsage"].append({"message": f"{name} {check['dashboard_language'].deleted}", "category": "success"})
            request = RedirectResponse(url="/admin/educations",status_code=HTTP_303_SEE_OTHER)
            return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/admin/login", status_code=HTTP_303_SEE_OTHER)
