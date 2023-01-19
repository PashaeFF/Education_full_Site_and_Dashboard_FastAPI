from fastapi import APIRouter, Request, Depends, UploadFile
from typing import Optional
from PIL import Image
from sqlalchemy.orm import Session
from configurations import models, database
from sections import default_site_language
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from utils.helper import templates, check_user, default_variables


languages_panel = APIRouter(
    tags=['Dashboard / Languages Panel'],
)

@languages_panel.get("/languages/{id}")
def get_language_page(id:int, request:Request, db: Session = Depends(database.get_db)):
    check = check_user(request)
    default = default_site_language
    language = db.query(models.SiteLanguages).filter_by(id=id).first()
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            variables = default_variables(request)
            return templates.TemplateResponse("/dashboard/get_site_languages.html", {
                                                'request':request, 'lang':language,"unread":variables['unread'], "site":variables['site'],
                                                "messages_time": variables['messages_time'], "user":check['user'], "flash":variables['_flash_message'],
                                                "default":default})

@languages_panel.post("/languages/{id}")
async def change_site_language(id:int, request:Request, db: Session = Depends(database.get_db)):
    check = check_user(request)
    language = db.query(models.SiteLanguages).filter_by(id=id)
    request.session["flash_messsage"] = []
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            form = await request.form()
            site_about = form.get("site_about")
            login_page_title = form.get("login_page_title")
            user_logged_message = form.get("user_logged_message")
            wrong_password_message = form.get("wrong_password_message")
            user_does_not_exist_message = form.get("user_does_not_exist_message")
            registration_page_title = form.get("registration_page_title")
            correct_email_message = form.get("correct_email_message")
            password_minimum_8_character_message = form.get("password_minimum_8_character_message")
            name_not_added_message = form.get("name_not_added_message")
            email_is_available_message = form.get("email_is_available_message")
            registration_success = form.get("registration_success")
            contact_page_title = form.get("contact_page_title")
            message_spam_message = form.get("message_spam_message")
            the_message_cannot_empty_message = form.get("the_message_cannot_empty_message")
            boxes_are_cannot_empty = form.get("boxes_are_cannot_empty")
            message_has_been_sent_to_management = form.get("message_has_been_sent_to_management")
            educations_page_title = form.get("educations_page_title")
            news_page_title = form.get("news_page_title")
            user_profile_info_page_title = form.get("user_profile_info_page_title")
            image_extension_error_message = form.get("image_extension_error_message")
            profile_success_message = form.get("profile_success_message")
            why = form.get("why")
            schedules = form.get("schedules")
            week_days = form.get("week_days")
            monday = form.get("monday")
            tuesday = form.get("tuesday")
            wednesday = form.get("wednesday")
            thursday = form.get("thursday")
            friday = form.get("friday")
            saturday = form.get("saturday")
            sunday = form.get("sunday")
            our_staff = form.get("our_staff")
            previous = form.get("previous")
            next = form.get("next")
            educations_all = form.get("educations_all")
            detail = form.get("detail")
            got_question_write_to_us_text = form.get("got_question_write_to_us_text")
            address = form.get("address")
            your_contact_number = form.get("your_contact_number")
            email = form.get("email")
            number_of_joined_students = form.get("number_of_joined_students")
            view = form.get("view")
            home = form.get("home")
            education = form.get("education")
            news = form.get("news")
            about = form.get("about")
            whatsapp_message = form.get("whatsapp_message")
            call_us = form.get("call_us")
            dashboard = form.get("dashboard")
            profile = form.get("profile")
            logout = form.get("logout")
            categories = form.get("categories")
            contact = form.get("contact")
            created_at = form.get("created_at")
            category = form.get("category")
            password = form.get("password")
            sign_in = form.get("sign_in")
            register = form.get("register")
            site_register = form.get("site_register")
            logged_in = form.get("logged_in")
            registered = form.get("registered")
            name_and_surname = form.get("name_and_surname")
            update_profile = form.get("update_profile")
            city = form.get("city")
            phone = form.get("phone")
            date_of_birth = form.get("date_of_birth")
            user_education = form.get("user_education")
            certificate_grades_or_university = form.get("certificate_grades_or_university")
            user_about = form.get("user_about")
            registration_date = form.get("registration_date")
            user_status = form.get("user_status")
            education_of_choice = form.get("education_of_choice")
            high_education = form.get("high_education")
            secondary_education = form.get("secondary_education")
            profile_picture = form.get("profile_picture")
            change_photo = form.get("change_photo")
            add_profile_picture = form.get("add_profile_picture")
            save = form.get("save")
            news_all = form.get("news_all")
            last = form.get("last")
            last_added = form.get("last_added")
            video_tutorial = form.get("video_tutorial")
            site_closed = form.get("site_closed")
            site_closed_time = form.get("site_closed_time")
            site_closed_text_reason = form.get("site_closed_text_reason")

            is_active = form.get("is_active")
            lang_name = form.get("lang_name")
            short_lang_name = form.get("short_lang_name")
            for k,i in form.items():
                if k == is_active:
                    continue
                else:
                    if len(i) == 0:
                        request.session["flash_messsage"].append({"message": "Dil parametri boş ola bilməz!", "category": "error"})
                        request = RedirectResponse(url="/admin/",status_code=HTTP_303_SEE_OTHER)
                        return request
            if is_active:
                if is_active == "on":
                    is_active = True
                elif is_active is None:
                    is_active = False

            # language.update({
            #         "lang_name":lang_name, "short_lang_name":short_lang_name, "is_active":is_active, "site_about":site_about,
            #         "login_page_title":login_page_title, "user_logged_message":user_logged_message,
            #         "wrong_password_message":wrong_password_message, "user_does_not_exist_message":user_does_not_exist_message,
            #         "registration_page_title":registration_page_title, "correct_email_message":correct_email_message,
            #         "password_minimum_8_character_message":password_minimum_8_character_message, "name_not_added_message":name_not_added_message,
            #         "email_is_available_message":email_is_available_message, "registration_success":registration_success,
            #         "contact_page_title":contact_page_title, "message_spam_message":message_spam_message,
            #         "the_message_cannot_empty_message":the_message_cannot_empty_message, "boxes_are_cannot_empty":boxes_are_cannot_empty,
            #         "message_has_been_sent_to_management":message_has_been_sent_to_management, "educations_page_title":educations_page_title,
            #         "news_page_title":news_page_title, "user_profile_info_page_title":user_profile_info_page_title,
            #         "image_extension_error_message":image_extension_error_message, "profile_success_message":profile_success_message,
            #         "why":why, "schedules":schedules, "week_days":week_days, "monday":monday, "tuesday":tuesday, "wednesday":wednesday,
            #         "thursday":thursday, "friday":friday, "saturday":saturday, "sunday":sunday, "our_staff":our_staff, "previous":previous,
            #         "next":next, "educations_all":educations_all, "detail":detail, "got_question_write_to_us_text":got_question_write_to_us_text,
            #         "address":address, "your_contact_number":your_contact_number, "email":email, "number_of_joined_students":number_of_joined_students,
            #         "view":view, "home":home, "education":education, "news":news, "about":about, "whatsapp_message":whatsapp_message,
            #         "call_us":call_us, "dashboard":dashboard, "profile":profile, "logout":logout, "categories":categories, "contact":contact,
            #         "created_at":created_at, "category":category, "password":password, "sign_in":sign_in, "register":register, "site_register":site_register,
            #         "logged_in":logged_in, "registered":registered, "name_and_surname":name_and_surname, "update_profile":update_profile, "city":city,
            #         "phone":phone, "date_of_birth":date_of_birth, "user_education":user_education, "certificate_grades_or_university":certificate_grades_or_university,
            #         "user_about":user_about, "registration_date":registration_date, "user_status":user_status, "education_of_choice":education_of_choice,
            #         "high_education":high_education, "secondary_education":secondary_education, "profile_picture":profile_picture, "change_photo":change_photo,
            #         "add_profile_picture":add_profile_picture, "save":save, "news_all":news_all, "last":last, "last_added":last_added,
            #         "video_tutorial":video_tutorial, "site_closed":site_closed, "site_closed_time":site_closed_time, "site_closed_text_reason":site_closed_text_reason
            #         })

            # language.update({
            #             "site_about":form.get['site_about'],
            #             "login_page_title":form.get['login_page_title'],
            #             "user_logged_message":form.get['user_logged_message'],
            #             "wrong_password_message":form.get['wrong_password_message'],
            #             "user_does_not_exist_message":form.get['user_does_not_exist_message'],
            #             "registration_page_title":form.get['registration_page_title'],
            #             "correct_email_message":form.get['correct_email_message'],
            #             "password_minimum_8_character_message":form.get['password_minimum_8_character_message'],
            #             "name_not_added_message":form.get['name_not_added_message'],
            #             "email_is_available_message":form.get['email_is_available_message'], 
            #             "registration_success":form.get['registration_success'],
            #             "contact_page_title":form.get['contact_page_title'], 
            #             "message_spam_message":form.get['message_spam_message'],
            #             "the_message_cannot_empty_message":form.get['the_message_cannot_empty_message'],
            #             "boxes_are_cannot_empty":form.get['boxes_are_cannot_empty'],
            #             "message_has_been_sent_to_management":form.get['message_has_been_sent_to_management'],
            #             "educations_page_title":form.get['educations_page_title'], 
            #             "news_page_title":form.get['news_page_title'],
            #             "user_profile_info_page_title":form.get['user_profile_info_page_title'],
            #             "image_extension_error_message":form.get['image_extension_error_message'],
            #             "profile_success_message":form.get['profile_success_message'],
            #             "why":form.get['why'], 
            #             "schedules":form.get['schedules'], 
            #             "week_days":form.get['week_days'],
            #             "monday":form.get['monday'], 
            #             "tuesday":form.get['tuesday'], 
            #             "wednesday":form.get['wednesday'],
            #             "thursday":form.get['thursday'], 
            #             "friday":form.get['friday'], 
            #             "saturday":form.get['saturday'],
            #             "sunday":form.get['sunday'], 
            #             "our_staff":form.get['our_staff'], 
            #             "previous":form.get['previous'],
            #             "next":form.get['next'], 
            #             "educations_all":form.get['educations_all'], 
            #             "detail":form.get['detail'],
            #             "got_question_write_to_us_text":form.get['got_question_write_to_us_text'], 
            #             "address":form.get['address'],
            #             "your_contact_number":form.get['your_contact_number'], 
            #             "email":form.get['email'],
            #             "number_of_joined_students":form.get['number_of_joined_students'],
            #             "view":form.get['view'], 
            #             "home":form.get['home'], 
            #             "education":form.get['education'],
            #             "news":form.get['news'], 
            #             "about":form.get['about'], 
            #             "whatsapp_message":form.get['whatsapp_message'],
            #             "call_us":form.get['call_us'], 
            #             "dashboard":form.get['dashboard'], 
            #             "profile":form.get['profile'],
            #             "logout":form.get['logout'], 
            #             "categories":form.get['categories'], 
            #             "contact":form.get['contact'],
            #             "created_at":form.get['created_at'], 
            #             "category":form.get['category'], 
            #             "password":form.get['password'],
            #             "sign_in":form.get['sign_in'], 
            #             "register":form.get['register'], 
            #             "site_register":form.get['site_register'],
            #             "logged_in":form.get['logged_in'], 
            #             "registered":form.get['registered'], 
            #             "name_and_surname":form.get['name_and_surname'],
            #             "update_profile":form.get['update_profile'], 
            #             "city":form.get['city'], 
            #             "phone":form.get['phone'],
            #             "date_of_birth":form.get['date_of_birth'], 
            #             "user_education":form.get['user_education'],
            #             "certificate_grades_or_university":form.get['certificate_grades_or_university'],
            #             "user_about":form.get['user_about'], 
            #             "registration_date":form.get['registration_date'],
            #             "user_status":form.get['user_status'], 
            #             "education_of_choice":form.get['education_of_choice'],
            #             "high_education":form.get['high_education'],
            #             "secondary_education":form.get['secondary_education'],
            #             "profile_picture":form.get['profile_picture'],
            #             "change_photo":form.get['change_photo'],
            #             "add_profile_picture":form.get['add_profile_picture'],
            #             "save":form.get['save'],
            #             "news_all":form.get['news_all'],
            #             "last":form.get['last'], "last_added":form.get['last_added'],
            #             "video_tutorial":form.get['video_tutorial'],
            #             "site_closed":form.get['site_closed'],
            #             "site_closed_time":form.get['site_closed_time'],
            #             "site_closed_text_reason":form.get['site_closed_text_reason']
            #             })
            db.commit()
            request.session["flash_messsage"].append({"message": "Updated", "category": "success"})
            request = RedirectResponse(url="/admin/",status_code=HTTP_303_SEE_OTHER)
            return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)