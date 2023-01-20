from sqlalchemy import Column, Integer, Boolean, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from configurations.database import Base
from datetime import datetime

  ######################################
 ###########      User     ############
######################################
class User(Base):
  __tablename__ = 'user'

  id = Column(Integer, primary_key=True, index=True)
  email = Column(String, nullable=False, unique=True,index=True)
  password = Column(String, nullable= False)
  is_active = Column(Boolean, default=True)
  admin_user = Column(Boolean, default=False)
  super_user = Column(Boolean, default=False)
  profile_picture = Column(String, nullable=True)
  education_files = Column(Text, nullable=True)
  user_site_language = Column(Integer, nullable=True, default=1)

  navbar_fixed = Column(String, nullable=True, default="")
  site_mode = Column(String, nullable=True, default="")
  sidebar_selected_color = Column(String, nullable=True, default="1")

  name_surname = Column(String(150), nullable=True, default="")
  age = Column(String, nullable=True)
  city = Column(String(100), nullable=True, default="")
  phone = Column(String(30),nullable=True, default="")
  education = Column(String(150), nullable=True, default="")
  certificate_points = Column(String, nullable=True, default="")
  about = Column(Text, nullable=True)


  select_university_id = Column(Integer, ForeignKey("education.id", ondelete='SET NULL'), default=None)
  select_university = relationship("Education", back_populates="select_education")

  created_at = Column(DateTime, default=datetime.now())
  updated_at = Column(DateTime, onupdate=datetime.now())

  ######################################
 ###########   Education   ############
######################################
class Education(Base):
  __tablename__ = 'education'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False, unique=True)
  city = Column(String, nullable=True)
  education_type = Column(String, nullable=True)
  students_count = Column(String, nullable=True, default=0)
  about_education = Column(String, nullable=True)
  documents = Column(String, nullable=True)
  photos = Column(String, nullable=True)

  select_education = relationship("User", back_populates="select_university", passive_deletes='all')

  ######################################
 ##########   Edu Category   ##########
######################################

class EduCategory(Base):
  __tablename__ = 'edu_category'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False, unique=True)

  ######################################
 ###########   SiteNews  ##############
######################################
class SiteNews(Base):
  __tablename__ = 'sitenews'

  id = Column(Integer, primary_key=True)
  news_title = Column(String, nullable=True)
  news_image = Column(String, nullable=True)
  description = Column(Text, nullable=True)
  news_active = Column(Boolean, default=True)
  views = Column(Integer, default=0)

  select_category_id = Column(Integer, ForeignKey("newscategory.id", ondelete='CASCADE'), default=1)
  select_category = relationship("NewsCategory", back_populates="category")

  created_at = Column(DateTime, default=datetime.now())
  updated_at = Column(DateTime, onupdate=datetime.now())

  ######################################
 ##########   NewsCategory   ##########
######################################
class NewsCategory(Base):
  __tablename__ = 'newscategory'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False, unique=True)
  category = relationship("SiteNews", back_populates="select_category", passive_deletes=True)

  ######################################
 ##########   SiteSettings   ##########
######################################
class SiteSettings(Base):
  __tablename__ = 'site_settings'

  id = Column(Integer, primary_key=True)
  site_url = Column(Text, nullable=True, default="")
  site_title = Column(String, nullable=True, default="")
  site_description = Column(Text, nullable=True, default="")
  site_logo = Column(Text, nullable=True, default="")
  site_slogan = Column(String, nullable=True, default="")
  phone = Column(String, nullable=True, default="")
  wp_number = Column(String, nullable=True, default="")
  wp_text = Column(String, nullable=True, default="")
  is_active = Column(Boolean, default=True)
  site_about = Column(Text, nullable=True, default="")
  about_teams = Column(Text, nullable=True, default="")
  site_email = Column(String, nullable=True, default="")
  address = Column(String, nullable=True, default="")
  google_map = Column(String, nullable=True, default="")
  set_site_language = Column(Integer, nullable=False, default=1)


  youtube_video = Column(String, nullable=True, default="")
  facebook = Column(Text, nullable=True, default="")
  instagram = Column(Text, nullable=True, default="")
  linkedin = Column(Text, nullable=True, default="")

  monday = Column(String, nullable=True, default="")
  tuesday = Column(String, nullable=True, default="")
  wednesday = Column(String, nullable=True, default="")
  thursday = Column(String, nullable=True, default="")
  friday = Column(String, nullable=True, default="")
  saturday = Column(String, nullable=True, default="")
  sunday = Column(String, nullable=True, default="")

  ######################################
 #########  Site Languages  ###########
######################################
 #########     Dashboard    ###########
######################################
# class DashboardLanguages(Base):
#   __tablename__ = 'dashboard_language'

#   id = Column(Integer, primary_key=True)
  

 #########       Site       ###########
######################################
class SiteLanguages(Base):
  __tablename__ = 'site_language'

  id = Column(Integer, primary_key=True)
  lang_name = Column(String, nullable=False, unique=True)
  short_lang_name = Column(String, nullable=False, unique=True)
  is_active = Column(Boolean, default=True)
  site_about = Column(String, nullable=False)
  login_page_title = Column(String, nullable=False)
  user_logged_message = Column(String, nullable=False)
  wrong_password_message = Column(String, nullable=False)
  user_does_not_exist_message = Column(String, nullable=False)
  registration_page_title = Column(String, nullable=False)
  correct_email_message = Column(String, nullable=False)
  password_minimum_8_character_message = Column(String, nullable=False)
  name_not_added_message = Column(String, nullable=False)
  email_is_available_message = Column(String, nullable=False)
  registration_success = Column(String, nullable=False)
  contact_page_title = Column(String, nullable=False)
  message_spam_message = Column(String, nullable=False)
  the_message_cannot_empty_message = Column(String, nullable=False)
  boxes_are_cannot_empty = Column(String, nullable=False)
  message_has_been_sent_to_management = Column(String, nullable=False)
  educations_page_title = Column(String, nullable=False)
  news_page_title = Column(String, nullable=False)
  user_profile_info_page_title = Column(String, nullable=False)
  image_extension_error_message = Column(String, nullable=False)
  profile_success_message = Column(String, nullable=False)
  login = Column(String, nullable=False)
  why = Column(String, nullable=False)
  schedules = Column(String, nullable=False)
  week_days = Column(String, nullable=False)
  monday = Column(String, nullable=False)
  tuesday = Column(String, nullable=False)
  wednesday = Column(String, nullable=False)
  thursday = Column(String, nullable=False)
  friday = Column(String, nullable=False)
  saturday = Column(String, nullable=False)
  sunday = Column(String, nullable=False)
  our_staff = Column(String, nullable=False)
  previous = Column(String, nullable=False)
  next = Column(String, nullable=False)
  educations_all = Column(String, nullable=False)
  detail = Column(String, nullable=False)
  got_question_write_to_us_text = Column(String, nullable=False)
  address = Column(String, nullable=False)
  your_contact_number = Column(String, nullable=False)
  email = Column(String, nullable=False)
  number_of_joined_students = Column(String, nullable=False)
  view = Column(String, nullable=False)
  home = Column(String, nullable=False)
  education = Column(String, nullable=False)
  news = Column(String, nullable=False)
  about = Column(String, nullable=False)
  whatsapp_message = Column(String, nullable=False)
  call_us = Column(String, nullable=False)
  dashboard = Column(String, nullable=False)
  profile = Column(String, nullable=False)
  logout = Column(String, nullable=False)
  categories = Column(String, nullable=False)
  contact = Column(String, nullable=False)
  created_at = Column(String, nullable=False)
  category = Column(String, nullable=False)
  password = Column(String, nullable=False)
  sign_in = Column(String, nullable=False)
  register = Column(String, nullable=False)
  site_register = Column(String, nullable=False)
  logged_in = Column(String, nullable=False)
  registered = Column(String, nullable=False)
  name_and_surname = Column(String, nullable=False)
  update_profile = Column(String, nullable=False)
  city = Column(String, nullable=False)
  phone = Column(String, nullable=False)
  date_of_birth = Column(String, nullable=False)
  user_education = Column(String, nullable=False)
  certificate_grades_or_university = Column(String, nullable=False)
  user_about = Column(String, nullable=False)
  registration_date = Column(String, nullable=False)
  user_status = Column(String, nullable=False)
  education_of_choice = Column(String, nullable=False)
  high_education = Column(String, nullable=False)
  secondary_education = Column(String, nullable=False)
  profile_picture = Column(String, nullable=False)
  change_photo = Column(String, nullable=False)
  add_profile_picture = Column(String, nullable=False)
  save = Column(String, nullable=False)
  news_all = Column(String, nullable=False)
  last = Column(String, nullable=False)
  last_added = Column(String, nullable=False)
  video_tutorial = Column(String, nullable=False)
  site_closed = Column(String, nullable=False)
  site_closed_time = Column(String, nullable=False)
  site_closed_text_reason = Column(String, nullable=False)
  forgot_password = Column(String, nullable=False)
  email_sent = Column(String, nullable=False)
  email_is_not_registere = Column(String, nullable=False)
  change_password = Column(String, nullable=False)
  password_not_same_confirm_password = Column(String, nullable=False)
  password_changed = Column(String, nullable=False)
  forgot_password_question = Column(String, nullable=False)
  confirm_password = Column(String, nullable=False)
  link_timed_out = Column(String, nullable=False)
  visit_the_link_reset_password = Column(String, nullable=False)
  send = Column(String, nullable=False)
  
  ######################################
 ########   Admin Messages   ##########
######################################
class AdminMessages(Base):
  __tablename__ = 'admin_messages'
  
  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  email = Column(String, nullable=False)
  message = Column(Text, nullable=False)
  sender_id = Column(Integer, nullable=True)
  readed = Column(Integer, default=0)

  created_at = Column(DateTime, default=datetime.now())
  updated_at = Column(DateTime, onupdate=datetime.now())

  ######################################
 ##########     Staff     #############
######################################
class Staff(Base):
  __tablename__ = 'staff'

  id = Column(Integer, primary_key=True)
  name_surname = Column(String, nullable=False)
  job_position = Column(String, nullable=False)
  photo = Column(Text, nullable=False)
  facebook = Column(Text, nullable=True)
  instagram = Column(Text, nullable=True)
  linkedin = Column(Text, nullable=True)
  twitter = Column(Text, nullable=True)
  behance = Column(Text, nullable=True)

  ######################################
 #########  SliderSettings  ###########
######################################
class SliderSettings(Base):
  __tablename__ = 'slider_settings'

  id = Column(Integer, primary_key=True)
  slider = Column(Integer, nullable = True)
  title = Column(Text, nullable=True)
  description = Column(Text, nullable=True)
  news_photo = Column(String, nullable=True)
  photos = Column(String, nullable=True)
  views = Column(Integer, default=0)

  created_at = Column(DateTime, default=datetime.now())
  updated_at = Column(DateTime, onupdate=datetime.now())

  ######################################
 #########    Models end    ###########
######################################