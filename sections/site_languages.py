from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from configurations import models, database
from sections import default_site_language
from sections.languages import english, russian
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from utils.helper import templates, check_user, default_variables, check_user_in_site


languages_panel = APIRouter(
    tags=['Dashboard / Languages Panel'],
)


@languages_panel.get("/languages")
def all_languages_page(request: Request, db: Session = Depends(database.get_db)):
    check = check_user(request)
    check_lang = check_user_in_site(request)
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            eng_lang = english
            ru_lang = russian
            az_lang = default_site_language
            check_ru = db.query(models.SiteLanguages).filter_by(lang_name=ru_lang.lang_name[0]).first()
            check_eng = db.query(models.SiteLanguages).filter_by(lang_name=eng_lang.lang_name[0]).first()
            check_az = db.query(models.SiteLanguages).filter_by(lang_name=az_lang.lang_name[0]).first()
            variables = default_variables(request)
            return templates.TemplateResponse("dashboard/site_languages.html",{"request":request, "languages":variables['languages_all'], "news_category":variables['news_category'],
                                                "counts":variables['counts'], "unread":variables['unread'], "count":len(variables['users']), "messages_time": variables['messages_time'],
                                                "user":check['user'], "flash":variables['_flash_message'], "site_language":check_lang['site_settings'].set_site_language,
                                                "check_eng":check_eng, "check_az":check_az, "check_ru":check_ru })
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@languages_panel.post("/language/install_language_pack/{lang_pack}")
async def install_language_pack(lang_pack:str, request: Request, db: Session = Depends(database.get_db)):
    check = check_user(request)
    az = default_site_language
    en = english
    ru = russian
    check_ru = db.query(models.SiteLanguages).filter_by(lang_name=ru.lang_name[0]).first()
    check_eng = db.query(models.SiteLanguages).filter_by(lang_name=en.lang_name[0]).first()
    check_az = db.query(models.SiteLanguages).filter_by(lang_name=az.lang_name[0]).first()
    request.session["flash_messsage"] = []
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            if lang_pack == "en":
                if check_eng:
                    request.session["flash_messsage"].append({"message": f"Bazada {en.lang_name[0]} paketi mövcuddur", "category": "error"})
                    request = RedirectResponse(url="/admin/languages/",status_code=HTTP_303_SEE_OTHER)
                    return request 
                else:
                    en.set_english_language()
                    request.session["flash_messsage"].append({"message": f"{en.lang_name[0]} yükləndi", "category": "success"})
                    request = RedirectResponse(url="/admin/languages/",status_code=HTTP_303_SEE_OTHER)
                    return request
            elif lang_pack == "az":
                if check_az:
                    request.session["flash_messsage"].append({"message": f"Bazada {az.lang_name[0]} paketi mövcuddur", "category": "error"})
                    request = RedirectResponse(url="/admin/languages/",status_code=HTTP_303_SEE_OTHER)
                    return request 
                else:
                    az.set_default_language()
                    request.session["flash_messsage"].append({"message": f"{az.lang_name[0]} yükləndi", "category": "success"})
                    request = RedirectResponse(url="/admin/languages/",status_code=HTTP_303_SEE_OTHER)
                    return request
            elif lang_pack == "ru":
                if check_ru:
                    request.session["flash_messsage"].append({"message": f"Bazada {ru.lang_name[0]} paketi mövcuddur", "category": "error"})
                    request = RedirectResponse(url="/admin/languages/",status_code=HTTP_303_SEE_OTHER)
                    return request 
                else:
                    ru.set_russian_language()
                    request.session["flash_messsage"].append({"message": f"{ru.lang_name[0]} yükləndi", "category": "success"})
                    request = RedirectResponse(url="/admin/languages/",status_code=HTTP_303_SEE_OTHER)
                    return request
            else:
                request.session["flash_messsage"].append({"message": "Belə funksiya mövcud deyil", "category": "error"})
                request = RedirectResponse(url="/admin/languages/",status_code=HTTP_303_SEE_OTHER)
                return request      
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@languages_panel.get("/languages/add-language")
def add_site_language(request:Request):
    check = check_user(request)
    default = default_site_language
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            variables = default_variables(request)
            return templates.TemplateResponse("/dashboard/add_site_language.html", {
                                                'request':request, "unread":variables['unread'], "site":variables['site'],
                                                "messages_time": variables['messages_time'], "user":check['user'], "flash":variables['_flash_message'],
                                                "default":default})


@languages_panel.post("/languages/add-language")
async def add_site_language_form(request:Request, db: Session = Depends(database.get_db)):
    check = check_user(request)
    lang = default_variables(request)['languages_all']
    request.session["flash_messsage"] = []
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            form = await request.form()
            
            for keys, inputs in form.items():
                if len(inputs) == 0:
                    request.session["flash_messsage"].append({"message": "Dil parametri boş ola bilməz!", "category": "error"})
                    request = RedirectResponse(url="/admin/languages/add-language",status_code=HTTP_303_SEE_OTHER)
                    return request

            for i in lang:
                if form.get('lang_name') == i.lang_name:
                    request.session["flash_messsage"].append({"message": f"Bazada {form.get('lang_name')} adlı dil var!", "category": "error"})
                    request = RedirectResponse(url="/admin/languages/add-language",status_code=HTTP_303_SEE_OTHER)
                    return request
                if form.get('short_lang_name') == i.short_lang_name:
                    request.session["flash_messsage"].append({"message": f"Bazada {form.get('short_lang_name')} adlı dil var!", "category": "error"})
                    request = RedirectResponse(url="/admin/languages/add-language",status_code=HTTP_303_SEE_OTHER)
                    return request

            add_new_language = models.SiteLanguages(
                                        lang_name=form.get('lang_name'),
                                        short_lang_name=form.get('short_lang_name'),
                                        site_about=form.get('site_about'),
                                        login_page_title=form.get('login_page_title'),
                                        user_logged_message=form.get('user_logged_message'),
                                        wrong_password_message=form.get('wrong_password_message'),
                                        user_does_not_exist_message=form.get('user_does_not_exist_message'),
                                        registration_page_title=form.get('registration_page_title'),
                                        correct_email_message=form.get('correct_email_message'),
                                        password_minimum_8_character_message=form.get('password_minimum_8_character_message'),
                                        name_not_added_message=form.get('name_not_added_message'),
                                        email_is_available_message=form.get('email_is_available_message'),
                                        registration_success=form.get('registration_success'),
                                        contact_page_title=form.get('contact_page_title'),
                                        message_spam_message=form.get('message_spam_message'),
                                        the_message_cannot_empty_message=form.get('the_message_cannot_empty_message'),
                                        boxes_are_cannot_empty=form.get('boxes_are_cannot_empty'),
                                        message_has_been_sent_to_management=form.get('message_has_been_sent_to_management'),
                                        educations_page_title=form.get('educations_page_title'),
                                        news_page_title=form.get('news_page_title'),
                                        user_profile_info_page_title=form.get('user_profile_info_page_title'),
                                        image_extension_error_message=form.get('image_extension_error_message'),
                                        profile_success_message=form.get('profile_success_message'),
                                        login=form.get('login'),
                                        why=form.get('why'),
                                        schedules=form.get('schedules'),
                                        week_days=form.get('week_days'),
                                        monday=form.get('monday'),
                                        tuesday=form.get('tuesday'),
                                        wednesday=form.get('wednesday'),
                                        thursday=form.get('thursday'),
                                        friday=form.get('friday'),
                                        saturday=form.get('saturday'),
                                        sunday=form.get('sunday'),
                                        our_staff=form.get('our_staff'),
                                        previous=form.get('previous'),
                                        next=form.get('next'),
                                        educations_all=form.get('educations_all'),
                                        detail=form.get('detail'),
                                        got_question_write_to_us_text=form.get('got_question_write_to_us_text'),
                                        address=form.get('address'),
                                        your_contact_number=form.get('your_contact_number'),
                                        email=form.get('email'),
                                        number_of_joined_students=form.get('number_of_joined_students'),
                                        view=form.get('view'),
                                        home=form.get('home'),
                                        education=form.get('education'),
                                        news=form.get('news'),
                                        about=form.get('about'),
                                        whatsapp_message=form.get('whatsapp_message'),
                                        call_us=form.get('call_us'),
                                        dashboard=form.get('dashboard'),
                                        profile=form.get('profile'),
                                        logout=form.get('logout'),
                                        categories=form.get('categories'),
                                        contact=form.get('contact'),
                                        created_at=form.get('created_at'),
                                        category=form.get('category'),
                                        password=form.get('password'),
                                        sign_in=form.get('sign_in'),
                                        register=form.get('register'),
                                        site_register=form.get('site_register'),
                                        logged_in=form.get('logged_in'),
                                        registered=form.get('registered'),
                                        name_and_surname=form.get('name_and_surname'),
                                        update_profile=form.get('update_profile'),
                                        city=form.get('city'),
                                        phone=form.get('phone'),
                                        date_of_birth=form.get('date_of_birth'),
                                        user_education=form.get('user_education'),
                                        certificate_grades_or_university=form.get('certificate_grades_or_university'),
                                        user_about=form.get('user_about'),
                                        registration_date=form.get('registration_date'),
                                        user_status=form.get('user_status'),
                                        education_of_choice=form.get('education_of_choice'),
                                        high_education=form.get('high_education'),
                                        secondary_education=form.get('secondary_education'),
                                        profile_picture=form.get('profile_picture'),
                                        change_photo=form.get('change_photo'),
                                        add_profile_picture=form.get('add_profile_picture'),
                                        save=form.get('save'),
                                        news_all=form.get('news_all'),
                                        last=form.get('last'),
                                        last_added=form.get('last_added'),
                                        video_tutorial=form.get('video_tutorial'),
                                        site_closed=form.get('site_closed'),
                                        site_closed_time=form.get('site_closed_time'),
                                        site_closed_text_reason=form.get('site_closed_text_reason'),
                                        forgot_password=form.get('forgot_password'),
                                        email_sent=form.get('email_sent'),
                                        email_is_not_registere=form.get('email_is_not_registere'),
                                        change_password=form.get('change_password'),
                                        password_not_same_confirm_password=form.get('password_not_same_confirm_password'),
                                        password_changed=form.get('password_changed'),
                                        forgot_password_question=form.get('forgot_password_question'),
                                        confirm_password=form.get('confirm_password'),
                                        send=form.get('send'),
                                        link_timed_out=form.get('link_timed_out'),
                                        visit_the_link_reset_password=form.get('visit_the_link_reset_password')
                                        )
            db.add(add_new_language)
            db.commit()
            db.refresh(add_new_language)
            request.session["flash_messsage"].append({"message": "Updated", "category": "success"})
            request = RedirectResponse(url="/admin/languages",status_code=HTTP_303_SEE_OTHER)
            return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@languages_panel.get("/languages/{id}")
def get_language_page(id:int, request:Request, db: Session = Depends(database.get_db)):
    check = check_user(request)
    default = default_site_language
    language = db.query(models.SiteLanguages).filter_by(id=id).first()
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            variables = default_variables(request)
            return templates.TemplateResponse("/dashboard/get_site_language.html", {
                                                'request':request, 'lang':language, "unread":variables['unread'], "site":variables['site'],
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
            
            for keys, inputs in form.items():
                if len(inputs) == 0:
                    request.session["flash_messsage"].append({"message": "Dil parametri boş ola bilməz!", "category": "error"})
                    request = RedirectResponse(url="/admin/",status_code=HTTP_303_SEE_OTHER)
                    return request

            language.update({
                    "site_about":form.get('site_about'), "login_page_title":form.get('login_page_title'),
                    "user_logged_message":form.get('user_logged_message'), "wrong_password_message":form.get('wrong_password_message'),
                    "user_does_not_exist_message":form.get('user_does_not_exist_message'),
                    "registration_page_title":form.get('registration_page_title'),
                    "correct_email_message":form.get('correct_email_message'),
                    "password_minimum_8_character_message":form.get('password_minimum_8_character_message'),
                    "name_not_added_message":form.get('name_not_added_message'),
                    "email_is_available_message":form.get('email_is_available_message'), 
                    "registration_success":form.get('registration_success'),
                    "contact_page_title":form.get('contact_page_title'), "login":form.get('login'),
                    "message_spam_message":form.get('message_spam_message'),
                    "the_message_cannot_empty_message":form.get('the_message_cannot_empty_message'),
                    "boxes_are_cannot_empty":form.get('boxes_are_cannot_empty'),
                    "message_has_been_sent_to_management":form.get('message_has_been_sent_to_management'),
                    "educations_page_title":form.get('educations_page_title'), 
                    "news_page_title":form.get('news_page_title'), "user_profile_info_page_title":form.get('user_profile_info_page_title'),
                    "image_extension_error_message":form.get('image_extension_error_message'),
                    "profile_success_message":form.get('profile_success_message'),
                    "why":form.get('why'), "schedules":form.get('schedules'),  "week_days":form.get('week_days'),
                    "monday":form.get('monday'), "tuesday":form.get('tuesday'), "wednesday":form.get('wednesday'),
                    "thursday":form.get('thursday'), "friday":form.get('friday'), "saturday":form.get('saturday'),
                    "sunday":form.get('sunday'), "our_staff":form.get('our_staff'), "previous":form.get('previous'),
                    "next":form.get('next'), "educations_all":form.get('educations_all'), "detail":form.get('detail'),
                    "got_question_write_to_us_text":form.get('got_question_write_to_us_text'), "address":form.get('address'),
                    "your_contact_number":form.get('your_contact_number'), "email":form.get('email'),
                    "number_of_joined_students":form.get('number_of_joined_students'), "view":form.get('view'), 
                    "home":form.get('home'), "education":form.get('education'), "news":form.get('news'), 
                    "about":form.get('about'), "whatsapp_message":form.get('whatsapp_message'), "call_us":form.get('call_us'), 
                    "dashboard":form.get('dashboard'), "profile":form.get('profile'), "logout":form.get('logout'), 
                    "categories":form.get('categories'), "contact":form.get('contact'), "created_at":form.get('created_at'), 
                    "category":form.get('category'), "password":form.get('password'), "sign_in":form.get('sign_in'), 
                    "register":form.get('register'), "site_register":form.get('site_register'), "logged_in":form.get('logged_in'), 
                    "registered":form.get('registered'), "name_and_surname":form.get('name_and_surname'),
                    "update_profile":form.get('update_profile'), "city":form.get('city'), "phone":form.get('phone'),
                    "date_of_birth":form.get('date_of_birth'), "user_education":form.get('user_education'),
                    "certificate_grades_or_university":form.get('certificate_grades_or_university'),
                    "user_about":form.get('user_about'), "registration_date":form.get('registration_date'),
                    "user_status":form.get('user_status'), "education_of_choice":form.get('education_of_choice'),
                    "high_education":form.get('high_education'), "secondary_education":form.get('secondary_education'),
                    "profile_picture":form.get('profile_picture'), "change_photo":form.get('change_photo'),
                    "add_profile_picture":form.get('add_profile_picture'), "save":form.get('save'),
                    "news_all":form.get('news_all'), "last":form.get('last'), "last_added":form.get('last_added'),
                    "video_tutorial":form.get('video_tutorial'), "site_closed":form.get('site_closed'),
                    "site_closed_time":form.get('site_closed_time'), "site_closed_text_reason":form.get('site_closed_text_reason'),
                    "forgot_password":form.get('forgot_password'), "email_sent":form.get('email_sent'),
                    "email_is_not_registere":form.get('email_is_not_registere'), "change_password":form.get('change_password'),
                    "password_not_same_confirm_password":form.get('password_not_same_confirm_password'),
                    "password_changed":form.get('password_changed'), "forgot_password_question":form.get('forgot_password_question'),
                    "confirm_password":form.get('confirm_password'), "send":form.get('send'), "link_timed_out":form.get('link_timed_out'),
                    'visit_the_link_reset_password':form.get('visit_the_link_reset_password')
                    })
            
            db.commit()
            request.session["flash_messsage"].append({"message": "Updated", "category": "success"})
            request = RedirectResponse(url="/admin/languages",status_code=HTTP_303_SEE_OTHER)
            return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@languages_panel.get("/language/{id}/delete")
def delete_site_language(id: int, request: Request, db: Session = Depends(database.get_db)):
    check = check_user(request)
    check_default = check_user_in_site(request)['site_settings'].set_site_language
    delete_option = db.query(models.SiteLanguages).filter_by(id=id)
    request.session["flash_messsage"] = []
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            if delete_option.first():
                name = delete_option.first().lang_name
                
                if delete_option.first().id == check_default:
                    request.session["flash_messsage"].append({"message": f"{name} saytın əsas dilidi, silinə bilməz", "category": "error"})
                    request = RedirectResponse(url="/admin/languages",status_code=HTTP_303_SEE_OTHER)
                    return request
                delete_option.delete()
                db.commit()
                request.session["flash_messsage"].append({"message": f"{name} silindi", "category": "success"})
                request = RedirectResponse(url="/admin/languages",status_code=HTTP_303_SEE_OTHER)
                return request
            else:
                request.session["flash_messsage"].append({"message": "Mövcud deyil", "category": "error"})
                request = RedirectResponse(url="/admin/languages",status_code=HTTP_303_SEE_OTHER)
                return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)