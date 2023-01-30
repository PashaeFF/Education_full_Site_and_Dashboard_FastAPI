from sqlalchemy.orm import Session
from configurations import database, models

lang_name = 'English',
short_lang_name = 'EN',
#/routers/site.py
site_about = 'About'
#/site_sections/auth.py  - '/login'
login_page_title = 'Login'
user_logged_message = 'You are logged in'
wrong_password_message = 'The password is incorrect'
user_does_not_exist_message = 'User does not exist'
login = 'Login'
####################### - '/registration'
registration_page_title = 'Registration'
correct_email_message = 'Email is incorrect'
password_minimum_8_character_message = 'Password must be at least 8 characters long'
name_not_added_message = 'You have not added a name'
email_is_available_message = 'Email is available'
registration_success = 'You are logged in'
#/site_sections/contact.py - '/contact'
contact_page_title = 'Contact'
message_spam_message = 'Spam!!!'
the_message_cannot_empty_message = 'The message cannot be empty'
boxes_are_cannot_empty = 'Boxes cannot be empty'
message_has_been_sent_to_management = 'Your message has been sent to management'
#/site_sections/educations.py - '/educations'
educations_page_title = 'Education'
#/site_sections/news.py '/news'
news_page_title = 'News'
#/site_sections/users.py  - '/profile/{id}'
user_profile_info_page_title = 'Profile information'
image_extension_error_message = 'JPG, PNG, JPEG only'
profile_success_message = 'Profile complete'
####################### HTML TEMPLATES LANGUAGE ########################
#/templates/site/route/about-page.html
why = 'Why'
schedules = 'Our working hours'
week_days = 'Week days'
monday = 'Mon.'
tuesday = 'Tue.'
wednesday = 'Wed.'
thursday = 'Thu.'
friday = 'Fri.'
saturday = 'Sat.'
sunday = 'Sun.'
our_staff = 'Our Team'
previous = 'Previous'
next = 'Next'
#/templates/site/route/all_educations.html
educations_all = 'Educations All'
detail = 'Details'
#/templates/site/route/contactus-page.html
got_question_write_to_us_text = 'Got a question?? Write to us.'
address = 'Address'
your_contact_number = 'Your contact number'
email = 'Email'
#/templates/site/route/aducation_details.html
number_of_joined_students = 'Joined Students'
#/templates/site/route/aducation-page.html 
view = 'View'
#/templates/site/route/footer.html & topnav.html
home = 'Home'
education = 'Education'
news = 'News'
about = 'About'
whatsapp_message = 'Whatsapp message'
call_us = 'Call us'
dashboard = 'Dashboard'
profile = 'Profile'
logout = 'Logout'
categories = 'Categories'
contact = 'Contact'
#/templates/site/route/full_news.html
created_at = 'Time to add'
category = 'Category'
#/templates/site/route/login.html & register.html
password = 'Password'
sign_in = 'Login'
register = 'Register'
site_register = 'Registration'
logged_in = 'You are logged in...'
registered = 'You are registered...'
name_and_surname = 'Name and Surname'
#/templates/site/route/profile.html
update_profile = 'Edit Profile'
city = 'City'
phone = 'Contact number'
date_of_birth = 'Date of Birth'
user_education = 'Education'
certificate_grades_or_university = 'Certificate grades or University'
user_about = 'About'
registration_date = 'Registration date'
user_status = 'Status'
education_of_choice = 'Education of choice'
high_education = 'High Education'
secondary_education = 'Secondary education'
profile_picture = 'Profile picture'
change_photo = 'Change profile picture'
add_profile_picture = 'Add profile picture'
save = 'Save'
#/templates/site/route/short_news.html
news_all = 'All news'
last = 'Last'
#/templates/site/route/slider_welcome.html
last_added = 'Recent additions'
#/templates/site/route/video_test.html
video_tutorial = 'Video Tutorial'
#/templates/site/route/closed.html
site_closed = 'the site is closed'
site_closed_time = 'temporarily'
site_closed_text_reason = 'Due to changes'
#lost password
#token.py
link_timed_out = 'Link timed out'
visit_the_link_reset_password = 'Visit the link to reset your password within 10 minutes'
#auth.py
#/forgot-password
forgot_password = 'Forgot password'
#/forgot-password
email_sent = 'Email sent'
email_is_not_registere = 'This email is not registered'
#/change-password
change_password = 'Change your password'
password_not_same_confirm_password = 'Password and confirm password are not the same'
password_changed = 'You have changed your password'
#login.html
forgot_password_question = 'Forgot password?'
#reset-password.html
confirm_password = 'Confirm Password'
send = 'Send'
#user.py
max_4_file = 'You can upload a maximum of 4 files'
profile_info = 'Profile information'
deleted = 'All deleted'
files_uploaded = 'Files uploaded'
file_upload = 'File upload'
#auth.py
deactive_user_message = 'The user is not active'
#profile.html
student_files = 'Student files'
delete_all = 'Delete all'
add = 'Add'
#upload_files.html
add_max_4_file = 'Add file (Maximum 4 files)'
there_are_no_files = 'There are no files'

def set_english_language(db: Session = database.get_db()):
    english_language = models.SiteLanguages(
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
    db.add(english_language)
    db.commit()
    db.refresh(english_language)
    


    
