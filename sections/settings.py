from fastapi import APIRouter, Request, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import and_
import models, database, time_calculate
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from utils.helper import templates, flash, get_flashed_messages


settings_panel = APIRouter(
    tags=['Dashboard / Settings'],
)

@settings_panel.get("/settings")
def site_settings(request: Request, db:Session = Depends(database.get_db)):
    unread = db.query(models.AdminMessages).filter_by(readed=0).all()
    site = db.query(models.SiteSettings).first()

    #mesajin gelme zamanini hesablayir
    messages_time = time_calculate.messages_time()

    return templates.TemplateResponse("dashboard/site_settings.html",{"request":request, "unread":unread, "site":site, "messages_time": messages_time})

@settings_panel.post("/settings")
async def post_site_settings(request: Request, db:Session = Depends(database.get_db)):
    site = db.query(models.SiteSettings).first()
    form = await request.form()
    site_title = form.get("site_title")
    site_logo = form.get("site_logo")
    site_slogan = form.get("site_slogan")
    site_description = form.get("site_description")
    site_about = form.get("site_about")
    about_teams = form.get("about_teams")
    site_email = form.get("site_email")
    phone = form.get("phone")
    wp_number = form.get("wp_number")
    wp_text = form.get("wp_text")
    phone = form.get("phone")
    address = form.get("address")
    google_map = form.get("google_map")

    youtube_video = form.get("youtube_video")
    facebook = form.get("facebook")
    instagram = form.get("instagram")
    linkedin = form.get("linkedin")
    is_active = form.get("is_active")

    monday = form.get("monday")
    tuesday = form.get("thursday")
    wednesday = form.get("wednesday")
    thursday = form.get("thursday")
    friday = form.get("friday")
    saturday = form.get("saturday")
    sunday = form.get("sunday")
    site = db.query(models.SiteSettings)
    if is_active:
        if is_active == "on":
            is_active = True
        elif is_active is None:
            is_active = False
    if site is None:
        add_site_settings = models.SiteSettings(site_title=site_title, site_logo=site_logo, site_slogan=site_slogan, site_description=site_description,
                                                site_about=site_about, about_teams=about_teams, site_email=site_email, phone=phone, address=address,
                                                google_map=google_map, wp_number=wp_number, wp_text=wp_text, facebook=facebook, instagram=instagram, linkedin=linkedin, 
                                                is_active=is_active, monday=monday, tuesday=tuesday, wednesday=wednesday, thursday=thursday,
                                                friday=friday, saturday=saturday, sunday=sunday)
        db.add(add_site_settings)
        db.commit()
        db.refresh(add_site_settings)
        flash(request,"Updated", "success")
        return templates.TemplateResponse("dashboard/site_settings.html",{"request":request})
    else:
        
        site.update({"site_title":site_title, "site_logo":site_logo, "site_slogan":site_slogan, "site_description":site_description, "site_about":site_about, 
                    "wp_number":wp_number, "site_email":site_email, "about_teams":about_teams, "phone":phone, "wp_text":wp_text, "google_map":google_map,
                    "youtube_video":youtube_video, "facebook":facebook, "instagram":instagram, "linkedin":linkedin, "is_active":is_active,
                    "address":address, "monday":monday, "thursday":thursday, "wednesday":wednesday, "thursday":thursday, "friday":friday,
                    "saturday":saturday, "sunday":sunday },synchronize_session=False)
        db.commit()
        flash(request,"Updated", "success")
        return RedirectResponse(url="/admin/settings",status_code=HTTP_303_SEE_OTHER)
