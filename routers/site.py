from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
import configurations.models as models, configurations.database as database
from utils.helper import templates, check_user_in_site, site_default_variables
from site_sections import news, educations, contact, auth, user


site_main = APIRouter(
    tags=['Site']
)

@site_main.get("/")
async def index(request: Request):
    check_site_user = check_user_in_site(request)
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        else:
            variables = site_default_variables(request)
            page_title = check_site_user['site_settings'].site_title
            return templates.TemplateResponse("site/index.html", {"request": request,"page_title":page_title, "slider":variables['slider'],"educations":variables['educations'], "news":variables['news'],
                                                                    "site_settings":check_site_user['site_settings'], "categories":variables['categories'], "news_category":variables['news_category'],
                                                                    "current_user":check_site_user['current_user'], "user":check_site_user['user'], "flash":variables['_flash_message']})
    else:
        return templates.TemplateResponse("site/closed.html", {"request":request})


@site_main.get("/slider/{id}")
def slider(id: int, request: Request, db: Session = Depends(database.get_db)):
    check_site_user = check_user_in_site(request)
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        else:
            variables = site_default_variables(request)
            slider = db.query(models.SliderSettings).filter_by(id=id).first()
            page_title = check_site_user['site_settings'].site_title+" - "+slider.title
            return templates.TemplateResponse("site/route/slide_full_news.html", {"request": request,"slider":slider, "categories":variables['categories'],
                                                "page_title":page_title, "site_settings":check_site_user['site_settings'], "news_category":variables['news_category'],
                                                "user":check_site_user['user'], "current_user":check_site_user['current_user']})


@site_main.get("/about")
def about_page(request: Request):
    check_site_user = check_user_in_site(request)
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        else:
            variables = site_default_variables(request)
            page_title = check_site_user['site_settings'].site_title+" - Haqqımızda"
            return templates.TemplateResponse("site/route/about-page.html", {"request":request, "site_settings":check_site_user['site_settings'],
                                                                                "user":check_site_user['user'], "current_user":check_site_user['current_user'],
                                                                                "page_title":page_title, "categories":variables['categories'],
                                                                                "news_category":variables['news_category'], "staff":variables['staff']})


site_main.include_router(auth.authorization)
site_main.include_router(user.user_panel)
site_main.include_router(news.site_news)
site_main.include_router(educations.site_educations)
site_main.include_router(contact.contact_page)