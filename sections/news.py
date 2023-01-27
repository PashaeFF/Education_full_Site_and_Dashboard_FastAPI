from fastapi import APIRouter, Request, Depends, UploadFile
from typing import Optional
from PIL import Image
from sqlalchemy.orm import Session
from configurations import models, database
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
import secrets, pathlib
from utils.helper import templates, check_user, default_variables
from utils import paginate


news_panel = APIRouter(
    tags=['Dashboard / News'],
)


@news_panel.get("/news")
def news(request: Request, page: int = 1, page_size: int = 10):
    check = check_user(request)
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            variables = default_variables(request)
            page_title = check['dashboard_language'].news_title
            news_all = paginate.paginate(data=variables['site_news'], data_length=len(variables['site_news']), page=page, page_size=page_size)
            return templates.TemplateResponse("dashboard/news.html",{"request":request, "response":news_all, "news_category":variables['news_category'],
                                                "counts":variables['counts'], "unread":variables['unread'], "count":len(variables['users']), "messages_time": variables['messages_time'], "user":check['user'],
                                                "flash":variables['_flash_message'], "page_title":page_title, "language":check['dashboard_language'],
                                                "dashboard_languages":check['dashboard_languages']})
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@news_panel.post("/add_news")
async def create_news(request: Request, db:Session = Depends(database.get_db),file: Optional[UploadFile] = None):
    check = check_user(request)
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            FILEPATH = "static/news_images/"
            form = await request.form()
            news_title = form.get("news_title")
            description = form.get("description")
            news_file = form.get("file")
            select_category_id = form.get("select_category_id")
            request.session["flash_messsage"] = []
            if news_file is None:
                pass
            else:
                filename = file.filename
                if len(filename) > 0:
                    extension = filename.split(".")[1]
                    if extension not in ["png","jpg","jpeg"]:
                        request.session["flash_messsage"].append({"message": check['dashboard_language'].image_extension_error, "category": "error"})
                        request = RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
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
                        new_news = models.SiteNews(news_title=news_title,description=description,select_category_id=select_category_id, news_image=token_name)
                else:
                    new_news = models.SiteNews(news_title=news_title,description=description,select_category_id=select_category_id)
            check_name = db.query(models.SiteNews).filter_by(news_title=news_title).first()
            if check_name:
                if news_title == check_name.news_title:
                    request.session["flash_messsage"].append({"message": check['dashboard_language'].conflict_error, "category": "error"})
                    request = RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
                    return request
            else:
                if len(news_title) == 0 and len(description) == 0:
                    request.session["flash_messsage"].append({"message": check['dashboard_language'].news_title_or_description_empty, "category": "error"})
                    request = RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
                    return request
                db.add(new_news)
                db.commit()
                db.refresh(new_news)
                request.session["flash_messsage"].append({"message": f"'{news_title}' {check['dashboard_language'].added_to_the_news}", "category": "success"})
                request = RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@news_panel.post("/add_news_category")
async def add_news_category(request: Request, db:Session = Depends(database.get_db)):
    check = check_user(request)
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            request.session["flash_messsage"] = []
            form = await request.form()
            category_name = form.get("category_name")
            check_name = db.query(models.NewsCategory).filter_by(name=category_name).first()
            if check_name:
                if category_name == check_name.name:
                    request.session["flash_messsage"].append({"message": check['dashboard_language'].conflict_error, "category": "error"})
                    request = RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
                    return request
            else:
                if len(category_name) == 0:
                    request.session["flash_messsage"].append({"message": check['dashboard_language'].name_cannot_be_empty, "category": "error"})
                    request = RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
                    return request
                new_news_category = models.NewsCategory(name=category_name)
                db.add(new_news_category)
                db.commit()
                db.refresh(new_news_category)
                request.session["flash_messsage"].append({"message": f"'{category_name}' {check['dashboard_language'].added_to_categories}", "category": "success"})
                request = RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
                return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
   

@news_panel.get("/news/{id}")
def get_update_news(id:int, request: Request, db:Session = Depends(database.get_db)):
    check = check_user(request)
    news = db.query(models.SiteNews).filter_by(id=id).first()
    request.session["flash_messsage"] = []
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            if news:
                variables = default_variables(request)
                page_title = check['dashboard_language'].news_title
                return templates.TemplateResponse("dashboard/get_update_news.html",{"request":request, "unread":variables['unread'], "messages_time": variables['messages_time'],
                                                    "counts":variables['counts'], "news_category":variables['news_category'], "news":news, "count":len(variables['users']), "user":check['user'],
                                                    "flash":variables['_flash_message'],"page_title":page_title, "language":check['dashboard_language'],
                                                    "dashboard_languages":check['dashboard_languages']})
            else:
                request.session["flash_messsage"].append({"message": check['dashboard_language'].does_not_exist, "category": "error"})
                request = RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@news_panel.post("/news/{id}")
async def post_update_news(id:int, request: Request, db:Session = Depends(database.get_db),file: Optional[UploadFile] = None):
    check = check_user(request)
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            changed_news = db.query(models.SiteNews).filter_by(id=id)
            #kohne shekil adi
            old_image = changed_news.first().news_image
            FILEPATH = "static/news_images/"
            form = await request.form()
            news_title = form.get("news_title")
            description = form.get("description")
            news_file = form.get("file")
            select_category_id = form.get("select_category_id")
            request.session["flash_messsage"] = []

            if news_file is None:
                pass
            if file:
                filename = file.filename
                if len(filename) > 0:
                    extension = filename.split(".")[1]
                    if extension not in ["png","jpg","jpeg"]:
                        request.session["flash_messsage"].append({"message": check['dashboard_language'].image_extension_error, "category": "error"})
                        request = RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
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
                        #kohne shekli silmek
                        if old_image:
                            old = pathlib.Path(FILEPATH+old_image)
                            old.unlink()
                        changed_news.update({"news_title":news_title,"description":description,"select_category_id":select_category_id, "news_image":token_name})
                        db.commit()
            changed_news.update({"news_title":news_title,"description":description,"select_category_id":select_category_id})
            db.commit()
            request.session["flash_messsage"].append({"message": check['dashboard_language'].updated, "category": "success"})
            request = RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
            return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@news_panel.get("/news/{id}/delete")
def delete_education(id:int, request: Request, db:Session = Depends(database.get_db)):
    check = check_user(request)
    delete_option = db.query(models.SiteNews).filter_by(id=id)
    request.session["flash_messsage"] = []
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            if delete_option.first():
                FILEPATH = "static/news_images/"
                name = delete_option.first().news_title
                news_image = delete_option.first().news_image
                delete_option.delete()
                db.commit()
                if news_image:
                    delete_image = pathlib.Path(FILEPATH+news_image)
                    delete_image.unlink()
                request.session["flash_messsage"].append({"message": f"{name} {check['dashboard_language'].deleted}", "category": "success"})
                request = RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
                return request
            else:
                request.session["flash_messsage"].append({"message": check['dashboard_language'].does_not_exist, "category": "error"})
                request = RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@news_panel.get("/newscategory/{id}/delete")
def delete_news_categoryy(id:int, request: Request, db:Session = Depends(database.get_db)):
    check = check_user(request)
    request.session["flash_messsage"] = []
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            delete_option = db.query(models.NewsCategory).filter_by(id=id)
            name = delete_option.first().name
            same_category = db.query(models.SiteNews).filter_by(select_category_id=id)
            same_category.delete()
            delete_option.delete()
            db.commit()
            request.session["flash_messsage"].append({"message": f"{name} {check['dashboard_language'].deleted}", "category": "success"})
            request = RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
            return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/admin/login", status_code=HTTP_303_SEE_OTHER)