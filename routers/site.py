from fastapi import APIRouter, Request, Depends, Response
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from sqlalchemy.orm import Session
from configurations import models, database
from utils.helper import templates, check_user_in_site, site_default_variables
from site_sections import news, educations, contact, auth, user


site_main = APIRouter(
    tags=['Site']
)


@site_main.post("/set_lang/")
async def user_set_language(request: Request, response: Response, db: Session = Depends(database.get_db)):
    form = await request.form()
    check_site_user = check_user_in_site(request)
    if check_site_user['user']:
        print(check_site_user['user'].id)
        user_set_language = db.query(models.User).filter_by(id=check_site_user['user'].id)
        user_set_language.update({
            'user_site_language':form.get('id')
            })
        db.commit()
        return RedirectResponse(url=f"/",status_code=HTTP_303_SEE_OTHER)
    response = RedirectResponse(url=f"/",status_code=HTTP_303_SEE_OTHER)
    response.set_cookie(key="user_site_language", value=form.get('id'), httponly=True)
    return response
        

@site_main.get("/")
async def index(request: Request):
    check_site_user = check_user_in_site(request)
    lang = check_user_in_site(request)['site_language']
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        else:
            variables = site_default_variables(request)
            page_title = check_site_user['site_settings'].site_title
            return templates.TemplateResponse("site/index.html", {"request": request,"page_title":page_title, "slider":variables['slider'],"educations":variables['educations'], "news":variables['news'],
                                                                    "site_settings":check_site_user['site_settings'], "categories":variables['categories'], "news_category":variables['news_category'],
                                                                    "current_user":check_site_user['current_user'], "user":check_site_user['user'], "flash":variables['_flash_message'],
                                                                    "language":lang, "langs":variables['languages_all']})
    else:
        return templates.TemplateResponse("site/closed.html", {"request":request})


@site_main.get("/slider/{id}")
def slider(id: int, request: Request, db: Session = Depends(database.get_db)):
    check_site_user = check_user_in_site(request)
    lang = check_user_in_site(request)['site_language']
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        else:
            variables = site_default_variables(request)
            slider = db.query(models.SliderSettings).filter_by(id=id).first()
            page_title = check_site_user['site_settings'].site_title+" - "+slider.title
            return templates.TemplateResponse("site/route/slide_full_news.html", {"request": request,"slider":slider, "categories":variables['categories'],
                                                "page_title":page_title, "site_settings":check_site_user['site_settings'], "news_category":variables['news_category'],
                                                "user":check_site_user['user'], "current_user":check_site_user['current_user'], "language":lang})


@site_main.get("/about")
def about_page(request: Request):
    check_site_user = check_user_in_site(request)
    lang = check_user_in_site(request)['site_language']
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        else:
            variables = site_default_variables(request)
            page_title = check_site_user['site_settings'].site_title+" - "+check_site_user['site_language'].site_about
            return templates.TemplateResponse("site/route/about-page.html", {"request":request, "site_settings":check_site_user['site_settings'],
                                                                                "user":check_site_user['user'], "current_user":check_site_user['current_user'],
                                                                                "page_title":page_title, "categories":variables['categories'],
                                                                                "news_category":variables['news_category'], "staff":variables['staff'],
                                                                                "language":lang})


site_main.include_router(auth.authorization)
site_main.include_router(user.user_panel)
site_main.include_router(news.site_news)
site_main.include_router(educations.site_educations)
site_main.include_router(contact.contact_page)