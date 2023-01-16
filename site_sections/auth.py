from fastapi import APIRouter, Request, Depends, Response
from sqlalchemy.orm import Session
import configurations.models as models, configurations.database as database
from sqlalchemy.exc import IntegrityError
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from utils.helper import templates, check_user_in_site, site_default_variables
from utils.hashing import Hasher
from configurations.token import create_access_token


authorization = APIRouter(
    tags=['Site / Authorization']
)

@authorization.get("/logout")
def logout(response: Response, request: Request):
    response = RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
    response.delete_cookie('access_token')
    return response


@authorization.get("/login")
async def login_page(request: Request):
    check_site_user = check_user_in_site(request)
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        if check_site_user['current_user']:
            return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
        else:
            variables = site_default_variables(request)
            page_title = check_site_user['site_settings'].site_title +" - İstifadəçi girişi"
        return templates.TemplateResponse("site/route/login.html", {"request":request, "site_settings":check_site_user['site_settings'],
                                            "current_user":check_site_user['current_user'], "page_title":page_title, "categories":variables['categories'],
                                            "news_category":variables['news_category'], "user":check_site_user['user'], "flash":variables['_flash_message']})


@authorization.post("/login")
@authorization.post("/admin/login")
async def post_login(response: Response, request: Request, db: Session = Depends(database.get_db)):
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
            response = RedirectResponse(url=request.headers['referer'], status_code=HTTP_303_SEE_OTHER)
            response.set_cookie(key="access_token", value=f"Bearer {create_access_token(data=data)}", httponly=True)
            return response
        else:
            request.session["flash_messsage"].append({"message": "Parol səhvdir", "category": "error"})
            request = RedirectResponse(url=request.headers['referer'], status_code=HTTP_303_SEE_OTHER)
            return request
    else:
        request.session["flash_messsage"].append({"message": "İstifadəçi mövcud deyil...", "category": "error"})
        request = RedirectResponse(url=request.headers['referer'], status_code=HTTP_303_SEE_OTHER)
        return request
    

@authorization.get("/registration")
def registration(request: Request):
    check_site_user = check_user_in_site(request)
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        if check_site_user['current_user']:
            return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
        else:
            variables = site_default_variables(request)
            page_title = check_site_user['site_settings'].site_title +" - Qeydiyyat"
            return templates.TemplateResponse("site/route/register.html",{"request":request, "site_settings":check_site_user['site_settings'],
                                                "current_user":check_site_user['current_user'], "page_title":page_title, "categories":variables['categories'],
                                                "news_category":variables['news_category'], "flash":variables['_flash_message'], "user":check_site_user['user']})


@authorization.post("/registration")
async def post_registration(request: Request, response: Response, db:Session = Depends(database.get_db)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    name_surname = form.get("name_surname")
    check_email = db.query(models.User).filter_by(email=email).first()
    request.session["flash_messsage"] = []
    if "@" not in email:
        request.session["flash_messsage"].append({"message": "Emaili düzgün qeyd edin", "category": "error"})
        request = RedirectResponse(url="/registration",status_code=HTTP_303_SEE_OTHER)
        return request
    if len(password) < 8:
        request.session["flash_messsage"].append({"message": "Parol minimum 8 simvol olmalıdır", "category": "error"})
        request = RedirectResponse(url="/registration",status_code=HTTP_303_SEE_OTHER)
        return request
    if len(name_surname) < 1:
        request.session["flash_messsage"].append({"message": "Ad əlavə etməmisiniz", "category": "error"})
        request = RedirectResponse(url="/registration",status_code=HTTP_303_SEE_OTHER)
        return request
    if check_email:
        request.session["flash_messsage"].append({"message": "Email mövcuddur", "category": "error"})
        request = RedirectResponse(url="/registration",status_code=HTTP_303_SEE_OTHER)
        return request
    user = models.User(email=email, password=Hasher.get_hash_password(password), name_surname=name_surname)
    db.add(user)
    db.commit()
    db.refresh(user)
    change = db.query(models.User).filter_by(email=email).first()
    data = {
            "sub": email,
            "id": user.id,
        }
    request.session["flash_messsage"].append({"message": "Daxil oldunuz", "category": "success"})
    response = RedirectResponse(url=f"/update_profile/{change.id}", status_code=HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=f"Bearer {create_access_token(data=data)}", httponly=True)
    return response










