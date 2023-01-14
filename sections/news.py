from fastapi import APIRouter, Request, Depends, UploadFile
from typing import Optional
from PIL import Image
from sqlalchemy.orm import Session
from sqlalchemy import and_
import models, database, schemas, paginate, time_calculate
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from sqlalchemy.exc import IntegrityError
from routers import admin
import secrets, pathlib
from utils.helper import templates
from configurations.token import verify_token

news_panel = APIRouter(
    tags=['Dashboard / News'],
)

@news_panel.get("/news")
def news(request: Request, db:Session = Depends(database.get_db), page: int = 1, page_size: int = 10):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    if user:
        if user.admin_user == True or user.super_user == True:
            unread = db.query(models.AdminMessages).filter_by(readed=0).all()
            users = db.query(models.User).all()
            data = db.query(models.SiteNews).all()
            news_category = db.query(models.NewsCategory).all()
            data_length = len(data)
            news_all = paginate.paginate(data=data, data_length=data_length,page=page, page_size=page_size)
            counts = admin.return_count()
            #mesajin gelme zamanini hesablayir
            messages_time = time_calculate.messages_time()
            ########## flash message
            _flash_message = ""
            if request.session.get("flash_messsage"):
                _flash_message = request.session.get("flash_messsage")
                request.session.pop("flash_messsage") if "flash_messsage" in request.session else []
            return templates.TemplateResponse("dashboard/news.html",{"request":request, "response":news_all, "news_category":news_category,
                                                "counts":counts, "unread":unread, "count":len(users), "messages_time": messages_time, "user":user,
                                                "flash":_flash_message})
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@news_panel.post("/news/add/{id}")
async def create_news(id:str, request: Request, db:Session = Depends(database.get_db),file: Optional[UploadFile] = None):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    if user:
        if user.admin_user == True or user.super_user == True:
            FILEPATH = "static/news_images/"
            form = await request.form()
            news_title = form.get("news_title")
            description = form.get("description")
            news_file = form.get("file")
            select_category_id = form.get("select_category_id")
            category_name = form.get("category_name")
            request.session["flash_messsage"] = []
            if news_file is None:
                pass
            else:
                filename = file.filename
                if len(filename) > 0:
                    extension = filename.split(".")[1]
                    if extension not in ["png","jpg","jpeg"]:
                        request.session["flash_messsage"].append({"message": "Yalnız JPG, PNG, JPEG", "category": "error"})
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
            try:
                if id == "add-news":
                    if len(news_title) and len(description) == 0:
                        request.session["flash_messsage"].append({"message": "Xəbər adı və Description boş ola bilməz...", "category": "error"})
                        request = RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
                        return request
                    db.add(new_news)
                    db.commit()
                    db.refresh(new_news)
                    request.session["flash_messsage"].append({"message": f"'{news_title}' adlı xəbər əlavə olundu", "category": "success"})
                elif id == "add-category":
                    if len(category_name) == 0:
                        request.session["flash_messsage"].append({"message": "Ad boş ola bilməz...", "category": "error"})
                        request = RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
                        return request
                    new_news_category = models.NewsCategory(name=category_name)
                    db.add(new_news_category)
                    db.commit()
                    db.refresh(new_news_category)
                    request.session["flash_messsage"].append({"message": f"'{category_name}' adlı kateqoriya əlavə olundu", "category": "success"})
                else:
                    request.session["flash_messsage"].append({"message": f"Belə funksiya yoxdur...", "category": "error"})
                request = RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
                return request
            except IntegrityError:
                request.session["flash_messsage"].append({"message": "Ad mövcuddur", "category": "error"})
                request = RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
        

@news_panel.get("/news/{id}")
def get_update_news(id:int, request: Request, db:Session = Depends(database.get_db)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    news = db.query(models.SiteNews).filter_by(id=id).first()
    request.session["flash_messsage"] = []
    if user:
        if user.admin_user == True or user.super_user == True:
            if news:
                unread = db.query(models.AdminMessages).filter_by(readed=0).all()
                users = db.query(models.User).all()
                news_category = db.query(models.NewsCategory).all()
                #mesajin gelme zamanini hesablayir
                messages_time = time_calculate.messages_time()
                counts = admin.return_count()
                ########## flash message
                _flash_message = ""
                if request.session.get("flash_messsage"):
                    _flash_message = request.session.get("flash_messsage")
                    request.session.pop("flash_messsage") if "flash_messsage" in request.session else []
                return templates.TemplateResponse("dashboard/get_update_news.html",{"request":request, "unread":unread, "messages_time": messages_time,
                                                    "counts":counts, "news_category":news_category, "news":news, "count":len(users), "user":user,
                                                    "flash":_flash_message})
            else:
                request.session["flash_messsage"].append({"message": "Mövcud deyil", "category": "error"})
                request = RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@news_panel.post("/news/{id}")
async def post_update_news(id:int, request: Request, db:Session = Depends(database.get_db),file: Optional[UploadFile] = None):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    if user:
        if user.admin_user == True or user.super_user == True:
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
            try:
                if news_file is None:
                    pass
                if file:
                    filename = file.filename
                    if len(filename) > 0:
                        extension = filename.split(".")[1]
                        if extension not in ["png","jpg","jpeg"]:
                            request.session["flash_messsage"].append({"message": "Yalnız JPG, PNG, JPEG", "category": "error"})
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
                request.session["flash_messsage"].append({"message": "Updated", "category": "success"})
                request = RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
                return request
            except IntegrityError:
                request.session["flash_messsage"].append({"message": f"{news_title} Ad mövcuddur", "category": "error"})
                request = RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@news_panel.get("/news/{id}/delete")
def delete_education(id:int, request: Request, db:Session = Depends(database.get_db)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    delete_option = db.query(models.SiteNews).filter_by(id=id)
    request.session["flash_messsage"] = []
    if user:
        if user.admin_user == True or user.super_user == True:
            if delete_option.first():
                FILEPATH = "static/news_images/"
                name = delete_option.first().news_title
                news_image = delete_option.first().news_image
                delete_option.delete()
                db.commit()
                if news_image:
                    delete_image = pathlib.Path(FILEPATH+news_image)
                    delete_image.unlink()
                request.session["flash_messsage"].append({"message": f"{name} silindi", "category": "success"})
                request = RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
                return request
            else:
                request.session["flash_messsage"].append({"message": "Mövcud deyil", "category": "error"})
                request = RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)