from sqlalchemy.orm import Session
from configurations import database, models


######## sections/education_dashboard.py
# /education/add/education
# /education/add/category
# /educations/{id}
# /educations/{id}/update
# /educations/{id}/delete
######## sections/messages.py
# /inbox/delete_all
# /inbox/{id}/delete
######## news.py
# /add_news
# /add_news_category
# /news/{id}
# /news/{id}/delete
######## sections/settings.py
# /settings
######## sections/site_languages.py
# /language/install_language_pack/{lang_pack}
# /languages/add-language
# /languages/{id}
# /language/{id}/delete
######## slider.py
# /slider
# /slider/{id}
# /slider/{id}/delete
######## staff.py
# /staff"
# /staff/{id}/delete
######## users.py
# /user/{id}
# /user/{id}/edit
############# FLASH MESSAGES ################
dashboard_language_name = 'Azərbaycan dili'
dashboard_short_language_name = 'AZ'
image_extension_error = 'Yalnız JPG, PNG, JPEG'
conflict_error = 'Ad mövcuddur'
required_boxes_error = 'Ulduzlu sahələri mütləq doldurmalısınız'
was_added = 'əlavə olundu'
name_cannot_be_empty = 'Ad boş ola bilməz'
does_not_exist = 'Mövcud deyil'
updated = 'yeniləndi'
deleted = 'silindi'
messages_deleted = 'Mesajlar silindi'
message_deleted = 'Mesaj silindi'
news_title_or_description_empty = 'Xəbər başlığı və Təsvir boş ola bilməz'
added_to_the_news  = 'xəbərlərə əlavə olundu'
added_to_categories = 'kateqoriyalara əlavə olundu'
deleted = 'silindi'
language_pack_available = 'dil paketi mövcuddur'
loaded = 'yükləndi'
the_language_settings_cannot_be_empty = 'Dil parametri boş ola bilməz!'
main_language_cannot_be_delete = 'saytın əsas dilidi, silinə bilməz'
slide_not_uploaded = 'Slayd yüklənməyib'
image_not_uploaded = 'Şəkil yüklənməyib'
slide_uploaded = 'Slayd Yükləndi'
############# Titles ################
######## routers/admin.py
dashboard_title = 'İdarə paneli'
messages_title = 'Admin mesajları'
educations_title = 'Təhsil'
news_title = 'Xəbərlər'
settings_title = 'Parametrlər'
site_languages_title = 'Saytın dilləri'
slider_title = 'Slayderlər'
staff_title = 'Heyət'
############ HTML TEMPLATES ############
# /templates/dashboard/add_site_language.html
add_site_language = 'Yeni dil əlavə et'
language_name = 'Dilin adı'
short_language_name = 'Dilin qısa adı(AZ,RU,EN)'
# /templates/dashboard/admin_users.html
admins_users = 'Adminlər'
contact_number = 'Əlaqə'
# /templates/dashboard/cards.html
number_of_registrations_in_one_month = 'Son 1 ay ərzində qeydiyyat sayı'
difference_during_the_last_one_month = 'Son 1 ay ərzində fərq'
registrations_in_the_last_one_week = 'Son 1 həftə ərzində olan qeydiyyat'
difference_in_one_week = '1 həftə ərzində fərq'
todays_registration_count = 'Bu günki qeydiyyat sayı'
the_difference_in_one_day = '1 gün ərzində olan fərq'
total_counts_of_users = 'Ümumi istifadəçi sayı'
# /templates/dashboard/edit_user.html
edit_profile = 'Profilə düzəliş et'
city = 'Şəhər'
user_education = 'Təhsil'
certificate_grades_or_university = 'Attestat qiymətləri vəya Universitet Diplomu'
user_about = 'Haqqında'
registration_date = 'Qeydiyyat tarixi'
education_of_choice = 'Seçdiyi Təhsil'
admin_user = 'Admin İstifadəçi'
status_active_or_deactive = 'Useri Aktiv/Deaktiv et'
# /templates/dashboard/educations.html
create_education = 'Təhsil növü əlavə et'
education_name = 'Adı'
country_or_city = 'Ölkə/Şəhər'
about_education = 'Haqqında'
education_category = 'Təhsil Kateqoriyası'
education = 'Təhsil'
person = 'nəfər'
# /templates/dashboard/functions.html
configurations = 'Konfiqurasiyalar'
sidedar_color = 'Yan panel rəngi'
navbar_fixed = 'Seçilmiş navbar'
ligth_or_dark = 'Açıq / Qaranlıq'
# /templates/dashboard/get_message.html
sender = 'Göndərən'
email = 'Email'
message = 'Mesaj'
sent_time = 'Göndərilmə vaxtı'
delete_message = 'Mesajı sil'
back_to_messages = 'Mesajlara qayıt'
# /templates/dashboard/get_site_languages.html
edit_site_language = 'Saytın dilinə düzəliş ver'
# /templates/dashboard/get_update_news.html
update_news = 'Xəbəri yenilə'
# /templates/dashboard/left_sidebar.html
messages = 'Mesajlar'
accounts = 'Hesablar'
admin_users = 'Adminlər'
site_settings = 'Sayt parametrləri'
slider_settings = 'Slayder parametrləri'
educations_settings = 'Təshil parametrləri'
staff = 'Heyət'
# /templates/dashboard/messages.html
admin_messages = 'Rəhbərlik mesajları'
delete_all_messages = 'Bütün mesajları sil'
delete_all_admin_messages = 'Bütün Admin mesajlarını silmək'
confirm_delete_all_messages = 'Bütün admin mesajlarını silməyə əminsiniz??'
no = 'Xeyr'
no_message = 'Mesaj yoxdur'
# /templates/dashboard/messages.html
logout = 'Çıxış'
all_messages = 'Bütün mesajlar'
# /templates/dashboard/news.html
add_news = 'Xəbər əlavə et'
time_to_be_added = 'Əlavə olunma vaxtı'
# /templates/dashboard/site_languages.html
# /templates/dashboard/site_settings.html
install_az = 'Azərbaycan dili yüklə'
install_ru = 'Rus dili yüklə'
install_en = 'İngilis dili yüklə'
add_other_language = 'Başqa dil əlavə et'
language = 'Dil'
short_name = 'Qısa adı'
main_language = 'Saytın əsas dili'
edit_site = 'Sayt Parametrlərinə düzəliş'
site_title = 'Saytın Başlığı'
site_logo = 'Saytın logo yazısı'
site_slogan = 'Saytın sloqanı'
site_email = 'Saytın emaili'
site_phone = 'Saytın əlaqə nömrəsi'
whatsapp_number = 'Whastapp nömrə'
whatsapp_text = 'Whatsapp mətn'
address = 'Adres'
google_map_location = 'Google map link'
site_description = 'Saytın təsviri'
site_about = 'Sayt haqqında'
about_teams = 'Heyət haqqında'
youtube_video_link = 'Youtube Video'
facebook_page = 'Facebook səhifə'
instagram_page = 'İnstagram səhifə'
linkedin_page = 'Linkedin səhifəsi'
schedules = 'İş saatlarımız'
monday = 'B.e.'
tuesday = 'Ç.a.'
wednesday = 'Ç.'
thursday = 'C.a.'
friday = 'C.'
saturday = 'Ş.'
sunday = 'B.'
activate_the_site = 'Saytı aktiv et'
deactivate_the_site = 'Saytı deaktiv et'
# /templates/dashboard/slider.html
slide = 'Slayd'
slide_image = 'Slaydın şəkli'
slide_image_recommendation = 'Normal görünüş üçün 1920 × 801 məsləhət görülür'
post_image = 'Postun şəkli'
slide_title = 'Slayd başlığı'
slide_description = 'Slayd təsviri'
slides = 'Slaydlar'
change_slide_image = 'Slaydın şəklini dəyiş'
change_post_image = 'Postun şəklini dəyiş'
# /templates/dashboard/staff.html
add_staff = 'Kadr əlavə et'
job_position = 'Vəzifəsi'
facebook = 'Facebook'
instagram = 'Instagram'
linkedin = 'Linkedin'
twitter = 'Twitter'
behance = 'Behance'
profile_picture = 'Profil fotosu'

######## universal values ##########
name_and_surname = 'Ad və soyad' 
date_of_birth = 'Doğum tarixi'
save = 'Yadda saxla'
add = 'Əlavə et'
admin = 'Admin'
info = 'Info'
edit = 'Düzəliş et'
delete = 'Sil'
update = 'Yenilə'
next = 'İrəli'
previous = 'Geri'
user_status = 'Status'
students = 'Tələbələr'
phone = 'Əlaqə nömrəsi'
student = 'Tələbə'
description = 'Təsvir'
title = 'Başlıq'
photo = 'Şəkil'
change_photo = 'Şəkli dəyiş'
users = 'İstifadəçilər'
no_category_message = 'Kateqoriya yoxdur. Əvvəlcə kateqoriya əlavə edin.'
add_category = 'Kateqoriya əlavə et'
category = 'Kategoriya'
news = 'Xəbərlər'
documents = 'Sənədləri'
password = 'Parol'
login = 'Daxil ol'
site_languages = 'Saytın dilləri'

def set_azerbaijan_language(db: Session = database.get_db()):
    azerbaijan_language = models.DashboardLanguages(
        image_extension_error = image_extension_error,
        conflict_error = conflict_error,
        required_boxes_error = required_boxes_error,
        was_added = was_added,
        name_cannot_be_empty = name_cannot_be_empty,
        does_not_exist = does_not_exist,
        updated = updated,
        deleted = deleted,
        messages_deleted = messages_deleted,
        message_deleted = message_deleted,
        news_title_or_description_empty = news_title_or_description_empty,
        added_to_the_news  = added_to_the_news,
        added_to_categories = added_to_categories,
        deleted = deleted,
        language_pack_available = language_pack_available,
        loaded = loaded,
        the_language_settings_cannot_be_empty = the_language_settings_cannot_be_empty,
        main_language_cannot_be_delete = main_language_cannot_be_delete,
        slide_not_uploaded = slide_not_uploaded,
        image_not_uploaded = image_not_uploaded,
        slide_uploaded = slide_uploaded,
        dashboard_title = dashboard_title,
        messages_title =  messages_title,
        educations_title = educations_title,
        news_title = news_title,
        settings_title = settings_title,
        site_languages_title = site_languages_title,
        slider_title = slider_title,
        staff_title = staff_title,
        add_site_language = add_site_language,
        language_name = language_name,
        short_language_name = short_language_name,
        admins_users = admins_users,
        contact_number = contact_number,
        number_of_registrations_in_one_month = number_of_registrations_in_one_month,
        difference_during_the_last_one_month = difference_during_the_last_one_month,
        registrations_in_the_last_one_week = registrations_in_the_last_one_week,
        difference_in_one_week = difference_in_one_week,
        todays_registration_count = todays_registration_count,
        the_difference_in_one_day = the_difference_in_one_day,
        total_counts_of_users = total_counts_of_users,
        edit_profile = edit_profile,
        city = city,
        user_education = user_education,
        certificate_grades_or_university = certificate_grades_or_university,
        user_about = user_about,
        registration_date = registration_date,
        education_of_choice = education_of_choice,
        admin_user = admin_user,
        status_active_or_deactive = status_active_or_deactive,
        create_education = create_education,
        education_name = education_name,
        country_or_city = country_or_city,
        about_education = about_education,
        education_category = education_category,
        education = education,
        person = person,
        configurations = configurations,
        sidedar_color = sidedar_color,
        navbar_fixed = navbar_fixed,
        ligth_or_dark = ligth_or_dark,
        sender = sender,
        email = email,
        message = message,
        sent_time = sent_time,
        delete_message = delete_message,
        back_to_messages = back_to_messages,
        edit_site_language = edit_site_language,
        update_news = update_news,
        messages = messages,
        accounts = accounts,
        admin_users = admin_users,
        site_settings = site_settings,
        slider_settings = slider_settings,
        educations_settings = educations_settings,
        staff = staff,
        admin_messages = admin_messages,
        delete_all_messages = delete_all_messages,
        delete_all_admin_messages = delete_all_admin_messages,
        confirm_delete_all_messages = confirm_delete_all_messages,
        no = no,
        no_message = no_message,
        logout = logout,
        all_messages = all_messages,
        add_news = add_news,
        time_to_be_added = time_to_be_added,
        install_az = install_az,
        install_ru = install_ru,
        install_en = install_en,
        add_other_language = add_other_language,
        language = language,
        short_name = short_name,
        main_language = main_language,
        edit_site = edit_site,
        site_title = site_title,
        site_logo = site_logo,
        site_slogan = site_slogan,
        site_email = site_email,
        site_phone = site_phone,
        whatsapp_number = whatsapp_number,
        whatsapp_text = whatsapp_text,
        address = address,
        google_map_location = google_map_location,
        site_description = site_description,
        site_about = site_about,
        about_teams = about_teams,
        youtube_video_link = youtube_video_link,
        facebook_page = facebook_page,
        instagram_page = instagram_page,
        linkedin_page = linkedin_page,
        schedules = schedules,
        monday = monday,
        tuesday = tuesday,
        wednesday = wednesday,
        thursday = thursday,
        friday = friday,
        saturday = saturday,
        sunday = sunday,
        activate_the_site = activate_the_site,
        deactivate_the_site = deactivate_the_site,
        slide = slide,
        slide_image = slide_image,
        slide_image_recommendation = slide_image_recommendation,
        post_image = post_image,
        slide_title = slide_title,
        slide_description = slide_description,
        slides = slides,
        change_slide_image = change_slide_image,
        change_post_image = change_post_image,
        add_staff = add_staff,
        job_position = job_position,
        facebook = facebook,
        instagram = instagram,
        linkedin = linkedin,
        twitter = twitter,
        behance = behance,
        profile_picture = profile_picture,
        name_and_surname = name_and_surname,
        date_of_birth = date_of_birth,
        save = save,
        add = add,
        admin = admin,
        info = info,
        edit = edit,
        delete = delete,
        update = update,
        next = next,
        previous = previous,
        user_status = user_status,
        students = students,
        phone = phone,
        student = student,
        description = description,
        title = title,
        photo = photo,
        change_photo = change_photo,
        users = users,
        no_category_message = no_category_message,
        add_category = add_category,
        category = category,
        news = news,
        documents = documents,
        password = password,
        login = login,
        site_languages = site_languages
    )

    db.add(azerbaijan_language)
    db.commit()










