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
dashboard_language_name = 'English'
dashboard_short_language_name = 'EN'
image_extension_error = 'JPG, PNG, JPEG only'
conflict_error = 'Name available'
required_boxes_error = 'You must fill in the starred fields'
was_added = 'was added'
name_cannot_be_empty = 'The name cannot be empty'
does_not_exist = 'Does not exist'
updated = 'updated'
deleted = 'deleted'
messages_deleted = 'Messages deleted'
message_deleted = 'Message deleted'
news_title_or_description_empty = 'News title and Description cannot be empty'
added_to_the_news  = 'added to the news'
added_to_categories = 'added to categories'
language_pack_available = 'language pack available'
loaded = 'loaded'
the_language_settings_cannot_be_empty = 'The language setting cannot be empty!'
main_language_cannot_be_delete = 'the main language of the site, cannot be deleted'
slide_not_uploaded = 'Slide not uploaded'
image_not_uploaded = 'Image not uploaded'
slide_uploaded = 'Slide Uploaded'
############# Titles ################
######## routers/admin.py
dashboard_title = 'Dashboard'
messages_title = 'Admin messages'
educations_title = 'Education'
news_title = 'News'
settings_title = 'Settings'
site_languages_title = 'Site languages'
slider_title = 'Sliders'
staff_title = 'Staff'
############ HTML TEMPLATES ############
# /templates/dashboard/add_site_language.html
add_site_language = 'Add new language'
language_name = 'The name of the language'
short_language_name = 'Short name of the language(AZ,RU,EN)'
# /templates/dashboard/admin_users.html
admins_users = 'Admins'
contact_number = 'Contact'
# /templates/dashboard/cards.html
number_of_registrations_in_one_month = 'Registration within 1 month'
difference_during_the_last_one_month = 'Difference in 1 month'
registrations_in_the_last_one_week = 'Registration within 1 week'
difference_in_one_week = 'Difference in 1 week'
todays_registration_count = 'Today\'s registration'
the_difference_in_one_day = 'The difference in 24 hours'
total_counts_of_users = 'Total counts of users'
# /templates/dashboard/edit_user.html
edit_profile = 'Edit profile'
city = 'City'
user_education = 'Education'
certificate_grades_or_university = 'Certificate grades or University'
user_about = 'About'
registration_date = 'Registration date'
education_of_choice = 'Education of choice'
admin_user = 'Admin user'
status_active_or_deactive = 'Enable/Disable User'
# /templates/dashboard/educations.html
create_education = 'Add education type'
education_name = 'Education name'
country_or_city = 'Country/City'
about_education = 'About'
education_category = 'Education Category'
education = 'Education'
person = 'person'
# /templates/dashboard/functions.html
configurations = 'Configurations'
sidedar_color = 'Sidebar color'
navbar_fixed = 'Navbar fixed'
ligth_or_dark = 'Light / Dark'
# /templates/dashboard/get_message.html
sender = 'Sender'
email = 'Email'
message = 'Message'
sent_time = 'Sent time'
delete_message = 'Delete message'
back_to_messages = 'Back to messages'
# /templates/dashboard/get_site_languages.html
edit_site_language = 'Edit the site language'
# /templates/dashboard/get_update_news.html
update_news = 'Update the news'
# /templates/dashboard/left_sidebar.html
messages = 'Messages'
accounts = 'Accounts'
admin_users = 'Admins'
site_settings = 'Site Settings'
slider_settings = 'Slider Settings'
educations_settings = 'Educational settings'
staff = 'Staff'
# /templates/dashboard/messages.html
admin_messages = 'Admin messages'
delete_all_messages = 'Delete all messages'
delete_all_admin_messages = 'Delete all Admin messages'
confirm_delete_all_messages = 'Are you sure to delete all admin messages???'
no = 'No'
no_message = 'No message'
# /templates/dashboard/navbar.html
logout = 'Logout'
all_messages = 'All messages'
# /templates/dashboard/news.html
add_news = 'Add news'
time_to_be_added = 'Added'
# /templates/dashboard/site_languages.html
# /templates/dashboard/site_settings.html
install_az = 'Install the Azerbaijani language'
install_ru = 'Install Russian language'
install_en = 'Install English'
add_other_language = 'Add another language'
language = 'Language'
short_name = 'Short name'
main_language = 'Main language of the site'
edit_site = 'Editing Site Settings'
site_title = 'Site title'
site_logo = 'Site logo'
site_slogan = 'Site slogan'
site_email = 'Site Email'
site_phone = 'Site contact number'
whatsapp_number = 'Whastapp number'
whatsapp_text = 'Whatsapp text'
address = 'Address'
google_map_location = 'Google map link'
site_description = 'Site Description'
site_about = 'About the site'
about_teams = 'About the staff'
youtube_video_link = 'Youtube Video'
facebook_page = 'Facebook page'
instagram_page = 'İnstagram page'
linkedin_page = 'Linkedin page'
schedules = 'Our working hours'
monday = 'Mon.'
tuesday = 'Tue.'
wednesday = 'Wed.'
thursday = 'Thu.'
friday = 'Fri.'
saturday = 'Sat.'
sunday = 'Sun.'
activate_the_site = 'Activate the site'
deactivate_the_site = 'Deactivate the site'
# /templates/dashboard/slider.html
slide = 'Slide'
slide_image = 'Image of the slide'
slide_image_recommendation = '1920 × 801 is recommended for normal viewing'
post_image = 'Image of the post'
slide_title = 'Slide title'
slide_description = 'Slide description'
slides = 'Slides'
change_slide_image = 'Changing the slide image'
change_post_image = 'Change the image of the post'
# /templates/dashboard/staff.html
add_staff = 'Add staff'
job_position = 'Job position'
facebook = 'Facebook'
instagram = 'Instagram'
linkedin = 'Linkedin'
twitter = 'Twitter'
behance = 'Behance'
profile_picture = 'Profile picture'

######## universal values ##########
name_and_surname = 'Name and surname' 
date_of_birth = 'Date of birth'
save = 'Save'
add = 'Add'
admin = 'Admin'
info = 'Info'
edit = 'Edit'
delete = 'Delete'
update = 'Update'
next = 'Next'
previous = 'Previous'
user_status = 'Status'
students = 'Students'
phone = 'Phone number'
student = 'Student'
description = 'Description'
title = 'Title'
photo = 'Photo'
change_photo = 'Change photo'
add_photo = 'Add a picture'
users = 'Users'
no_category_message = 'No category. First, add a category.'
add_category = 'Add category'
category = 'Category'
category_name = 'Category name'
posts_count = 'Posts count'
news = 'News'
documents = 'Documents'
password = 'Password'
login = 'Login'
site_languages = 'Site languages'
#installer
correct_email_message = 'Email is incorrect'
password_minimum_8_character_message = 'Password must be at least 8 characters long'
boxes_are_cannot_empty = 'Boxes cannot be empty'
there_is_no_such_option = 'There is no such option'
the_site_is_ready_for_use = 'The site is ready for use ;)'

installation_panel = 'Installation panel'
create_super_user = 'Create a Super User'
site_url = 'Site url'
site_language = 'The language of the site'


def set_english(db: Session = database.get_db()):
    english_language = models.DashboardLanguages(
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

    db.add(english_language)
    db.commit()

