from fastapi import APIRouter, Request, Depends, UploadFile, File, Form, Query
from typing import Optional
from PIL import Image
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import and_
import models, database, schemas, paginate, time_calculate
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from routers import admin
import secrets, pathlib
from utils.helper import templates, flash, get_flashed_messages

staff_panel = APIRouter(
    tags=['Dashboard / Staff'],
)

@staff_panel.get('/staff')
def staff(request: Request, db: Session = Depends(database.get_db)):
    unread = db.query(models.AdminMessages).filter_by(readed=0).all()
    users = db.query(models.User).all()
    counts = admin.return_count()
    staff = db.query(models.Staff).all()

    #mesajin gelme zamanini hesablayir
    messages_time = time_calculate.messages_time()

    return templates.TemplateResponse("dashboard/staff.html",{"request":request,"staff":staff, "messages_time": messages_time,
                                        "unread":unread, "counts":counts, "count":len(users)})

@staff_panel.post("/staff")
async def create_staff(request: Request, db:Session = Depends(database.get_db),file: Optional[UploadFile] = None):
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
    if len(filename) > 0:
        extension = filename.split(".")[1]
        if extension not in ["png","jpg","jpeg"]:
            flash(request,"PNG, JPG, JPEG icaze verilir", "error")
            return RedirectResponse(url=f"/admin/staff",status_code=HTTP_303_SEE_OTHER)
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
    flash(request,"Elave olundu", "success")
    return RedirectResponse(url=f"/admin/staff",status_code=HTTP_303_SEE_OTHER)

@staff_panel.get("/staff/{id}/delete")
def delete_staff(id:int, request: Request, db:Session = Depends(database.get_db)):
    FILEPATH = "static/staff_images/"
    delete_option = db.query(models.Staff).filter_by(id=id)
    image = delete_option.first().photo
    name = delete_option.first().name_surname
    delete_option.delete()
    db.commit()
    if image:
        old = pathlib.Path(FILEPATH+image)
        old.unlink()
    flash(request,f'"{name}" silindi', 'success')
    return RedirectResponse(url="/admin/staff",status_code=HTTP_303_SEE_OTHER)

