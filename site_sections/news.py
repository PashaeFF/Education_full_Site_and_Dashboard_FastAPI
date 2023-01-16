from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
import configurations.models as models, configurations.database as database
from utils.helper import templates, check_user_in_site, site_default_variables
from utils import paginate


site_news = APIRouter(
    tags=['Site/News']
)


@site_news.get("/news")
def get_all_news(request: Request, page: int = 1, page_size: int = 5):
    check_site_user = check_user_in_site(request)
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        else:
            variables = site_default_variables(request)
            page_title = check_site_user['site_settings'].site_title+" - Xəbərlər"
            response = paginate.paginate(data=variables['news'], data_length=len(variables['news']),page=page, page_size=page_size)
            return templates.TemplateResponse("site/route/news-page.html", {"request": request,"response":response, "current_user":check_site_user['current_user'], "user":check_site_user['user'],
                                                "page_title":page_title, "site_settings":check_site_user['site_settings'], "categories":variables['categories'], "news_category":variables['news_category']})


@site_news.get("/news/{name}/{id}")
def get_news_id(name: str, id: int, request: Request, db: Session = Depends(database.get_db)):
    check_site_user = check_user_in_site(request)
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        else:
            variables = site_default_variables(request)
            news = db.query(models.SiteNews).filter_by(id=id).first()
            page_title = check_site_user['site_settings'].site_title+" - "+news.news_title
            return templates.TemplateResponse("site/route/full_news.html", {"request": request,"news":news, "site_settings":check_site_user['site_settings'],
                                                "page_title":page_title, "categories":variables['categories'], "news_category":variables['news_category'], 
                                                "user":check_site_user['user'], "current_user":check_site_user['current_user']})


@site_news.get("/news/{name}")
def get_category(name: str, request: Request, db: Session = Depends(database.get_db), page: int = 1, page_size: int = 5):
    check_site_user = check_user_in_site(request)
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        else:
            variables = site_default_variables(request)
            category = db.query(models.NewsCategory).filter_by(name=name).first()
            news = db.query(models.SiteNews).filter_by(select_category_id=category.id).all()
            page_title = check_site_user['site_settings'].site_title+" - "+category.name
            response = paginate.paginate(data=news, data_length=len(news), page=page, page_size=page_size)
            return templates.TemplateResponse("site/route/news-page.html", {"request": request, "category":category, "page_title":page_title,
                                                "response":response, "site_settings":check_site_user['site_settings'], "news_category":variables['news_category'],
                                                "user":check_site_user['user'], "current_user":check_site_user['current_user']})

