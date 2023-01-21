from sqlalchemy.orm import Session
from configurations import database, models

lang_name = 'Русский',
short_lang_name = 'RU',
#/routers/site.py
site_about = 'О нас'
#/site_sections/auth.py  - '/login'
login_page_title = 'Логин'
user_logged_message = 'Вы вошли на сайт'
login = 'Логин'
wrong_password_message = 'Пароль неправильный'
user_does_not_exist_message = 'Пользователь не существует'
####################### - '/registration'
registration_page_title = 'Регистрация'
correct_email_message = 'Введите адрес электронной почты правильно'
password_minimum_8_character_message = 'Пароль должен быть не менее 8 символов'
name_not_added_message = 'Вы не добавили имя'
email_is_available_message = 'Электронная почта уже доступна'
registration_success = 'Вы вошли на сайт'
#/site_sections/contact.py - '/contact'
contact_page_title = 'Контакт'
message_spam_message = 'Спам!!!'
the_message_cannot_empty_message = 'Сообщение не может быть пустым'
boxes_are_cannot_empty = 'Введите значение'
message_has_been_sent_to_management = 'Ваше сообщение отправлено администраторам'
#/site_sections/educations.py - '/educations'
educations_page_title = 'Образование'
#/site_sections/news.py '/news'
news_page_title = 'Новости'
#/site_sections/users.py  - '/profile/{id}'
user_profile_info_page_title = 'Информация профиля'
image_extension_error_message = 'Только JPG, PNG, JPEG'
profile_success_message = 'Профиль завершен'
####################### HTML TEMPLATES LANGUAGE ########################
#/templates/site/route/about-page.html
why = 'Почему'
schedules = 'Наше рабочее время'
week_days = 'Дни недели'
monday = 'П.'
tuesday = 'Вт.'
wednesday = 'Ср.'
thursday = 'Ч.'
friday = 'Пя.'
saturday = 'С.'
sunday = 'В.'
our_staff = 'Наша команда'
previous = 'Назад'
next = 'Вперед'
#/templates/site/route/all_educations.html
educations_all = 'Общий'
detail = 'Подробности'
#/templates/site/route/contactus-page.html
got_question_write_to_us_text = 'У вас есть вопрос?? Напишите нам'
address = 'Адрес'
your_contact_number = 'Ваш контактный номер'
email = 'Эл. адрес'
#/templates/site/route/aducation_details.html
number_of_joined_students = 'Количество студентов'
#/templates/site/route/aducation-page.html 
view = 'Посмотреть'
#/templates/site/route/footer.html & topnav.html
home = 'Главная'
education = 'Образование'
news = 'Новости'
about = 'О нас'
whatsapp_message = 'WhatsApp'
call_us = 'Позвоните нам'
dashboard = 'Панель администратора'
profile = 'Профиль'
logout = 'Выход'
categories = 'Категории'
contact = 'Контакт'
#/templates/site/route/full_news.html
created_at = 'Добавлен'
category = 'Категория'
#/templates/site/route/login.html & register.html
password = 'Пароль'
sign_in = 'Входить'
register = 'Зарегистрироваться'
site_register = 'Регистрация'
logged_in = 'Вы вошли в систему...'
registered = 'Вы зарегистрированы...'
name_and_surname = 'Ваше имя и фамилия'
#/templates/site/route/profile.html
update_profile = 'Редактировать профиль'
city = 'Место рождения'
phone = 'Контактный телефон'
date_of_birth = 'Дата рождения'
user_education = 'Образование'
certificate_grades_or_university = 'Сертификационные оценки или университетский диплом'
user_about = 'О пользователе'
registration_date = 'Дата регистрации'
user_status = 'Статус'
education_of_choice = 'Образование на выбор'
high_education = 'Высшее образование'
secondary_education = 'Среднее образование'
profile_picture = 'Аватар'
change_photo = 'Изменить фото'
add_profile_picture = 'Добавить фото'
save = 'Сохранить'
#/templates/site/route/short_news.html
news_all = 'Все новости'
last = 'Последние'
#/templates/site/route/slider_welcome.html
last_added = 'Последние добавления'
#/templates/site/route/video_test.html
video_tutorial = 'Видео инструкция'
#/templates/site/route/closed.html
site_closed = 'Сайт закрыт'
site_closed_time = 'временно'
site_closed_text_reason = 'для обновлений'
#lost password
#token.py
link_timed_out = 'Срок действия ссылки истек'
visit_the_link_reset_password = 'Перейдите по ссылке, чтобы сбросить пароль в течение 10 минут'
#auth.py
#/forgot-password
forgot_password = 'Восстановление пароля'
#/forgot-password
email_sent = 'Письмо отправлено на Email'
email_is_not_registere = 'Эта электронная почта не зарегистрирована'
#/change-password
change_password = 'Измените свой пароль'
password_not_same_confirm_password = 'Пароль и подтверждение пароля не совпадают'
password_changed = 'Вы изменили свой пароль'
#login.html
forgot_password_question = 'Забыли свой пароль?'
#reset-password.html
confirm_password = 'Подтверждение пароля'
send = 'Отправить'
#user.py
max_4_file = 'Вы можете загрузить максимум 4 файла'
profile_info = 'Информация профиля'
deleted = 'Все удалено'
files_uploaded = 'Файлы загружены'
file_upload = 'Загрузить файл'
#auth.py
deactive_user_message = 'Пользователь не активен'
#profile.html
student_files = 'Студенческие файлы'
delete_all = 'Удалить все'
add = 'Добавить'
#upload_files.html
add_max_4_file = 'Добавить файл (максимум 4 файла)'
there_are_no_files = 'Нет файлов'


def set_russian_language(db: Session = database.get_db()):
    russian_language = models.SiteLanguages(
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
                                        max_4_file = max_4_file,
                                        profile_info = profile_info,
                                        deleted = deleted,
                                        files_uploaded = files_uploaded,
                                        file_upload = file_upload,
                                        deactive_user_message = deactive_user_message,
                                        student_files = student_files,
                                        delete_all = delete_all,
                                        add = add,
                                        add_max_4_file = add_max_4_file,
                                        there_are_no_files = there_are_no_files
                                        )
    db.add(russian_language)
    db.commit()
    db.refresh(russian_language)
    


    


