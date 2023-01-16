from starlette.templating import Jinja2Templates
from starlette.status import HTTP_303_SEE_OTHER
from configurations.token import verify_token
from fastapi import Request, Depends, Response
from sqlalchemy.orm import Session
import configurations.models as models, configurations.database as database
from datetime import datetime, timedelta
from utils import paginate, time_calculate

def closed(request, site_settings):
    return templates.TemplateResponse("site/closed.html", {"request":request, "site_settings":site_settings})

templates = Jinja2Templates(directory="templates")


def check_user(request: Request, db: Session = database.get_db()):
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    if current_user:
        user = db.query(models.User).filter_by(id=current_user).first()
    else:
        user = ""
    us = {
        'access_token':access_token,
        'current_user':current_user,
        'user':user
    }
    return us

def check_user_in_site(request: Request, db: Session = database.get_db()):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    access_token = request.cookies.get("access_token")
    if access_token:
        current_user = verify_token(access_token)
        user = db.query(models.User).filter_by(id=current_user).first()
    else:
        current_user = ""
        user = ""
    us = {
        'site_settings':site_settings,
        'access_token':access_token,
        'current_user':current_user,
        'user':user
    }
    return us


def flash_message(request: Request):
    _flash_message = ""
    if request.session.get("flash_messsage"):
        _flash_message = request.session.get("flash_messsage")
        request.session.pop("flash_messsage") if "flash_messsage" in request.session else []
    return _flash_message


def default_variables(request: Request, db: Session = database.get_db()):
    messages_data = db.query(models.AdminMessages).order_by(models.AdminMessages.created_at.desc()).all()
    unread_messages_data = db.query(models.AdminMessages).filter_by(readed=0).order_by(models.AdminMessages.created_at.desc()).all()
    unread = db.query(models.AdminMessages).filter_by(readed=0).all()
    user_admin = db.query(models.User).filter_by(admin_user = True).all()
    users = db.query(models.User).all()
    education = db.query(models.Education).all()
    education_category = db.query(models.EduCategory).all()
    site_news = db.query(models.SiteNews).all()
    news_category = db.query(models.NewsCategory).all()
    staff = db.query(models.Staff).all()
    site = db.query(models.SiteSettings).first()
    sliders = db.query(models.SliderSettings).all()
    counts = return_count()
    messages_time = time_calculate.messages_time()
    _flash_message = flash_message(request)
    variables = {
        'unread':unread,
        'users':users,
        'staff':staff,
        'site':site,
        'messages_data':messages_data,
        'unread_messages_data':unread_messages_data,
        'site_news':site_news,
        'news_category':news_category,
        'sliders':sliders,
        'user_admin':user_admin,
        'education':education,
        'education_category':education_category,
        'counts':counts,
        'messages_time':messages_time,
        '_flash_message':_flash_message
    }
    return variables


def site_default_variables(request: Request, db: Session = database.get_db()):
    _flash_message = flash_message(request)
    slider = db.query(models.SliderSettings).all()
    educations = db.query(models.Education).all()
    categories = db.query(models.EduCategory).all()
    news = db.query(models.SiteNews).all()
    staff = db.query(models.Staff).all()
    news_category = db.query(models.NewsCategory).all()
    variables = {
        '_flash_message':_flash_message,
        'slider':slider,
        'educations':educations,
        'categories':categories,
        'news':news,
        'news_category':news_category,
        'staff':staff
    }
    return variables


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

    counts = {
        "users_one_day_count":users_one_day_count,
        "users_week_count":users_week_count,
        "users_month_count":users_month_count,
        "difference_one_day":difference_one_day,
        "difference_week":difference_week,
        "difference_month":difference_month
        }
    return counts