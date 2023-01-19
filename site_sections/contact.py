from fastapi import APIRouter, Request, Depends, Response
from sqlalchemy.orm import Session
from configurations import models, database
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from utils.helper import templates, check_user_in_site, site_default_variables
from datetime import datetime


contact_page = APIRouter(
    tags=['Site/Contact']
)


@contact_page.get("/contact")
def about_page(request: Request, db: Session = Depends(database.get_db)):
    check_site_user = check_user_in_site(request)
    lang = check_user_in_site(request)['site_language']
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        else:
            variables = site_default_variables(request)
            page_title = check_site_user['site_settings'].site_title+" - "+lang.contact_page_title
            return templates.TemplateResponse("site/route/contactus-page.html", {"request":request, "site_settings":check_site_user['site_settings'],
                                                                                "user":check_site_user['user'], "current_user":check_site_user['current_user'],
                                                                                "page_title":page_title, "categories":variables['categories'],
                                                                                "news_category":variables['news_category'], "flash":variables['_flash_message'],"language":lang})


@contact_page.post("/contact")
async def send_message(request: Request, response: Response, db: Session = Depends(database.get_db)):
    check_site_user = check_user_in_site(request)
    lang = check_user_in_site(request)['site_language']
    antispam = request.cookies.get("time")
    current_time = datetime.now().strftime("%y%m%d%H%M%S")
    #######     end    ##########
    form = await request.form()
    name = form.get("name")
    email = form.get("email")
    message = form.get("message")
    request.session["flash_messsage"] = []
    if antispam:
        if antispam[0:11] == str(current_time)[0:11]:
            request.session["flash_messsage"].append({"message": lang.message_spam_message, "category": "error"})
            response = RedirectResponse(url="/contact",status_code=HTTP_303_SEE_OTHER)
            return response
    if check_site_user['user']:
        if len(message) == 0:
            request.session["flash_messsage"].append({"message": lang.the_message_cannot_empty_message, "category": "error"})
            response = RedirectResponse(url="/contact",status_code=HTTP_303_SEE_OTHER)
            return response
        save_message = models.AdminMessages(sender_id=check_site_user['user'].id, name=check_site_user['user'].name_surname, email=check_site_user['user'].email, message=message, created_at = datetime.now())
    else:
        if len(name) == 0 or  len(email) == 0 or len(message) == 0:
            request.session["flash_messsage"].append({"message": lang.boxes_are_cannot_empty, "category": "error"})
            response = RedirectResponse(url="/contact",status_code=HTTP_303_SEE_OTHER)
            return response
        save_message = models.AdminMessages(name=name, email=email, message=message, created_at = datetime.now()) 
    db.add(save_message)
    db.commit()
    db.refresh(save_message)
    request.session["flash_messsage"].append({"message": lang.message_has_been_sent_to_management, "category": "success"})
    response = RedirectResponse(url="/contact",status_code=HTTP_303_SEE_OTHER)
    response.set_cookie(key="time", value=current_time, httponly=True)
    return response