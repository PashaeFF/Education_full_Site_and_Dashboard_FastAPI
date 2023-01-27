from fastapi import APIRouter, Request, Depends, UploadFile
from typing import Optional
from PIL import Image
from sqlalchemy.orm import Session
from configurations import models, database
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
import secrets, pathlib
from utils.helper import templates, check_user, default_variables


staff_panel = APIRouter(
    tags=['Dashboard / Staff'],
)


@staff_panel.get('/staff')
def staff(request: Request):
    check = check_user(request)
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            variables = default_variables(request)
            page_title = check['dashboard_language'].staff_title
            return templates.TemplateResponse("dashboard/staff.html",{"request":request,"staff":variables['staff'], "messages_time": variables['messages_time'],
                                                "unread":variables['unread'], "counts":variables['counts'], "count":len(variables['users']), "user":check['user'],
                                                 "flash":variables['_flash_message'], "page_title":page_title, "language":check['dashboard_language'],
                                                 "dashboard_languages":check['dashboard_languages']})
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/admin/login", status_code=HTTP_303_SEE_OTHER)


@staff_panel.post("/staff")
async def create_staff(request: Request, db:Session = Depends(database.get_db),file: Optional[UploadFile] = None):
    check = check_user(request)
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
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
            if len(filename) > 0 and len(name_surname) > 0 and len(job_position) > 0:
                extension = filename.split(".")[1]
                if extension not in ["png","jpg","jpeg"]:
                    request.session["flash_messsage"].append({"message": check['dashboard_language'].image_extension_error, "category": "error"})
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
                request.session["flash_messsage"].append({"message": check['dashboard_language'].was_added, "category": "success"})
                request = RedirectResponse(url=f"/admin/staff",status_code=HTTP_303_SEE_OTHER)
                return request
            else:
                request.session["flash_messsage"].append({"message": check['dashboard_language'].required_boxes_error, "category": "error"})
                request = RedirectResponse(url=f"/admin/staff",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/admin/login", status_code=HTTP_303_SEE_OTHER)


@staff_panel.get("/staff/{id}/delete")
def delete_staff(id:int, request: Request, db:Session = Depends(database.get_db)):
    check = check_user(request)
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
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
            request.session["flash_messsage"].append({"message": check['dashboard_language'].deleted, "category": "success"})
            request = RedirectResponse(url=f"/admin/staff",status_code=HTTP_303_SEE_OTHER)
            return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/admin/login", status_code=HTTP_303_SEE_OTHER)

