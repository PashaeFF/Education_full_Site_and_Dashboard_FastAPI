from fastapi import APIRouter, Request, Depends, UploadFile
from typing import Optional
from PIL import Image
from sqlalchemy.orm import Session
from sqlalchemy import and_
import models, database, time_calculate
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from routers import admin
import secrets, pathlib
from utils.helper import templates
from configurations.token import verify_token

staff_panel = APIRouter(
    tags=['Dashboard / Staff'],
)

@staff_panel.get('/staff')
def staff(request: Request, db: Session = Depends(database.get_db)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    if user:
        if user.admin_user == True or user.super_user == True:
            unread = db.query(models.AdminMessages).filter_by(readed=0).all()
            users = db.query(models.User).all()
            counts = admin.return_count()
            staff = db.query(models.Staff).all()
            #mesajin gelme zamanini hesablayir
            messages_time = time_calculate.messages_time()
            ########## flash message
            _flash_message = ""
            if request.session.get("flash_messsage"):
                _flash_message = request.session.get("flash_messsage")
                request.session.pop("flash_messsage") if "flash_messsage" in request.session else []
            return templates.TemplateResponse("dashboard/staff.html",{"request":request,"staff":staff, "messages_time": messages_time,
                                                "unread":unread, "counts":counts, "count":len(users), "user":user, "flash":_flash_message})
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

@staff_panel.post("/staff")
async def create_staff(request: Request, db:Session = Depends(database.get_db),file: Optional[UploadFile] = None):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    if user:
        if user.admin_user == True or user.super_user == True:
            FILEPATH = "static/staff_images/"
            form = await request.form()
            name_surname = form.get("name_surname")
            job_position = form.get("job_position")
            photo = form.get("file")
            facebook = form.get("facebook")
            instagram = form.get("instagram")
            twitter = form.get("twitter")
            linkedin = form.get("linkedin")
            behance = form.get("behance")
            filename = file.filename
            request.session["flash_messsage"] = []
            if len(filename) and len(name_surname) and len(job_position) > 0:
                extension = filename.split(".")[1]
                if extension not in ["png","jpg","jpeg"]:
                    request.session["flash_messsage"].append({"message": "Yalnız JPG, PNG, JPEG", "category": "error"})
                    request = RedirectResponse(url=f"/admin/staff",status_code=HTTP_303_SEE_OTHER)
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
                    new_staff = models.Staff(name_surname=name_surname,job_position=job_position, photo=token_name, facebook=facebook,
                                            instagram=instagram, twitter=twitter, linkedin=linkedin, behance=behance)
                db.add(new_staff)
                db.commit()
                db.refresh(new_staff)
                request.session["flash_messsage"].append({"message": "Əlavə olundu", "category": "success"})
                request = RedirectResponse(url=f"/admin/staff",status_code=HTTP_303_SEE_OTHER)
                return request
            else:
                request.session["flash_messsage"].append({"message": "Ulduzlu sahələri mütləq doldurmalısınız..", "category": "error"})
                request = RedirectResponse(url=f"/admin/staff",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

@staff_panel.get("/staff/{id}/delete")
def delete_staff(id:int, request: Request, db:Session = Depends(database.get_db)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    if user:
        if user.admin_user == True or user.super_user == True:
            FILEPATH = "static/staff_images/"
            delete_option = db.query(models.Staff).filter_by(id=id)
            image = delete_option.first().photo
            name = delete_option.first().name_surname
            delete_option.delete()
            db.commit()
            if image:
                old = pathlib.Path(FILEPATH+image)
                old.unlink()
            request.session["flash_messsage"] = []
            request.session["flash_messsage"].append({"message": "Əlavə olundu", "category": "success"})
            request = RedirectResponse(url=f"/admin/staff",status_code=HTTP_303_SEE_OTHER)
            return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

