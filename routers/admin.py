from fastapi import APIRouter, Request, Depends, Response
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from sqlalchemy.orm import Session
from sections import education_dashboard, users, slider, settings, news, staff, messages, site_languages
from utils.helper import templates, check_user, default_variables
from utils import paginate
from configurations import models, database

dashboard = APIRouter(
    prefix= ("/admin")
)


@dashboard.get("/")
@dashboard.get("/users")
async def index(request: Request, page: int = 1, page_size: int = 10):
    check = check_user(request)
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            variables = default_variables(request)
            page_title = check['dashboard_language'].dashboard_title
            response = paginate.paginate(data=variables['users'], data_length=len(variables['users']),page=page, page_size=page_size)
            return templates.TemplateResponse("dashboard/index.html", {"request": request, "response": response, "count": len(variables['users']), "user":check['user'],
                                                                        "messages_time":variables['messages_time'], "counts":variables['counts'], "unread": variables['unread'],
                                                                        "flash": variables['_flash_message'], "page_title":page_title, "language":check['dashboard_language'],
                                                                        "dashboard_languages":check['dashboard_languages']})
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/admin/login", status_code=HTTP_303_SEE_OTHER)


@dashboard.get("/login")
def dashboard_login(request: Request):
    check = check_user(request)
    variables = default_variables(request)
    if check['current_user']:
        return RedirectResponse(url="/admin", status_code=HTTP_303_SEE_OTHER)
    page_title = check['dashboard_language'].dashboard_title
    return templates.TemplateResponse("dashboard/sign-in.html",{"request":request, "user":check['user'], "current_user":check['current_user'],
                                                                "page_title":page_title, "flash":variables['_flash_message'], "language":check['dashboard_language'],
                                                                "dashboard_languages":check['dashboard_languages']})


@dashboard.post("/lang/")
async def post_language(request: Request, db: Session = Depends(database.get_db)):
    check = check_user(request)
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            user = db.query(models.User).filter_by(id=check['current_user'])
            if user:
                form = await request.form()
                user.update({"user_dashboard_language":form.get('id')})
                db.commit()
                for i in request.headers.items():
                    if i[0] == 'referer':
                        referer = i[1]
                return RedirectResponse(url=referer, status_code=HTTP_303_SEE_OTHER)
        else:
            return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)


@dashboard.post("/functions/{id}")
async def post_functions(id:str, request: Request, db: Session = Depends(database.get_db)):
    check = check_user(request)
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            user = db.query(models.User).filter_by(id=check['current_user'])
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
    else:
        return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)



dashboard.include_router(users.users_panel)
dashboard.include_router(slider.slider_panel)
dashboard.include_router(settings.settings_panel)
dashboard.include_router(education_dashboard.education_panel)
dashboard.include_router(news.news_panel)
dashboard.include_router(staff.staff_panel)
dashboard.include_router(messages.messages_panel)
dashboard.include_router(site_languages.languages_panel)