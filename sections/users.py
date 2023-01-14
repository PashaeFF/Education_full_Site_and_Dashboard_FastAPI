from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
import models, database, paginate, time_calculate
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from routers import admin
from utils.helper import templates
from configurations.token import verify_token

users_panel = APIRouter(
    tags=['Dashboard / Users'],
)

########### Users ###########
@users_panel.get("/admin-users")
async def index(request: Request, db: Session = Depends(database.get_db), page: int = 1, page_size: int = 10):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    if user:
        if user.admin_user == True or user.super_user == True:
            unread = db.query(models.AdminMessages).filter_by(readed=0).all()
            user_admin = db.query(models.User).filter_by(admin_user = True).all()
            users = db.query(models.User).all()
            counts = admin.return_count()
            data_length = len(user_admin)
            response = paginate.paginate(data=user_admin, data_length=data_length,page=page, page_size=page_size)
            messages_time = time_calculate.messages_time()
            return templates.TemplateResponse("dashboard/admin_users.html", {"request": request, "user_admin":response, "count":len(users), 
                                                "messages_time":messages_time, "unread":unread, "counts":counts, "user":user} )
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@users_panel.get("/user/{id}")
def user_profile(id: int, request: Request, db: Session = Depends(database.get_db)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    change_user = db.query(models.User).filter_by(id=id).first()
    if user:
        if user.admin_user == True or user.super_user == True:
            if change_user:
                unread = db.query(models.AdminMessages).filter_by(readed=0).all()
                messages_time = time_calculate.messages_time()
                ########## flash message
                _flash_message = ""
                if request.session.get("flash_messsage"):
                    _flash_message = request.session.get("flash_messsage")
                    request.session.pop("flash_messsage") if "flash_messsage" in request.session else []
                return templates.TemplateResponse("dashboard/profile.html", {"request":request,"user":user, "messages_time":messages_time, 
                                                                            "flash":_flash_message, "unread":unread, "change_user":change_user})
            else:
                request.session["flash_messsage"].append({"message": "Mövcud deyil...", "category": "error"})
                request = RedirectResponse(url="/admin",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@users_panel.get("/user/{id}/edit")
def user_update(id: int, request: Request, db:Session = Depends(database.get_db)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    change_user = db.query(models.User).filter_by(id=id).first()
    request.session["flash_messsage"] = []
    if user:
        if user.admin_user == True or user.super_user == True:
            if change_user:
                unread = db.query(models.AdminMessages).filter_by(readed=0).all()
                users = db.query(models.User).all()
                education = db.query(models.Education).all()
                selected_edu = db.query(models.Education).filter_by(id=id).first()
                counts = admin.return_count()
                messages_time = time_calculate.messages_time()
                return templates.TemplateResponse("dashboard/edit_user.html", {"request":request, "user":user, "count": len(users), "messages_time":messages_time,
                                                    "education":education, "selected_edu":selected_edu, "unread":unread, "counts":counts, "change_user":change_user})
            else:
                request.session["flash_messsage"].append({"message": "Mövcud deyil...", "category": "error"})
                request = RedirectResponse(url="/admin",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@users_panel.post("/user/{id}/edit")
async def update(id:int, request: Request, db:Session = Depends(database.get_db)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    change_user = db.query(models.User).filter_by(id=id)
    request.session["flash_messsage"] = []
    if user:
        if user.admin_user == True or user.super_user == True:
            if change_user.first():
                form = await request.form()
                name_surname = form.get("name_surname")
                phone = form.get("phone")
                age = form.get("age")
                city = form.get("city")
                education = form.get("education")
                certificate_points = form.get("certificate_points")
                about = form.get("about")
                select_university_id = form.get("select_university_id")
                created_at = form.get("created_at")
                admin_user = form.get("admin_user")
                is_active = form.get("is_active")
                if admin_user == "on":
                    admin_user = True
                elif admin_user is None:
                    admin_user = False
                if is_active == "on":
                    is_active = True
                elif is_active is None:
                    is_active = False
                change_user.update({'name_surname':name_surname, 'age':age, 'city':city, 'phone':phone,
                            'education':education, 'certificate_points':certificate_points, 'about':about,
                            'select_university_id':select_university_id, 'created_at':created_at, 'admin_user':admin_user, 'is_active':is_active },synchronize_session=False)
                db.commit()
                request.session["flash_messsage"].append({"message": "Updated", "category": "success"})
                request = RedirectResponse(url=f"/admin/user/{id}", status_code=HTTP_303_SEE_OTHER)
                return request
            else:
                request.session["flash_messsage"].append({"message": f"Mövcud deyil...", "category": "error"})
                request = RedirectResponse(url="/admin/",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)