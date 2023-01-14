from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
import models, database, time_calculate
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from routers import admin
from fastapi import APIRouter, Request, Depends, UploadFile, File
from PIL import Image
import secrets, pathlib, time
from utils.helper import templates
from configurations.token import verify_token

slider_panel = APIRouter(
    tags=['Dashboard / Sliders'],
)

########### Site slider settings ###########

@slider_panel.get('/slider')
def site_slider_settings(request: Request, db:Session = Depends(database.get_db)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    if user:
        if user.admin_user == True or user.super_user == True:
            unread = db.query(models.AdminMessages).filter_by(readed=0).all()
            sliders = db.query(models.SliderSettings).all()
            users = db.query(models.User).all()
            counts = admin.return_count()
            #mesajin gelme zamanini hesablayir
            messages_time = time_calculate.messages_time()
            ########## flash message
            _flash_message = ""
            if request.session.get("flash_messsage"):
                _flash_message = request.session.get("flash_messsage")
                request.session.pop("flash_messsage") if "flash_messsage" in request.session else []
            return templates.TemplateResponse("dashboard/slider.html", {"request":request, "sliders":sliders, "count": len(users), "flash":_flash_message,
                                                                        "unread":unread, "counts":counts, "messages_time": messages_time, "user":user})
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

@slider_panel.post('/slider')
async def post_slider_settings(request: Request, db:Session = Depends(database.get_db),
                                file: UploadFile = File(...), file2: UploadFile = File(...)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    if user:
        if user.admin_user == True or user.super_user == True:
            FILEPATH = "static/site/images/slider/"
            FILEPATH_2 = "static/site/images/slider/news_photo/"
            form = await request.form()
            title = form.get("title")
            description = form.get("description")
            filename = file.filename
            filename2 = file2.filename
            request.session["flash_messsage"] = []
            if len(filename) < 1:
                request.session["flash_messsage"].append({"message": "Slide Yüklənməyib", "category": "error"})
                request = RedirectResponse(url=f"/admin/slider",status_code=HTTP_303_SEE_OTHER)
                return request
            if len(filename2) < 1:
                request.session["flash_messsage"].append({"message": "Şəkil yüklənməyib", "category": "error"})
                request = RedirectResponse(url=f"/admin/slider",status_code=HTTP_303_SEE_OTHER)
                return request
            extension = filename.split(".")[1]
            extension2 = filename2.split(".")[1]
            if extension and extension not in ["png","jpg","jpeg"]:
                request.session["flash_messsage"].append({"message": "Yalnız JPG, PNG, JPEG", "category": "error"})
                request = RedirectResponse(url=f"/admin/slider",status_code=HTTP_303_SEE_OTHER)
                return request
            if extension and extension2 not in ["png","jpg","jpeg"]:
                request.session["flash_messsage"].append({"message": "Yalnız JPG, PNG, JPEG", "category": "error"})
                request = RedirectResponse(url=f"/admin/slider",status_code=HTTP_303_SEE_OTHER)
                return request
            else:
                slide_image_name = secrets.token_hex(12)+"."+extension
                news_image_name = secrets.token_hex(12)+"."+extension
                generated_name_slide_image = FILEPATH + slide_image_name
                generated_name_news_image = FILEPATH_2 + news_image_name
                file_content = await file.read()
                file_content_2 = await file2.read()
                with open(generated_name_slide_image, "wb") as file:
                    file.write(file_content)
                with open(generated_name_news_image, "wb") as file2:
                    file2.write(file_content_2)
                img = Image.open(generated_name_slide_image)
                img_2 = Image.open(generated_name_news_image)
                img.save(generated_name_slide_image)
                time.sleep(0.5)
                img_2.save(generated_name_news_image)
                file.close()
                time.sleep(0.5)
                file2.close()
                new_slide = models.SliderSettings(title=title,description=description,photos=slide_image_name, news_photo=news_image_name)
                db.add(new_slide)
                db.commit()
                db.refresh(new_slide)
                request.session["flash_messsage"].append({"message": "Slide Yükləndi", "category": "success"})
                request = RedirectResponse(url=f"/admin/slider",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

@slider_panel.post('/slider/{id}')
async def post_update_slider_settings(id: int, request: Request, db:Session = Depends(database.get_db),
                                        file: UploadFile = File(None), file2: UploadFile = File(None)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    if user:
        if user.admin_user == True or user.super_user == True:
            update_slide = db.query(models.SliderSettings).filter_by(id=id)
            old_slide_image = update_slide.first().photos
            old_news_image = update_slide.first().news_photo
            FILEPATH = "static/site/images/slider/"
            FILEPATH_2 = "static/site/images/slider/news_photo/"
            form = await request.form()
            title = form.get("title")
            description = form.get("description")
            errors = []
            #files
            filename = file.filename
            filename2 = file2.filename
            request.session["flash_messsage"] = []
            if len(filename) != 0:
                extension = filename.split(".")[1]
                if extension not in ["png","jpg","jpeg"]:
                    request.session["flash_messsage"].append({"message": "Yalnız JPG, PNG, JPEG", "category": "error"})
                    request = RedirectResponse(url=f"/admin/slider",status_code=HTTP_303_SEE_OTHER)
                    return request
                else:
                    slide_image_name = secrets.token_hex(12)+"."+extension
                    generated_name_slide_image = FILEPATH + slide_image_name
                    file_content = await file.read()
                    with open(generated_name_slide_image, "wb") as file:
                        file.write(file_content)
                    img = Image.open(generated_name_slide_image)
                    img.save(generated_name_slide_image)
                    file.close()
                    old = pathlib.Path(FILEPATH+old_slide_image)
                    old.unlink()
            else:
                slide_image_name = update_slide.first().photos
            if len(filename2) != 0:
                extension2 = filename2.split(".")[1]
                if extension2 not in ["png","jpg","jpeg"]:
                    request.session["flash_messsage"].append({"message": "Yalnız JPG, PNG, JPEG", "category": "error"})
                    request = RedirectResponse(url=f"/admin/slider",status_code=HTTP_303_SEE_OTHER)
                    return request
                else:
                    news_image_name = secrets.token_hex(12)+"."+extension2
                    generated_name_news_image = FILEPATH_2 + news_image_name
                    file_content_2 = await file2.read()
                    with open(generated_name_news_image, "wb") as file2:
                        file2.write(file_content_2)
                    img_2 = Image.open(generated_name_news_image)
                    img_2.save(generated_name_news_image)
                    file2.close()
                    old = pathlib.Path(FILEPATH_2+old_news_image)
                    old.unlink()
            else:
                news_image_name = update_slide.first().news_photo
            update_slide.update({"title":title, "description":description, "photos": slide_image_name, "news_photo":news_image_name})
            db.commit()
            request.session["flash_messsage"].append({"message": "Updated", "category": "success"})
            request = RedirectResponse(url=f"/admin/slider",status_code=HTTP_303_SEE_OTHER)
            return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

@slider_panel.get("/slider/{id}/delete")
def delete_slide(id:int, request: Request, db:Session = Depends(database.get_db)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    if user:
        if user.admin_user == True or user.super_user == True:
            FILEPATH = "static/site/images/slider/"
            FILEPATH_2 = "static/site/images/slider/news_photo/"
            delete_option = db.query(models.SliderSettings).filter_by(id=id)
            slide_image = delete_option.first().photos
            news_image = delete_option.first().news_photo
            delete_slide = pathlib.Path(FILEPATH+slide_image)
            delete_image = pathlib.Path(FILEPATH_2+news_image)
            delete_slide.unlink()
            delete_image.unlink()
            delete_option.delete()
            db.commit()
            request.session["flash_messsage"] = []
            request.session["flash_messsage"].append({"message": "Silindi", "category": "success"})
            request = RedirectResponse(url=f"/admin/slider",status_code=HTTP_303_SEE_OTHER)
            return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

        