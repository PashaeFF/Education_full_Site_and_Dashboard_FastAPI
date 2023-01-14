from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
import models, database, time_calculate
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from utils.helper import templates
from configurations.token import verify_token


settings_panel = APIRouter(
    tags=['Dashboard / Settings'],
)

@settings_panel.get("/settings")
def site_settings(request: Request, db:Session = Depends(database.get_db)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    if user:
        if user.admin_user == True or user.super_user == True:
            unread = db.query(models.AdminMessages).filter_by(readed=0).all()
            site = db.query(models.SiteSettings).first()
            #mesajin gelme zamanini hesablayir
            messages_time = time_calculate.messages_time()
            ########## flash message
            _flash_message = ""
            if request.session.get("flash_messsage"):
                _flash_message = request.session.get("flash_messsage")
                request.session.pop("flash_messsage") if "flash_messsage" in request.session else []
            return templates.TemplateResponse("dashboard/site_settings.html",{"request":request, "unread":unread, "site":site, "messages_time": messages_time
                                                                            , "user":user, "flash":_flash_message})
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@settings_panel.post("/settings")
async def post_site_settings(request: Request, db:Session = Depends(database.get_db)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    if user:
        if user.admin_user == True or user.super_user == True:
            site = db.query(models.SiteSettings).filter_by(id=1)
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
            if is_active:
                if is_active == "on":
                    is_active = True
                elif is_active is None:
                    is_active = False
            site.update({"site_title":site_title, "site_logo":site_logo, "site_slogan":site_slogan, "site_description":site_description, "site_about":site_about, 
                        "wp_number":wp_number, "site_email":site_email, "about_teams":about_teams, "phone":phone, "wp_text":wp_text, "google_map":google_map,
                        "youtube_video":youtube_video, "facebook":facebook, "instagram":instagram, "linkedin":linkedin, "is_active":is_active,
                        "address":address, "monday":monday, "thursday":thursday, "wednesday":wednesday, "thursday":thursday, "friday":friday,
                        "saturday":saturday, "sunday":sunday },synchronize_session=False)
            db.commit()
            request.session["flash_messsage"] = []
            request.session["flash_messsage"].append({"message": "Updated", "category": "success"})
            request = RedirectResponse(url="/admin/settings",status_code=HTTP_303_SEE_OTHER)
            return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
