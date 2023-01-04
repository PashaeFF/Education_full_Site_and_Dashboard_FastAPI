from fastapi import APIRouter, Request, Depends, UploadFile, File, Form, Query
from typing import Optional
from PIL import Image
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import and_
import models, database, schemas, paginate, time_calculate
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from sqlalchemy.exc import IntegrityError
from routers import admin
import secrets, pathlib
from utils.helper import templates, flash, get_flashed_messages

news_panel = APIRouter(
    tags=['Dashboard / News'],
)

# ###########     educations     ###########
@news_panel.get("/news")
def news(request: Request, db:Session = Depends(database.get_db), page: int = 1, page_size: int = 10):
    unread = db.query(models.AdminMessages).filter_by(readed=0).all()
    users = db.query(models.User).all()
    data = db.query(models.SiteNews).all()
    news_category = db.query(models.NewsCategory).all()
    data_length = len(data)
    response = paginate.paginate(data=data, data_length=data_length,page=page, page_size=page_size)
    counts = admin.return_count()

    #mesajin gelme zamanini hesablayir
    messages_time = time_calculate.messages_time()

    return templates.TemplateResponse("dashboard/news.html",{"request":request, "response":response, "news_category":news_category,
                                        "counts":counts, "unread":unread, "count":len(users), "messages_time": messages_time})

@news_panel.post("/news")
async def create_news(request: Request, db:Session = Depends(database.get_db),file: Optional[UploadFile] = None):
    FILEPATH = "static/news_images/"
    form = await request.form()
    news_title = form.get("news_title")
    description = form.get("description")
    news_file = form.get("file")
    select_category_id = form.get("select_category_id")
    category_name = form.get("category_name")
    if news_file is None:
        pass
    else:
        filename = file.filename
        if len(filename) > 0:
            extension = filename.split(".")[1]
            if extension not in ["png","jpg","jpeg"]:
                flash(request,"PNG, JPG, JPEG icaze verilir", "error")
                return RedirectResponse(url=f"/admin/news",status_code=HTTP_303_SEE_OTHER)
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
                new_news = models.SiteNews(news_title=news_title,description=description,select_category_id=select_category_id, news_image=token_name)
        else:
            new_news = models.SiteNews(news_title=news_title,description=description,select_category_id=select_category_id)
    try:
        if category_name == None:
            db.add(new_news)
            db.commit()
            db.refresh(new_news)
        elif news_title == None:
            new_news_category = models.NewsCategory(name=category_name)
            db.add(new_news_category)
            db.commit()
            db.refresh(new_news_category)
        flash(request,"Elave olundu", "success")
        return RedirectResponse(url=f"/admin/news",status_code=HTTP_303_SEE_OTHER)
    except IntegrityError:
        flash(request,"Movcuddur", "error")
        return RedirectResponse(url=f"/admin/news",status_code=HTTP_303_SEE_OTHER)

@news_panel.get("/news/{id}")
def get_update_news(id:int, request: Request, db:Session = Depends(database.get_db)):
    unread = db.query(models.AdminMessages).filter_by(readed=0).all()
    users = db.query(models.User).all()
    news_category = db.query(models.NewsCategory).all()
    news = db.query(models.SiteNews).filter_by(id=id).first()

    #mesajin gelme zamanini hesablayir
    messages_time = time_calculate.messages_time()
        
    counts = admin.return_count()
    return templates.TemplateResponse("dashboard/get_update_news.html",{"request":request, "unread":unread, "messages_time": messages_time,
                                        "counts":counts, "news_category":news_category, "news":news, "count":len(users)})

@news_panel.post("/news/{id}")
async def post_update_news(id:int, request: Request, db:Session = Depends(database.get_db),file: Optional[UploadFile] = None):
    changed_news = db.query(models.SiteNews).filter_by(id=id)
    #kohne shekil adi
    old_image = changed_news.first().news_image
    FILEPATH = "static/news_images/"
    form = await request.form()
    news_title = form.get("news_title")
    description = form.get("description")
    news_file = form.get("file")
    print(news_file)
    select_category_id = form.get("select_category_id")
    try:
        if news_file is None:
            pass
        if file:
            filename = file.filename
            if len(filename) > 0:
                extension = filename.split(".")[1]
                if extension not in ["png","jpg","jpeg"]:
                    flash(request,"PNG, JPG, JPEG icaze verilir", "error")
                    return RedirectResponse(url=f"/admin/news",status_code=HTTP_303_SEE_OTHER)
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
                    #kohne shekli silmek
                    if old_image:
                        old = pathlib.Path(FILEPATH+old_image)
                        old.unlink()
                    changed_news.update({"news_title":news_title,"description":description,"select_category_id":select_category_id, "news_image":token_name})
                    db.commit()
        changed_news.update({"news_title":news_title,"description":description,"select_category_id":select_category_id})
        db.commit()
        flash(request,"Yenilendi", "success")
        return RedirectResponse(url=f"/admin/news",status_code=HTTP_303_SEE_OTHER)
    except IntegrityError:
        flash(request,"Bu adda movcuddur", "error")
        return RedirectResponse(url=f"/admin/news",status_code=HTTP_303_SEE_OTHER)


@news_panel.get("/news/{id}/delete")
def delete_education(id:int, request: Request, db:Session = Depends(database.get_db)):
    delete_option = db.query(models.SiteNews).filter_by(id=id)
    name = delete_option.first().news_title
    delete_option.delete()
    db.commit()
    flash(request,f'"{name}" silindi', 'success')
    return RedirectResponse(url="/admin/news",status_code=HTTP_303_SEE_OTHER)
