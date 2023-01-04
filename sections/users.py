from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import and_
import models, database, paginate, time_calculate
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from routers import admin
from utils.helper import templates, flash, get_flashed_messages
from datetime import datetime

users_panel = APIRouter(
    tags=['Dashboard / Users'],
)

########### Users ###########
@users_panel.get("/admin-users")
async def index(request: Request, db: Session = Depends(database.get_db), page: int = 1, page_size: int = 10):
    unread = db.query(models.AdminMessages).filter_by(readed=0).all()
    user_admin = db.query(models.User).filter_by(admin_user = True).all()
    users = db.query(models.User).all()
    counts = admin.return_count()
    data_length = len(user_admin)
    response = paginate.paginate(data=user_admin, data_length=data_length,page=page, page_size=page_size)

    messages_time = time_calculate.messages_time()
    return templates.TemplateResponse("dashboard/admin_users.html", {"request": request, "user_admin":response, "count":len(users), 
                                        "messages_time":messages_time, "unread":unread, "counts":counts} )

@users_panel.get("/user/{id}")
def user_profile(id: int, request: Request, db: Session = Depends(database.get_db)):
    unread = db.query(models.AdminMessages).filter_by(readed=0).all()
    user = db.query(models.User).filter_by(id=id).first()

    messages_time = time_calculate.messages_time()
    return templates.TemplateResponse("dashboard/profile.html", {"request":request,"user":user, "messages_time":messages_time, "unread":unread})


@users_panel.get("/user/{id}/edit")
def user_update(id: int, request: Request, db:Session = Depends(database.get_db)):
    unread = db.query(models.AdminMessages).filter_by(readed=0).all()
    user = db.query(models.User).filter_by(id=id).first()
    users = db.query(models.User).all()
    education = db.query(models.Education).all()
    selected_edu = db.query(models.Education).filter_by(id=id).first()
    counts = admin.return_count()
    messages_time = time_calculate.messages_time()
    return templates.TemplateResponse("dashboard/edit_user.html", {"request":request, "user":user, "count": len(users), "messages_time":messages_time,
                                        "education":education, "selected_edu":selected_edu, "unread":unread, "counts":counts})

@users_panel.post("/user/{id}/edit")
async def update(id:int, request: Request, db:Session = Depends(database.get_db)):
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
    user = db.query(models.User).filter_by(id=id)
    user.update({'name_surname':name_surname, 'age':age, 'city':city, 'phone':phone,
                'education':education, 'certificate_points':certificate_points, 'about':about,
                'select_university_id':select_university_id, 'created_at':created_at, 'admin_user':admin_user, 'is_active':is_active },synchronize_session=False)
    db.commit()
    flash(request,"Updated", "success")
    return RedirectResponse(url=f"/admin/user/{id}",status_code=HTTP_303_SEE_OTHER)