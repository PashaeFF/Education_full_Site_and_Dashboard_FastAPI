from fastapi import APIRouter, Request, Depends, Response
from sqlalchemy.orm import Session
import models, database, paginate
from configurations.token import verify_token
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from utils.helper import templates
from datetime import datetime


main = APIRouter(
    tags=['Site']
)

@main.get("/")
async def index(request: Request, response: Response, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    if access_token:
        current_user = verify_token(access_token)
        user = db.query(models.User).filter_by(id=current_user).first()
    else:
        current_user = ""
        user = ""
    #######     end    ##########
    if site_settings:
        if site_settings.is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        else:
            slider = db.query(models.SliderSettings).all()
            educations = db.query(models.Education).all()
            categories = db.query(models.EduCategory).all()
            news = db.query(models.SiteNews).all()
            news_category = db.query(models.NewsCategory).all()
            page_title = site_settings.site_title
            ########## flash message
            _flash_message = ""
            if request.session.get("flash_messsage"):
                _flash_message = request.session.get("flash_messsage")
                request.session.pop("flash_messsage") if "flash_messsage" in request.session else []
            return templates.TemplateResponse("site/index.html", {"request": request,"page_title":page_title, "slider":slider,"educations":educations, "news":news,
                                                                    "site_settings":site_settings, "categories":categories, "news_category":news_category,
                                                                    "current_user":current_user, "user":user, "flash":_flash_message})
    else:
        return templates.TemplateResponse("site/closed.html", {"request":request})


@main.get("/news")
def get_all_news(request: Request, db: Session = Depends(database.get_db), page: int = 1, page_size: int = 5):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    if access_token:
        current_user = verify_token(access_token)
        user = db.query(models.User).filter_by(id=current_user).first()
    else:
        current_user = ""
        user = ""
    #######     end    ##########
    if site_settings:
        if site_settings.is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request, "site_settings":site_settings})
        else:
            category = db.query(models.NewsCategory).all()
            news = db.query(models.SiteNews).all()
            categories = db.query(models.EduCategory).all()
            news_category = db.query(models.NewsCategory).all()
            data_length = len(news)
            page_title = site_settings.site_title+" - Xəbərlər"
            response = paginate.paginate(data=news, data_length=data_length,page=page, page_size=page_size)
            return templates.TemplateResponse("site/route/news-page.html", {"request": request,"response":response, "current_user":current_user, "user":user,
                                                "page_title":page_title, "site_settings":site_settings, "categories":categories, "news_category":news_category, "category":category})


@main.get("/educations")
def get_all_news(request: Request, db: Session = Depends(database.get_db), page: int = 1, page_size: int = 6):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    if access_token:
        current_user = verify_token(access_token)
        user = db.query(models.User).filter_by(id=current_user).first()
    else:
        current_user = ""
        user = ""
    #######     end    ##########
    if site_settings:
        if site_settings.is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request, "site_settings":site_settings})
        else:
            categories = db.query(models.EduCategory).all()
            category_name = db.query(models.EduCategory).all()
            education = db.query(models.Education).all()
            news_category = db.query(models.NewsCategory).all()
            data_length = len(education)
            page_title = site_settings.site_title+" - Təhsil"
            response = paginate.paginate(data=education, data_length=data_length,page=page, page_size=page_size)
            return templates.TemplateResponse("site/route/educations-page.html", {"request": request, "response":response,"category_name":category_name,
                                                "page_title":page_title, "site_settings":site_settings, "categories":categories, "news_category":news_category,
                                                "user":user, "current_user":current_user})


@main.get("/slider/{id}")
def slider(id: int, request: Request, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    if access_token:
        current_user = verify_token(access_token)
        user = db.query(models.User).filter_by(id=current_user).first()
    else:
        current_user = ""
        user = ""
    #######     end    ##########
    if site_settings:
        if site_settings.is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request, "site_settings":site_settings})
        else:
            slider = db.query(models.SliderSettings).filter_by(id=id).first()
            categories = db.query(models.EduCategory).all()
            news_category = db.query(models.NewsCategory).all()
            page_title = site_settings.site_title+" - "+slider.title
            return templates.TemplateResponse("site/route/slide_full_news.html", {"request": request,"slider":slider, "categories":categories,
                                                "page_title":page_title, "site_settings":site_settings, "news_category":news_category,
                                                "user":user, "current_user":current_user})


@main.get("/educations/{education_type}/{id}")
def educations(education_type: str, id: int, request: Request, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    if access_token:
        current_user = verify_token(access_token)
        user = db.query(models.User).filter_by(id=current_user).first()
    else:
        current_user = ""
        user = ""
    #######     end    ##########
    if site_settings:
        if site_settings.is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request, "site_settings":site_settings})
        else:
            education = db.query(models.Education).filter_by(id=id).first()
            categories = db.query(models.EduCategory).all()
            news_category = db.query(models.NewsCategory).all()
            page_title = site_settings.site_title+" - "+education.name
            return templates.TemplateResponse("site/route/education_details.html", {"request": request,"education":education, "site_settings":site_settings,
                                                "page_title":page_title, "categories":categories,"news_category":news_category, "user":user, "current_user":current_user})



@main.get("/educations/{name}")
def get_category(name: str, request: Request, db: Session = Depends(database.get_db), page: int = 1, page_size: int = 6):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    if access_token:
        current_user = verify_token(access_token)
        user = db.query(models.User).filter_by(id=current_user).first()
    else:
        current_user = ""
        user = ""
    #######     end    ##########
    if site_settings:
        if site_settings.is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request, "site_settings":site_settings})
        else:
            categories = db.query(models.EduCategory).all()
            category_name = db.query(models.EduCategory).filter_by(name=name).first()
            education = db.query(models.Education).filter_by(education_type=name).all()
            news_category = db.query(models.NewsCategory).all()
            data_length = len(education)
            page_title = site_settings.site_title+" - "+category_name.name
            response = paginate.paginate(data=education, data_length=data_length,page=page, page_size=page_size)
            return templates.TemplateResponse("site/route/educations-page.html", {"request": request,"category_name":category_name, "page_title":page_title,
                                                "response":response, "site_settings":site_settings, "categories":categories, "news_category":news_category,
                                                "user":user, "current_user":current_user})


@main.get("/news/{name}/{id}")
def get_news_id(name: str, id: int, request: Request, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    if access_token:
        current_user = verify_token(access_token)
        user = db.query(models.User).filter_by(id=current_user).first()
    else:
        current_user = ""
        user = ""
    #######     end    ##########
    if site_settings:
        if site_settings.is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request, "site_settings":site_settings})
        else:
            news = db.query(models.SiteNews).filter_by(id=id).first()
            categories = db.query(models.EduCategory).all()
            news_category = db.query(models.NewsCategory).all()
            page_title = site_settings.site_title+" - "+news.news_title
            return templates.TemplateResponse("site/route/full_news.html", {"request": request,"news":news, "site_settings":site_settings,
                                                "page_title":page_title, "categories":categories, "news_category":news_category, "user":user, "current_user":current_user})


@main.get("/news/{name}")
def get_category(name: str, request: Request, db: Session = Depends(database.get_db), page: int = 1, page_size: int = 5):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    if access_token:
        current_user = verify_token(access_token)
        user = db.query(models.User).filter_by(id=current_user).first()
    else:
        current_user = ""
        user = ""
    #######     end    ##########
    if site_settings:
        if site_settings.is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request, "site_settings":site_settings})
        else:
            category = db.query(models.NewsCategory).filter_by(name=name).first()
            news_category = db.query(models.NewsCategory).all()
            news = db.query(models.SiteNews).filter_by(select_category_id=category.id).all()
            data_length = len(news)
            page_title = site_settings.site_title+" - "+category.name
            response = paginate.paginate(data=news, data_length=data_length,page=page, page_size=page_size)
            return templates.TemplateResponse("site/route/news-page.html", {"request": request, "category":category, "page_title":page_title,
                                                "response":response, "site_settings":site_settings, "news_category":news_category, "user":user, "current_user":current_user})


@main.get("/about")
def about_page(request: Request, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    if access_token:
        current_user = verify_token(access_token)
        user = db.query(models.User).filter_by(id=current_user).first()
    else:
        current_user = ""
        user = ""
    #######     end    ##########
    if site_settings:
        if site_settings.is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request, "site_settings":site_settings})
        else:
            categories = db.query(models.EduCategory).all()
            news_category = db.query(models.NewsCategory).all()
            staff = db.query(models.Staff).all()
            page_title = site_settings.site_title+" - Haqqımızda"
            return templates.TemplateResponse("site/route/about-page.html", {"request":request, "site_settings":site_settings, "user":user, "current_user":current_user,
                                                "page_title":page_title, "categories":categories,"news_category":news_category, "staff":staff})


@main.get("/contact")
def about_page(request: Request, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    if access_token:
        current_user = verify_token(access_token)
        user = db.query(models.User).filter_by(id=current_user).first()
    else:
        current_user = ""
        user = ""
    #######     end    ##########
    if site_settings:
        if site_settings.is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request, "site_settings":site_settings})
        else:
            categories = db.query(models.EduCategory).all()
            news_category = db.query(models.NewsCategory).all()
            page_title = site_settings.site_title+" - Əlaqə"
            ########## flash message
            _flash_message = ""
            if request.session.get("flash_messsage"):
                _flash_message = request.session.get("flash_messsage")
                request.session.pop("flash_messsage") if "flash_messsage" in request.session else []
            return templates.TemplateResponse("site/route/contactus-page.html", {"request":request, "site_settings":site_settings, "user":user, "current_user":current_user,
                                                "page_title":page_title, "categories":categories,"news_category":news_category, "flash":_flash_message})

@main.post("/contact")
async def send_message(request: Request, response: Response, db: Session = Depends(database.get_db)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    if access_token:
        current_user = verify_token(access_token)
        user = db.query(models.User).filter_by(id=current_user).first()
    else:
        current_user = ""
        user = ""
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
            request.session["flash_messsage"].append({"message": "Spam!!!", "category": "error"})
            response = RedirectResponse(url="/contact",status_code=HTTP_303_SEE_OTHER)
            return response
    if user:
        if len(message) == 0:
            request.session["flash_messsage"].append({"message": "Mesaj boş ola bilməz", "category": "error"})
            response = RedirectResponse(url="/contact",status_code=HTTP_303_SEE_OTHER)
            return response
        save_message = models.AdminMessages(sender_id=user.id, name=user.name_surname, email=user.email, message=message, created_at = datetime.now())
    else:
        if len(name) == 0 or  len(email) == 0 or len(message) == 0:
            request.session["flash_messsage"].append({"message": "Xanalar boş ola bilməz", "category": "error"})
            response = RedirectResponse(url="/contact",status_code=HTTP_303_SEE_OTHER)
            return response
        save_message = models.AdminMessages(name=name, email=email, message=message, created_at = datetime.now()) 
    db.add(save_message)
    db.commit()
    db.refresh(save_message)
    request.session["flash_messsage"].append({"message": "Mesajınız rəhbərliyə göndərildi", "category": "success"})
    response = RedirectResponse(url="/contact",status_code=HTTP_303_SEE_OTHER)
    response.set_cookie(key="time", value=current_time, httponly=True)
    return response