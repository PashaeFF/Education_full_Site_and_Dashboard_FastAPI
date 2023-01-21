from sqlalchemy.orm import Session
from configurations import database, models

lang_name = 'Azərbaycan dili',
short_lang_name = 'AZ',
#/routers/site.py
site_about = 'Haqqımızda'
#/site_sections/auth.py  - '/login'
login_page_title = 'İstifadəçi girişi'
user_logged_message = 'Daxil oldunuz'
login = 'Daxil ol'
wrong_password_message = 'Parol səhvdir'
user_does_not_exist_message = 'İstifadəçi mövcud deyil'
####################### - '/registration'
registration_page_title = 'Qeydiyyat'
correct_email_message = 'Emaili düzgün qeyd edin'
password_minimum_8_character_message = 'Parol minimum 8 simvol olmalıdır'
name_not_added_message = 'Ad əlavə etməmisiniz'
email_is_available_message = 'Email mövcuddur'
registration_success = 'Daxil oldunuz'
#/site_sections/contact.py - '/contact'
contact_page_title = 'Əlaqə'
message_spam_message = 'Spam!!!'
the_message_cannot_empty_message = 'Mesaj boş ola bilməz'
boxes_are_cannot_empty = 'Xanalar boş ola bilməz'
message_has_been_sent_to_management = 'Mesajınız rəhbərliyə göndərildi'
#/site_sections/educations.py - '/educations'
educations_page_title = 'Təhsil'
#/site_sections/news.py '/news'
news_page_title = 'Xəbərlər'
#/site_sections/users.py  - '/profile/{id}'
user_profile_info_page_title = 'Profil məlumatları'
image_extension_error_message = 'Yalnız JPG, PNG, JPEG'
profile_success_message = 'Profil tamamlandı'
####################### HTML TEMPLATES LANGUAGE ########################
#/templates/site/route/about-page.html
why = 'Niyə'
schedules = 'İş saatlarımız'
week_days = 'Həftənin günləri'
monday = 'B.e.'
tuesday = 'Ç.a.'
wednesday = 'Ç.'
thursday = 'C.a.'
friday = 'C.'
saturday = 'Ş.'
sunday = 'B.'
our_staff = 'Bizim Komanda'
previous = 'Geri'
next = 'Irəli'
#/templates/site/route/all_educations.html
educations_all = 'Ümumi'
detail = 'Ətraflı'
#/templates/site/route/contactus-page.html
got_question_write_to_us_text = 'Sualınız var?? Bizə yazın, cavablayaq'
address = 'Adres'
your_contact_number = 'Əlaqə nömrəniz'
email = 'Email'
#/templates/site/route/aducation_details.html
number_of_joined_students = 'Qoşulan Tələbə sayı'
#/templates/site/route/aducation-page.html 
view = 'Bax'
#/templates/site/route/footer.html & topnav.html
home = 'Əsas səhifə'
education = 'Təhsil'
news = 'Xəbərlər'
about = 'Haqqımızda'
whatsapp_message = 'Whatsapp mesaj'
call_us = 'Bizə zəng'
dashboard = 'İdarə paneli'
profile = 'Profil'
logout = 'Çıxış'
categories = 'Kateqoriyalar'
contact = 'Əlaqə'
#/templates/site/route/full_news.html
created_at = 'Əlavə olunma vaxtı'
category = 'Kateqoriya'
#/templates/site/route/login.html & register.html
password = 'Parol'
sign_in = 'Daxil ol'
register = 'Qeyd ol'
site_register = 'Qeydiyyat'
logged_in = 'Daxil olmusunuz...'
registered = 'Qeydiyyatlısınız...'
name_and_surname = 'Adınız və soyadınız'
#/templates/site/route/profile.html
update_profile = 'Profili Düzəlt'
city = 'Şəhər'
phone = 'Əlaqə nömrəsi'
date_of_birth = 'Doğum tarixi'
user_education = 'Təhsil'
certificate_grades_or_university = 'Attestat qiymətləri vəya Universitet Diplomu'
user_about = 'Haqqında'
registration_date = 'Qeydiyyat tarixi'
user_status = 'Status'
education_of_choice = 'Seçdiyi Təhsil'
high_education = 'Ali təhsil'
secondary_education = 'Orta təhsil'
profile_picture = 'Profil fotosu'
change_photo = 'Fotonu dəyiş'
add_profile_picture = 'Foto elave et'
save = 'Yadda saxla'
#/templates/site/route/short_news.html
news_all = 'Bütün xəbərlər'
last = 'Son'
#/templates/site/route/slider_welcome.html
last_added = 'Son əlavə olunanlar'
#/templates/site/route/video_test.html
video_tutorial = 'Video Təlimat'
#/templates/site/route/closed.html
site_closed = 'sayt Bağlıdır'
site_closed_time = 'keçici olaraq'
site_closed_text_reason = 'Yenilənməyə görə'
#lost password
#token.py
link_timed_out = 'Linkin vaxtı bitib'
visit_the_link_reset_password = '10 dəqiqə ərzində parolu sıfırlamaq üçün linkə daxil olun'
#auth.py
#/forgot-password
forgot_password = 'Parol bərpası'
#/forgot-password
email_sent = 'Email göndərildi'
email_is_not_registere = 'Bu email qeydiyyatlı deyil'
#/change-password
change_password = 'Parolunu dəyiş'
password_not_same_confirm_password = 'Parol və parolun təsdiqi eyni deyil'
password_changed = 'Parolunuzu dəyişdiniz'
#login.html
forgot_password_question = 'Parolu unutmusan?'
#reset-password.html
confirm_password = 'Parolun təsdiqi'
send = 'Göndər'
#user.py
max_4_file = 'Maksimum 4 fayl yükləyə bilərsiniz'
profile_info = 'Profil məlumatları'
deleted = 'Hamısı silindi'
files_uploaded = 'Fayllar yükləndi'
file_upload = 'Fayl yüklənməsi'
#auth.py
deactive_user_message = 'İstifadəçi deaktivdir'
#profile.html
student_files = 'Tələbə faylları'
delete_all = 'Hamısını sil'
add = 'Əlavə et'
#upload_files.html
add_max_4_file = 'Fayl əlavə et(Maksimum 4 ədəd)'
there_are_no_files = 'Heç bir fayl yoxdur'


def set_default_language(db: Session = database.get_db()):
    default_site_language = models.SiteLanguages(
                                        lang_name = lang_name,
                                        short_lang_name = short_lang_name,
                                        site_about=site_about,
                                        login_page_title=login_page_title,
                                        user_logged_message=user_logged_message,
                                        wrong_password_message=wrong_password_message,
                                        user_does_not_exist_message=user_does_not_exist_message,
                                        registration_page_title=registration_page_title,
                                        correct_email_message=correct_email_message,
                                        password_minimum_8_character_message=password_minimum_8_character_message,
                                        name_not_added_message=name_not_added_message,
                                        email_is_available_message=email_is_available_message,
                                        registration_success=registration_success,
                                        contact_page_title=contact_page_title,
                                        message_spam_message=message_spam_message,
                                        the_message_cannot_empty_message=the_message_cannot_empty_message,
                                        boxes_are_cannot_empty=boxes_are_cannot_empty,
                                        message_has_been_sent_to_management=message_has_been_sent_to_management,
                                        educations_page_title=educations_page_title,
                                        news_page_title=news_page_title,
                                        user_profile_info_page_title=user_profile_info_page_title,
                                        image_extension_error_message=image_extension_error_message,
                                        profile_success_message=profile_success_message,
                                        login=login,
                                        why=why,
                                        schedules=schedules,
                                        week_days=week_days,
                                        monday=monday,
                                        tuesday=tuesday,
                                        wednesday=wednesday,
                                        thursday=thursday,
                                        friday=friday,
                                        saturday=saturday,
                                        sunday=sunday,
                                        our_staff=our_staff,
                                        previous=previous,
                                        next=next,
                                        educations_all=educations_all,
                                        detail=detail,
                                        got_question_write_to_us_text=got_question_write_to_us_text,
                                        address=address,
                                        your_contact_number=your_contact_number,
                                        email=email,
                                        number_of_joined_students=number_of_joined_students,
                                        view=view,
                                        home=home,
                                        education=education,
                                        news=news,
                                        about=about,
                                        whatsapp_message=whatsapp_message,
                                        call_us=call_us,
                                        dashboard=dashboard,
                                        profile=profile,
                                        logout=logout,
                                        categories=categories,
                                        contact=contact,
                                        created_at=created_at,
                                        category=category,
                                        password=password,
                                        sign_in=sign_in,
                                        register=register,
                                        site_register=site_register,
                                        logged_in=logged_in,
                                        registered=registered,
                                        name_and_surname=name_and_surname,
                                        update_profile=update_profile,
                                        city=city,
                                        phone=phone,
                                        date_of_birth=date_of_birth,
                                        user_education=user_education,
                                        certificate_grades_or_university=certificate_grades_or_university,
                                        user_about=user_about,
                                        registration_date=registration_date,
                                        user_status=user_status,
                                        education_of_choice=education_of_choice,
                                        high_education=high_education,
                                        secondary_education=secondary_education,
                                        profile_picture=profile_picture,
                                        change_photo=change_photo,
                                        add_profile_picture=add_profile_picture,
                                        save=save,
                                        news_all=news_all,
                                        last=last,
                                        last_added=last_added,
                                        video_tutorial=video_tutorial,
                                        site_closed=site_closed,
                                        site_closed_time=site_closed_time,
                                        site_closed_text_reason=site_closed_text_reason,
                                        link_timed_out=link_timed_out,
                                        visit_the_link_reset_password=visit_the_link_reset_password,
                                        forgot_password=forgot_password,
                                        email_sent=email_sent,
                                        email_is_not_registere=email_is_not_registere,
                                        change_password=change_password,
                                        password_not_same_confirm_password=password_not_same_confirm_password,
                                        password_changed=password_changed,
                                        forgot_password_question=forgot_password_question,
                                        confirm_password=confirm_password,
                                        send=send,
                                        max_4_file=max_4_file,
                                        profile_info=profile_info,
                                        deleted=deleted,
                                        files_uploaded=files_uploaded,
                                        file_upload=file_upload,
                                        deactive_user_message=deactive_user_message,
                                        student_files=student_files,
                                        delete_all=delete_all,
                                        add=add,
                                        add_max_4_file=add_max_4_file,
                                        there_are_no_files=there_are_no_files
                                        )
    db.add(default_site_language)
    db.commit()
    db.refresh(default_site_language)
    


    


