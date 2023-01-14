from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from sqlalchemy.orm import Session
import models, database, paginate, time_calculate
from starlette.status import HTTP_303_SEE_OTHER
from datetime import datetime, timedelta
from sections import education_dashboard, users, slider, settings, news, staff, messages
from utils.helper import templates
from utils.hashing import Hasher
from configurations.token import verify_token, create_access_token

dashboard = APIRouter(
    prefix= ("/admin")
)

def return_count(db: Depends = database.get_db()):
    one_day = datetime.now() - timedelta(days=1)
    week = datetime.now() - timedelta(days=7)
    month = datetime.now() - timedelta(days=30)
    yesterday = one_day - timedelta(days=2)
    last_week = week - timedelta(days=14)
    last_month = month - timedelta(days=60)

    users_one_day_count = db.query(models.User).where(models.User.created_at > one_day).count()
    users_week_count = db.query(models.User).where(models.User.created_at > week).count()
    users_month_count = db.query(models.User).where(models.User.created_at > month).count()
    users_yesterday_count = db.query(models.User).where(models.User.created_at > yesterday).count()
    users_last_week_count = db.query(models.User).where(models.User.created_at > last_week).count()
    users_last_month_count = db.query(models.User).where(models.User.created_at > last_month).count()

    difference_one_day = users_yesterday_count - users_one_day_count
    difference_week = users_last_week_count - users_week_count
    difference_month = users_last_month_count - users_month_count
    if difference_one_day > 0:
        difference_one_day = f"+{difference_one_day}"
    if difference_week > 0:
        difference_week = f"+{difference_week}"
    if difference_month > 0:
        difference_month = f"+{difference_month}"


    counts = {"users_one_day_count":users_one_day_count,
                "users_week_count":users_week_count,
                "users_month_count":users_month_count,
                "difference_one_day":difference_one_day,
                "difference_week":difference_week,
                "difference_month":difference_month}
    return counts

@dashboard.get("/")
@dashboard.get("/users")
async def index(request: Request, db: Session = Depends(database.get_db), page: int = 1, page_size: int = 10):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    if user:
        if user.admin_user == True or user.super_user == True:
            unread = db.query(models.AdminMessages).filter_by(readed=0).all()
            users = db.query(models.User).all()
            counts = return_count()
            data_length = len(users)
            messages_time = time_calculate.messages_time()
            response = paginate.paginate(data=users, data_length=data_length,page=page, page_size=page_size)
            ########## flash message
            _flash_message = ""
            if request.session.get("flash_messsage"):
                _flash_message = request.session.get("flash_messsage")
                request.session.pop("flash_messsage") if "flash_messsage" in request.session else []
            return templates.TemplateResponse("dashboard/index.html", {"request": request, "response": response, "count": len(users), "user":user,
                                                                        "messages_time":messages_time, "counts":counts, "unread": unread,
                                                                        "flash":_flash_message } )
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

@dashboard.get("/login")
def dashboard_login(request: Request, db: Session = Depends(database.get_db)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    if current_user:
        return RedirectResponse(url="/admin", status_code=HTTP_303_SEE_OTHER)
    page_title = "Idarə paneli"
    ########## flash message
    _flash_message = ""
    if request.session.get("flash_messsage"):
        _flash_message = request.session.get("flash_messsage")
        request.session.pop("flash_messsage") if "flash_messsage" in request.session else []
    return templates.TemplateResponse("dashboard/sign-in.html",{"request":request, "user":user, "current_user":current_user,
                                                                "page_title":page_title, "flash":_flash_message})

@dashboard.post("/login")
async def post_dashboard_login(response: Response, request: Request, db: Session = Depends(database.get_db)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    user = db.query(models.User).filter_by(email=email).first()
    request.session["flash_messsage"] = []
    if user:
        if Hasher.verify_password(password,user.password) == True:
            data = {
                "sub": email,
                "id": user.id,
            }
            request.session["flash_messsage"].append({"message": "Daxil oldunuz", "category": "success"})
            response = RedirectResponse(url="/admin", status_code=HTTP_303_SEE_OTHER)
            response.set_cookie(key="access_token", value=f"Bearer {create_access_token(data=data)}", httponly=True)
            return response
        else:
            request.session["flash_messsage"].append({"message": "Parol səhvdir", "category": "error"})
            request = RedirectResponse(url="/admin/login", status_code=HTTP_303_SEE_OTHER)
            return request
    else:
        request.session["flash_messsage"].append({"message": "İstifadəçi mövcud deyil...", "category": "error"})
        request = RedirectResponse(url="/admin/login", status_code=HTTP_303_SEE_OTHER)
        return request

@dashboard.post("/functions/{id}")
async def post_functions(id:str, response: Response, request: Request, db: Session = Depends(database.get_db)):
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user)
    if user:
        form = await request.form()
        if id == "fixed":
            navbar_fixed = form.get("navbar_fixed")
            user.update({"navbar_fixed":navbar_fixed})
        if id == "mode":
            site_mode = form.get("site_mode")
            user.update({"site_mode":site_mode})
        if id == "color":
            sidebar_selected_color = form.get("sidebar_selected_color")
            user.update({"sidebar_selected_color":sidebar_selected_color})
        db.commit()
        for i in request.headers.items():
            if i[0] == 'referer':
                referer = i[1]
        return RedirectResponse(url=referer, status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)



dashboard.include_router(users.users_panel)
dashboard.include_router(slider.slider_panel)
dashboard.include_router(settings.settings_panel)
dashboard.include_router(education_dashboard.education_panel)
dashboard.include_router(news.news_panel)
dashboard.include_router(staff.staff_panel)
dashboard.include_router(messages.messages_panel)