from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
import schemas, models, database, paginate
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from utils.helper import templates, closed, flash, get_flashed_messages

main = APIRouter(
    tags=['Site']
)

@main.get("/")
async def index(request: Request, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    if site_settings:
        if site_settings.is_active is None:
            return closed()
        else:
            slider = db.query(models.SliderSettings).all()
            educations = db.query(models.Education).all()
            categories = db.query(models.EduCategory).all()
            news = db.query(models.SiteNews).all()
            news_category = db.query(models.NewsCategory).all()
            page_title = site_settings.site_title
            return templates.TemplateResponse("site/index.html", {"request": request,"page_title":page_title, "slider":slider,"educations":educations, "news":news,
                                                                    "site_settings":site_settings, "categories":categories, "news_category":news_category})
    else:
        return 'Sayt melumatlari yerleshdirilmeyib...'


@main.get("/news")
def get_all_news(request: Request, db: Session = Depends(database.get_db), page: int = 1, page_size: int = 5):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    if site_settings:
        if site_settings.is_active is None:
            return closed()
        else:
            category = db.query(models.NewsCategory).all()
            news = db.query(models.SiteNews).all()
            categories = db.query(models.EduCategory).all()
            news_category = db.query(models.NewsCategory).all()
            data_length = len(news)
            page_title = site_settings.site_title+" - Xəbərlər"
            response = paginate.paginate(data=news, data_length=data_length,page=page, page_size=page_size)
            return templates.TemplateResponse("site/route/news-page.html", {"request": request,"response":response, 
                                                "page_title":page_title, "site_settings":site_settings, "categories":categories, "news_category":news_category, "category":category})
    else:
        return 'Sayt melumatlari yerleshdirilmeyib...'

@main.get("/educations")
def get_all_news(request: Request, db: Session = Depends(database.get_db), page: int = 1, page_size: int = 6):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    if site_settings:
        if site_settings.is_active is None:
            return closed()
        else:
            categories = db.query(models.EduCategory).all()
            category_name = db.query(models.EduCategory).all()
            education = db.query(models.Education).all()
            news_category = db.query(models.NewsCategory).all()
            data_length = len(education)
            page_title = site_settings.site_title+" - Təhsil"
            response = paginate.paginate(data=education, data_length=data_length,page=page, page_size=page_size)
            return templates.TemplateResponse("site/route/educations-page.html", {"request": request, "response":response,"category_name":category_name,
                                                "page_title":page_title, "site_settings":site_settings, "categories":categories, "news_category":news_category})
    else:
        return 'Sayt melumatlari yerleshdirilmeyib...'


@main.get("/slider/{id}")
def slider(id: int, request: Request, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    if site_settings:
        if site_settings.is_active is None:
            return closed()
        else:
            slider = db.query(models.SliderSettings).filter_by(id=id).first()
            categories = db.query(models.EduCategory).all()
            news_category = db.query(models.NewsCategory).all()
            page_title = site_settings.site_title+" - "+slider.title
            return templates.TemplateResponse("site/route/slide_full_news.html", {"request": request,"slider":slider, "categories":categories,
                                                "page_title":page_title, "site_settings":site_settings, "news_category":news_category})
    else:
        return 'Sayt melumatlari yerleshdirilmeyib...'


@main.get("/educations/{education_type}/{id}")
def educations(education_type: str, id: int, request: Request, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    if site_settings:
        if site_settings.is_active is None:
            return closed()
        else:
            education = db.query(models.Education).filter_by(id=id).first()
            categories = db.query(models.EduCategory).all()
            news_category = db.query(models.NewsCategory).all()
            page_title = site_settings.site_title+" - "+education.name
            return templates.TemplateResponse("site/route/education_details.html", {"request": request,"education":education, "site_settings":site_settings,
                                                "page_title":page_title, "categories":categories,"news_category":news_category})
    else:
        return 'Sayt melumatlari yerleshdirilmeyib...'


@main.get("/educations/{name}")
def get_category(name: str, request: Request, db: Session = Depends(database.get_db), page: int = 1, page_size: int = 6):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    if site_settings:
        if site_settings.is_active is None:
            return closed()
        else:
            categories = db.query(models.EduCategory).all()
            category_name = db.query(models.EduCategory).filter_by(name=name).first()
            education = db.query(models.Education).filter_by(education_type=name).all()
            news_category = db.query(models.NewsCategory).all()
            data_length = len(education)
            page_title = site_settings.site_title+" - "+category_name.name
            response = paginate.paginate(data=education, data_length=data_length,page=page, page_size=page_size)
            return templates.TemplateResponse("site/route/educations-page.html", {"request": request,"category_name":category_name, "page_title":page_title,
                                                "response":response, "site_settings":site_settings, "categories":categories, "news_category":news_category})
    else:
        return 'Sayt melumatlari yerleshdirilmeyib...'


@main.get("/news/{name}/{id}")
def get_news_id(name: str, id: int, request: Request, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    if site_settings:
        if site_settings.is_active is None:
            return closed()
        else:
            news = db.query(models.SiteNews).filter_by(id=id).first()
            categories = db.query(models.EduCategory).all()
            news_category = db.query(models.NewsCategory).all()
            page_title = site_settings.site_title+" - "+news.news_title
            return templates.TemplateResponse("site/route/full_news.html", {"request": request,"news":news, "site_settings":site_settings,
                                                "page_title":page_title, "categories":categories, "news_category":news_category})
    else:
        return 'Sayt melumatlari yerleshdirilmeyib...'


@main.get("/news/{name}")
def get_category(name: str, request: Request, db: Session = Depends(database.get_db), page: int = 1, page_size: int = 5):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    if site_settings:
        if site_settings.is_active is None:
            return closed()
        else:
            category = db.query(models.NewsCategory).filter_by(name=name).first()
            news_category = db.query(models.NewsCategory).all()
            news = db.query(models.SiteNews).filter_by(select_category_id=category.id).all()
            data_length = len(news)
            page_title = site_settings.site_title+" - "+category.name
            response = paginate.paginate(data=news, data_length=data_length,page=page, page_size=page_size)
            return templates.TemplateResponse("site/route/news-page.html", {"request": request, "category":category, "page_title":page_title,
                                                "response":response, "site_settings":site_settings, "news_category":news_category})
    else:
        return 'Sayt melumatlari yerleshdirilmeyib...'

@main.get("/about")
def about_page(request: Request, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    if site_settings:
        if site_settings.is_active is None:
            return closed()
        else:
            categories = db.query(models.EduCategory).all()
            news_category = db.query(models.NewsCategory).all()
            staff = db.query(models.Staff).all()
            page_title = site_settings.site_title+" - Haqqımızda"
            return templates.TemplateResponse("site/route/about-page.html", {"request":request, "site_settings":site_settings,
                                                "page_title":page_title, "categories":categories,"news_category":news_category, "staff":staff})
    else:
        return 'Sayt melumatlari yerleshdirilmeyib...'


@main.get("/contact")
def about_page(request: Request, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    if site_settings:
        if site_settings.is_active is None:
            return closed()
        else:
            categories = db.query(models.EduCategory).all()
            news_category = db.query(models.NewsCategory).all()
            page_title = site_settings.site_title+" - Əlaqə"
            return templates.TemplateResponse("site/route/contactus-page.html", {"request":request, "site_settings":site_settings,
                                                "page_title":page_title, "categories":categories,"news_category":news_category})
    else:
        return 'Sayt melumatlari yerleshdirilmeyib...'

@main.post("/contact")
async def send_message(request: Request, db: Session = Depends(database.get_db)):
    form = await request.form()
    name = form.get("name")
    email = form.get("email")
    message = form.get("message")

    save_message = models.AdminMessages(name=name, email=email, message=message)
    db.add(save_message)
    db.commit()
    db.refresh(save_message)
    flash(request,"Mesajınız rəhbərliyə göndərildi", "success")
    return RedirectResponse(url="/contact",status_code=HTTP_303_SEE_OTHER)
