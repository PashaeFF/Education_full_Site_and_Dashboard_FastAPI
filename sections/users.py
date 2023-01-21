from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from configurations import models, database
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from utils.helper import templates, check_user, default_variables
from utils import paginate

users_panel = APIRouter(
    tags=['Dashboard / Users'],
)

########### Users ###########
@users_panel.get("/admin-users")
async def index(request: Request, page: int = 1, page_size: int = 10):
    check = check_user(request)
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            variables = default_variables(request)
            response = paginate.paginate(data=variables['user_admin'], data_length=len(variables['user_admin']),page=page, page_size=page_size)
            page_title = 'İstifadəçilər'
            return templates.TemplateResponse("dashboard/admin_users.html", {"request": request, "user_admin":response, "count":len(variables['users']), 
                                                "messages_time":variables['messages_time'], "unread":variables['unread'], "counts":variables['counts'], 
                                                "user":check['user'], "page_title":page_title} )
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/admin/login", status_code=HTTP_303_SEE_OTHER)


@users_panel.get("/user/{id}")
def user_profile(id: int, request: Request, db: Session = Depends(database.get_db)):
    ######## user_check #########
    check = check_user(request)
    change_user = db.query(models.User).filter_by(id=id).first()
    request.session["flash_messsage"] = []
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            if change_user:
                variables = default_variables(request)
                page_title = 'İstifadəçilər'
                if change_user.education_files:
                    user_education_files = change_user.education_files.split(',')
                else:
                    user_education_files = ""
                return templates.TemplateResponse("dashboard/profile.html", {"request":request,"user":check['user'], "messages_time":variables['messages_time'], 
                                                                            "flash":variables['_flash_message'], "unread":variables['unread'], "change_user":change_user,
                                                                            "page_title ":page_title, "user_education_files":user_education_files})
            else:
                request.session["flash_messsage"].append({"message": "Mövcud deyil...", "category": "error"})
                request = RedirectResponse(url="/admin",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/admin/login", status_code=HTTP_303_SEE_OTHER)


@users_panel.get("/user/{id}/edit")
def user_update(id: int, request: Request, db:Session = Depends(database.get_db)):
    ######## user_check #########
    check = check_user(request)
    change_user = db.query(models.User).filter_by(id=id).first()
    request.session["flash_messsage"] = []
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            if change_user:
                selected_edu = db.query(models.Education).filter_by(id=id).first()
                variables = default_variables(request)
                page_title = 'İstifadəçilər'
                return templates.TemplateResponse("dashboard/edit_user.html", {"request":request, "user":check['user'], "count": len(variables['users']), "messages_time":variables['messages_time'],
                                                    "education":variables['education'], "selected_edu":selected_edu, "unread":variables['unread'], "counts":variables['counts'], "change_user":change_user,
                                                    "page_title ":page_title})
            else:
                request.session["flash_messsage"].append({"message": "Mövcud deyil...", "category": "error"})
                request = RedirectResponse(url="/admin",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/admin/login", status_code=HTTP_303_SEE_OTHER)


@users_panel.post("/user/{id}/edit")
async def update(id:int, request: Request, db:Session = Depends(database.get_db)):
    ######## user_check #########
    check = check_user(request)
    change_user = db.query(models.User).filter_by(id=id)
    request.session["flash_messsage"] = []
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
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