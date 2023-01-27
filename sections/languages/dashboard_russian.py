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
dashboard_language_name = 'Русский'
dashboard_short_language_name = 'RU'
image_extension_error = 'Только JPG, PNG, JPEG'
conflict_error = 'Имя доступно'
required_boxes_error = 'Вы должны заполнить отмеченные поля'
was_added = 'был добавлен'
name_cannot_be_empty = 'Имя не может быть пустым'
does_not_exist = 'Не существует'
updated = 'обновлен'
deleted = 'удален'
messages_deleted = 'Сообщения удалены'
message_deleted = 'Сообщение удалено'
news_title_or_description_empty = 'Заголовок новости и описание не могут быть пустыми'
added_to_the_news  = 'добавлено в новость'
added_to_categories = 'добавлено в категории'
language_pack_available = 'языковой пакет доступен'
loaded = 'загружен'
the_language_settings_cannot_be_empty = 'Параметр языка не может быть пустым!'
main_language_cannot_be_delete = 'основной язык сайта, удалить нельзя'
slide_not_uploaded = 'Слайд не загружен'
image_not_uploaded = 'Изображение не загружено'
slide_uploaded = 'Слайд загружен'
############# Titles ################
######## routers/admin.py
dashboard_title = 'Панель администратора'
messages_title = 'Сообщения администратора'
educations_title = 'Образование'
news_title = 'Новости'
settings_title = 'Настройки'
site_languages_title = 'Языки сайта'
slider_title = 'Слайдеры'
staff_title = 'Персонал'
############ HTML TEMPLATES ############
# /templates/dashboard/add_site_language.html
add_site_language = 'Добавить новый язык'
language_name = 'Название языка'
short_language_name = 'Краткое название языка(AZ,RU,EN)'
# /templates/dashboard/admin_users.html
admins_users = 'Админы'
contact_number = 'Контакт'
# /templates/dashboard/cards.html
number_of_registrations_in_one_month = 'Последний 1 месяц'
difference_during_the_last_one_month = 'Разница в 1 месяц'
registrations_in_the_last_one_week = 'Последняя 1 неделя'
difference_in_one_week = 'Разница в 1 неделю'
todays_registration_count = 'Сегодняшняя регистрация'
the_difference_in_one_day = 'Разница в 24 часа'
total_counts_of_users = 'Общее количество пользователей'
# /templates/dashboard/edit_user.html
edit_profile = 'Редактировать профиль'
city = 'Город'
user_education = 'Образование'
certificate_grades_or_university = 'Сертификационные оценки или университет'
user_about = 'О пользователе'
registration_date = 'Дата регистрации'
education_of_choice = 'Образование на выбор'
admin_user = 'Администратор'
status_active_or_deactive = 'Включить/отключить пользователя'
# /templates/dashboard/educations.html
create_education = 'Добавить тип образования'
education_name = 'Название образования'
country_or_city = 'Страна/Город'
about_education = 'Об образовании'
education_category = 'Категория образования'
education = 'Образование'
person = 'человек'
# /templates/dashboard/functions.html
configurations = 'Конфигурации'
sidedar_color = 'Цвет боковой панели'
navbar_fixed = 'Навбар исправлен'
ligth_or_dark = 'Светлый / Темный'
# /templates/dashboard/get_message.html
sender = 'Отправитель'
email = 'Эл. адрес'
message = 'Сообщение'
sent_time = 'Время отправки'
delete_message = 'Удалить сообщение'
back_to_messages = 'Назад к сообщениям'
# /templates/dashboard/get_site_languages.html
edit_site_language = 'Изменить язык сайта'
# /templates/dashboard/get_update_news.html
update_news = 'Обновите новости'
# /templates/dashboard/left_sidebar.html
messages = 'Сообщения'
accounts = 'Учетные записи'
admin_users = 'Админы'
site_settings = 'Настройки сайта'
slider_settings = 'Настройки слайдера'
educations_settings = 'Образовательные настройки'
staff = 'Персонал'
# /templates/dashboard/messages.html
admin_messages = 'Сообщения администратора'
delete_all_messages = 'Удалить все сообщения'
delete_all_admin_messages = 'Удалить все сообщения администратора'
confirm_delete_all_messages = 'Вы уверены, что удалили все сообщения администратора???'
no = 'Нет'
no_message = 'Нет сообщений'
# /templates/dashboard/navbar.html
logout = 'Выйти'
all_messages = 'Все сообщения'
# /templates/dashboard/news.html
add_news = 'Добавить новость'
time_to_be_added = 'Добавлен'
# /templates/dashboard/site_languages.html
# /templates/dashboard/site_settings.html
install_az = 'Установить Aзербайджанский язык'
install_ru = 'Установить Русский язык'
install_en = 'Установить Aнглийский'
add_other_language = 'Добавить другой язык'
language = 'Язык'
short_name = 'Короткое имя'
main_language = 'Основной язык сайта'
edit_site = 'Редактирование настроек сайта'
site_title = 'Заголовок сайта'
site_logo = 'Логотип сайта'
site_slogan = 'Слоган сайта'
site_email = 'Электронная почта сайта'
site_phone = 'Контактный телефон сайта'
whatsapp_number = 'Номер WhatsApp'
whatsapp_text = 'WhatsApp текст'
address = 'Адрес'
google_map_location = 'ссылка на Google map'
site_description = 'Oписание сайта'
site_about = 'О сайте'
about_teams = 'О персонале'
youtube_video_link = 'Youtube Video'
facebook_page = 'Cтраница на Facebook'
instagram_page = 'Cтраница на  İnstagram'
linkedin_page = 'Cтраница на  Linkedin'
schedules = 'Наше рабочее время'
monday = 'П.'
tuesday = 'Вт.'
wednesday = 'Ср.'
thursday = 'Ч.'
friday = 'Пя.'
saturday = 'С.'
sunday = 'В.'
activate_the_site = 'Активировать сайт'
deactivate_the_site = 'Деактивировать сайт'
# /templates/dashboard/slider.html
slide = 'Слайд'
slide_image = 'Изображение слайда'
slide_image_recommendation = '1920 × 801 рекомендуется для обычного просмотра'
post_image = 'Изображение поста'
slide_title = 'Название слайда'
slide_description = 'Описание слайда'
slides = 'Слайды'
change_slide_image = 'Изменение изображения слайда'
change_post_image = 'Сменить картинку поста'
# /templates/dashboard/staff.html
add_staff = 'Добавить персонал'
job_position = 'Место работы'
facebook = 'Facebook'
instagram = 'Instagram'
linkedin = 'Linkedin'
twitter = 'Twitter'
behance = 'Behance'
profile_picture = 'Изображение профиля'

######## universal values ##########
name_and_surname = 'Имя и фамилия' 
date_of_birth = 'Дата рождения'
save = 'Сохранить'
add = 'Добавлять'
admin = 'Администратор'
info = 'Информация'
edit = 'Редактировать'
delete = 'Удалить'
update = 'Обновлять'
next = 'Следующий'
previous = 'Предыдущий'
user_status = 'Статус'
students = 'Ученики'
phone = 'Номер телефона'
student = 'Ученик'
description = 'Описание'
title = 'Заголовок'
photo = 'Фото'
change_photo = 'Измени фотографию'
add_photo = 'Добавить изображение'
users = 'Пользователи'
no_category_message = 'Нет категории. Сначала добавьте категорию.'
add_category = 'Добавить категорию'
category = 'Категория'
category_name = 'Название категории'
posts_count = 'Количество сообщений'
news = 'Новости'
documents = 'Документы'
password = 'Пароль'
login = 'Входить'
site_languages = 'Языки сайта'
#installer
correct_email_message = 'Электронная почта неверна'
password_minimum_8_character_message = 'Пароль должен быть не менее 8 символов'
boxes_are_cannot_empty = 'Введите значение'
there_is_no_such_option = 'Нет такого варианта'
the_site_is_ready_for_use = 'Сайт готов к использованию ;)'

installation_panel = 'Панель установки'
create_super_user = 'Создайте суперпользователя'
site_url = 'Адрес сайта'
site_language = 'Язык сайта'


def set_russian(db: Session = database.get_db()):
    russian_language = models.DashboardLanguages(
        dashboard_language_name = dashboard_language_name,
        dashboard_short_language_name = dashboard_short_language_name,
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
        site_languages = site_languages,
        correct_email_message = correct_email_message,
        password_minimum_8_character_message = password_minimum_8_character_message,
        boxes_are_cannot_empty = boxes_are_cannot_empty,
        there_is_no_such_option = there_is_no_such_option,
        the_site_is_ready_for_use = the_site_is_ready_for_use,
        installation_panel = installation_panel,
        create_super_user = create_super_user,
        site_url = site_url,
        site_language = site_language,
        category_name = category_name,
        posts_count = posts_count,
        add_photo = add_photo
    )

    db.add(russian_language)
    db.commit()

