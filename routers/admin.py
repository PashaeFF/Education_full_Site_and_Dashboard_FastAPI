from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import models, database, paginate, time_calculate
from starlette.status import HTTP_303_SEE_OTHER
from datetime import datetime, timedelta
from sections import education_dashboard, users, slider, settings, news, staff, messages
from utils.helper import templates

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

@dashboard.get("/", response_class=HTMLResponse)
@dashboard.get("/users")
async def index(request: Request, db: Session = Depends(database.get_db), page: int = 1, page_size: int = 10):
    unread = db.query(models.AdminMessages).filter_by(readed=0).all()
    users = db.query(models.User).all()
    counts = return_count()
    data_length = len(users)
    messages_time = time_calculate.messages_time()
    response = paginate.paginate(data=users, data_length=data_length,page=page, page_size=page_size)
    return templates.TemplateResponse("dashboard/index.html", {"request": request, "response": response, "count": len(users),
                                                                "messages_time":messages_time, "counts":counts, "unread": unread } )


dashboard.include_router(users.users_panel)
dashboard.include_router(slider.slider_panel)
dashboard.include_router(settings.settings_panel)
dashboard.include_router(education_dashboard.education_panel)
dashboard.include_router(news.news_panel)
dashboard.include_router(staff.staff_panel)
dashboard.include_router(messages.messages_panel)